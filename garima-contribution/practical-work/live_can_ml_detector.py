import time
import math
import random
import can
from collections import Counter
from sklearn.ensemble import IsolationForest

def entropy(data):
    if not data:
        return 0.0
    counts = Counter(data)
    total = len(data)
    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )

def features(messages):
    duration = max(messages[-1][0] - messages[0][0], 0.001)
    frequency = len(messages) / duration
    avg_entropy = sum(entropy(data) for _, data in messages) / len(messages)
    return [frequency, avg_entropy]

def normal_training_data():
    training = []
    for _ in range(100):
        messages = []
        timestamp = 0.0
        interval = random.uniform(0.08, 0.12)

        for _ in range(10):
            timestamp += interval
            data = bytes(random.randint(0, 255) for _ in range(8))
            messages.append((timestamp, data))

        training.append(features(messages))

    return training

model = IsolationForest(contamination=0.05, random_state=42)
model.fit(normal_training_data())

print("CAN-Sentinel Live ML Detector")
print("Monitoring vcan0 in 5-second batches.")

try:
    with can.Bus(interface="socketcan", channel="vcan0") as bus:
        while True:
            batch = []
            start = time.monotonic()

            while time.monotonic() - start < 5:
                msg = bus.recv(timeout=0.5)
                if msg is not None:
                    batch.append((time.monotonic(), bytes(msg.data)))

            if not batch:
                print("No CAN traffic received in this batch.")
                continue

            result = features(batch)
            prediction = model.predict([result])[0]
            score = model.decision_function([result])[0]

            print(f"\nMessages: {len(batch)}")
            print(f"Frequency: {result[0]:.2f} messages/sec")
            print(f"Average entropy: {result[1]:.3f}")
            print(f"Anomaly score: {score:.4f}")

            if prediction == -1:
                print("ML RESULT: ANOMALY DETECTED")
            else:
                print("ML RESULT: NORMAL")

except KeyboardInterrupt:
    print("\nLive ML monitoring stopped.")
