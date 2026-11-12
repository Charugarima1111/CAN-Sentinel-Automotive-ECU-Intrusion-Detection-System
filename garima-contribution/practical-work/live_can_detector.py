import can
import time
from collections import defaultdict, deque

KNOWN_IDS = {0x100, 0x200, 0x300, 0x400}
SUSPICIOUS_IDS = {0x000, 0x7FF}
RATE_LIMIT = 20

history = defaultdict(deque)
alerted_ids = set()

print("CAN-Sentinel Live Intrusion Detector")
print("Monitoring vcan0. Press Ctrl+C to stop.")

try:
    with can.Bus(interface="socketcan", channel="vcan0") as bus:
        while True:
            msg = bus.recv(timeout=1)

            if msg is None:
                continue

            now = time.time()
            frames = history[msg.arbitration_id]
            frames.append(now)

            while frames and now - frames[0] > 1:
                frames.popleft()

            can_id = msg.arbitration_id
            print(f"ID: 0x{can_id:03X} | Data: {msg.data.hex().upper()}")

            if can_id in SUSPICIOUS_IDS:
                print("ALERT: Suspicious CAN ID detected!")

            elif can_id not in KNOWN_IDS:
                print("WARNING: Unknown CAN ID detected!")

            if len(frames) > RATE_LIMIT and can_id not in alerted_ids:
                print("ALERT: High message frequency detected!")
                alerted_ids.add(can_id)
            elif len(frames) <= RATE_LIMIT:
                alerted_ids.discard(can_id)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
