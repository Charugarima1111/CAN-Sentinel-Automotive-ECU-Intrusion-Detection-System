
import os
import socket
import time
import math
import random
from collections import Counter

from sklearn.ensemble import IsolationForest

SOCKET_PATH = "/tmp/can_sentinel.sock"
BATCH_SECONDS = 5


def entropy(data):
    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def extract_features(messages):
    duration = max(
        messages[-1][0] - messages[0][0],
        0.001
    )

    frequency = len(messages) / duration

    avg_entropy = sum(
        entropy(data) for _, data in messages
    ) / len(messages)

    return [frequency, avg_entropy]


def normal_training_data():
    training = []

    for _ in range(100):
        messages = []
        timestamp = 0.0
        interval = random.uniform(0.08, 0.12)

        for _ in range(10):
            timestamp += interval
            data = bytes(
                random.randint(0, 255) for _ in range(8)
            )
            messages.append((timestamp, data))

        training.append(extract_features(messages))

    return training


model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(normal_training_data())

if os.path.exists(SOCKET_PATH):
    os.remove(SOCKET_PATH)

server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server.bind(SOCKET_PATH)
server.listen(1)

print("CAN-Sentinel Python ML Receiver")
print("Waiting for C sniffer connection...")

try:
    connection, _ = server.accept()
    connection.settimeout(0.5)

    print("C sniffer connected successfully.")
    print("Analyzing incoming CAN traffic in 5-second batches.")

    buffer = b""
    batch = []
    batch_start = time.monotonic()

    while True:
        try:
            chunk = connection.recv(4096)

            if not chunk:
                print("C sniffer disconnected.")
                break

            buffer += chunk

            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)

                try:
                    can_id, dlc, payload = line.decode().split(",")

                    data = bytes.fromhex(payload)

                    if len(data) != int(dlc):
                        print("Invalid DLC received.")
                        continue

                    timestamp = time.monotonic()
                    batch.append((timestamp, data))

                    print(
                        f"Received CAN ID: 0x{int(can_id, 16):03X}"
                    )

                except (ValueError, UnicodeDecodeError):
                    print("Invalid CAN frame received.")

        except socket.timeout:
            pass

        if time.monotonic() - batch_start >= BATCH_SECONDS:
            if len(batch) >= 5:
                features = extract_features(batch)

                prediction = model.predict([features])[0]
                score = model.decision_function([features])[0]

                print("\n--- CAN-Sentinel ML Analysis ---")
                print(f"Messages: {len(batch)}")
                print(f"Frequency: {features[0]:.2f} messages/sec")
                print(f"Average entropy: {features[1]:.3f}")
                print(f"Anomaly score: {score:.4f}")

                if prediction == -1:
                    print("ML RESULT: ANOMALY DETECTED")
                else:
                    print("ML RESULT: NORMAL")

                print("--------------------------------\n")

            batch = []
            batch_start = time.monotonic()

except KeyboardInterrupt:
    print("\nPython ML receiver stopped.")

finally:
    if 'connection' in locals():
        connection.close()

    server.close()

    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    print("Socket receiver closed.")

