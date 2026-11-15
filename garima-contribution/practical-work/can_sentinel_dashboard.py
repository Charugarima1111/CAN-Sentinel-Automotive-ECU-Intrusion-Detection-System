
import sys
import re
from pathlib import Path

from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel,
    QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QGridLayout, QFrame
)


class CanSentinelDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CAN-Sentinel | Automotive IDS Dashboard")
        self.setMinimumSize(850, 600)

        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.read_output)
        self.process.readyReadStandardError.connect(self.read_error)
        self.process.finished.connect(self.receiver_finished)

        self.total_messages = 0
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        layout = QVBoxLayout(central)

        title = QLabel("CAN-SENTINEL")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold; color: #00bcd4;"
        )
        layout.addWidget(title)

        subtitle = QLabel("Automotive ECU Intrusion Detection System")
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)

        self.status = QLabel("STATUS: STOPPED")
        self.status.setAlignment(Qt.AlignCenter)
        self.status.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: red;"
        )
        layout.addWidget(self.status)

        grid = QGridLayout()

        self.messages = self.make_card("Total CAN Messages", "0")
        self.can_id = self.make_card("Latest CAN ID", "N/A")
        self.frequency = self.make_card("Frequency", "0 messages/sec")
        self.entropy = self.make_card("Average Entropy", "0.000")
        self.score = self.make_card("Anomaly Score", "N/A")
        self.result = self.make_card("ML Classification", "WAITING")

        cards = [
            self.messages, self.can_id, self.frequency,
            self.entropy, self.score, self.result
        ]

        for index, card in enumerate(cards):
            grid.addWidget(card, index // 3, index % 3)

        layout.addLayout(grid)

        buttons = QHBoxLayout()

        self.start_button = QPushButton("START RECEIVER")
        self.stop_button = QPushButton("STOP RECEIVER")
        self.stop_button.setEnabled(False)

        self.start_button.clicked.connect(self.start_receiver)
        self.stop_button.clicked.connect(self.stop_receiver)

        buttons.addWidget(self.start_button)
        buttons.addWidget(self.stop_button)
        layout.addLayout(buttons)

        log_title = QLabel("LIVE ACTIVITY LOG")
        log_title.setStyleSheet("font-weight: bold;")
        layout.addWidget(log_title)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        layout.addWidget(self.log)

        central.setStyleSheet(
            "background-color: #17212b; color: white;"
        )

        self.setStyleSheet("""
            QPushButton {
                background-color: #008c9e;
                color: white;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:disabled {
                background-color: #555555;
            }
            QTextEdit {
                background-color: #101820;
                color: #00e676;
                font-family: monospace;
            }
        """)

    def make_card(self, heading, value):
        card = QFrame()
        card.setFrameShape(QFrame.Box)
        card.setStyleSheet(
            "QFrame { border: 1px solid #00bcd4; padding: 12px; }"
        )

        box = QVBoxLayout(card)

        name = QLabel(heading)
        name.setAlignment(Qt.AlignCenter)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet(
            "font-size: 18px; font-weight: bold; color: #00e5ff;"
        )

        box.addWidget(name)
        box.addWidget(value_label)

        card.value_label = value_label
        return card

    def add_log(self, message):
        self.log.append(message)

    def start_receiver(self):
        script = Path(__file__).with_name("can_socket_receiver.py")

        if not script.exists():
            self.add_log("ERROR: Receiver file not found.")
            return

        self.process.start(
            sys.executable,
            ["-u", str(script)]
        )

        if not self.process.waitForStarted(3000):
            self.add_log("ERROR: Could not start Python receiver.")
            return

        self.status.setText("STATUS: STARTING / WAITING FOR C SNIFFER")
        self.status.setStyleSheet("color: orange; font-weight: bold;")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.add_log("Python ML receiver started.")

    def read_output(self):
        data = bytes(self.process.readAllStandardOutput())
        output = data.decode(errors="replace")

        for line in output.splitlines():
            self.add_log(line)

            if "C sniffer connected successfully" in line:
                self.status.setText("STATUS: MONITORING")
                self.status.setStyleSheet(
                    "color: #00e676; font-weight: bold;"
                )

            if "Received CAN ID:" in line:
                match = re.search(r"0x[0-9A-Fa-f]+", line)
                if match:
                    self.total_messages += 1
                    self.messages.value_label.setText(
                        str(self.total_messages)
                    )
                    self.can_id.value_label.setText(match.group())

            if "Frequency:" in line:
                self.frequency.value_label.setText(
                    line.split("Frequency:", 1)[1].strip()
                )

            if "Average entropy:" in line:
                self.entropy.value_label.setText(
                    line.split("Average entropy:", 1)[1].strip()
                )

            if "Anomaly score:" in line:
                self.score.value_label.setText(
                    line.split("Anomaly score:", 1)[1].strip()
                )

            if "ML RESULT: NORMAL" in line:
                self.result.value_label.setText("NORMAL")
                self.result.value_label.setStyleSheet(
                    "color: #00e676; font-size: 18px; font-weight: bold;"
                )

            if "ML RESULT: ANOMALY DETECTED" in line:
                self.result.value_label.setText("ANOMALY")
                self.result.value_label.setStyleSheet(
                    "color: #ff5252; font-size: 18px; font-weight: bold;"
                )

    def read_error(self):
        data = bytes(self.process.readAllStandardError())
        if data:
            self.add_log("ERROR: " + data.decode(errors="replace"))

    def stop_receiver(self):
        if self.process.state() != QProcess.NotRunning:
            self.process.terminate()
            if not self.process.waitForFinished(2000):
                self.process.kill()

    def receiver_finished(self):
        self.status.setText("STATUS: STOPPED")
        self.status.setStyleSheet("color: red; font-weight: bold;")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.add_log("Python ML receiver stopped.")

    def closeEvent(self, event):
        if self.process.state() != QProcess.NotRunning:
            self.process.terminate()
            if not self.process.waitForFinished(2000):
                self.process.kill()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CanSentinelDashboard()
    window.show()
    sys.exit(app.exec_())
x
