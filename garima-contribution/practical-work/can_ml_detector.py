

import math
import random
import csv

from collections import Counter

from sklearn.ensemble import IsolationForest


def load_captured_messages(filename="can_traffic.csv"):
    """Load captured CAN messages from a CSV file."""
    messages = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            messages.append({
                "timestamp": float(row["timestamp"]),
                "data": bytes.fromhex(row["data"].strip()),
            })

    return messages


def calculate_entropy(data):
    """Calculate Shannon entropy of a CAN payload in bits per byte."""
    if not data:
        return 0.0

    counts = Counter(data)
    total = len(data)

    return -sum(
        (count / total) * math.log2(count / total)
        for count in counts.values()
    )


def extract_features(messages):
    """Extract message frequency and average payload entropy."""
    if not messages:
        return [0.0, 0.0]

    duration = max(
        messages[-1]["timestamp"] - messages[0]["timestamp"],
        0.001,
    )

    frequency = len(messages) / duration

    entropies = [
        calculate_entropy(message["data"])
        for message in messages
    ]

    average_entropy = sum(entropies) / len(entropies)

    return [frequency, average_entropy]


def create_normal_training_data():
    """Create illustrative normal CAN traffic for a demonstration."""
    training_data = []

    for _ in range(100):
        count = random.randint(8, 12)
        interval = random.uniform(0.08, 0.12)
        start_time = 0.0

        messages = []

        for i in range(count):
            start_time += interval
            messages.append({
                "timestamp": start_time,
                "data": [random.randint(0, 255) for _ in range(8)],
            })

        training_data.append(extract_features(messages))

    return training_data


def main():
    print("CAN-Sentinel: Machine Learning Detector")
    print("---------------------------------------")

    # Train on simulated normal traffic.
    training_data = create_normal_training_data()

    model = IsolationForest(
        contamination=0.05,
        random_state=42,
    )
    model.fit(training_data)

    # Test a normal simulated traffic batch.
    normal_messages = []
    for i in range(10):
        normal_messages.append({
            "timestamp": i * 0.1,
            "data": [random.randint(0, 255) for _ in range(8)],
        })

    # Test an unusually high-frequency batch.
    attack_messages = []
    for i in range(100):
        attack_messages.append({
            "timestamp": i * 0.001,
            "data": [255] * 8,
        })

    
    captured_messages = load_captured_messages()

    tests = [
        ("Normal simulated traffic", normal_messages),
        ("High-frequency simulated traffic", attack_messages),
        ("Captured CAN CSV traffic", captured_messages),
    ]
    for name, messages in tests:
        features = extract_features(messages)
        prediction = model.predict([features])[0]
        anomaly_score = model.decision_function([features])[0]

        print(f"\nTest: {name}")
        print(f"Message frequency: {features[0]:.2f} messages/second")
        print(f"Average payload entropy: {features[1]:.3f} bits/byte")
        print(f"Anomaly score: {anomaly_score:.4f}")

        if prediction == -1:
            print("ML result: ANOMALY DETECTED")
        else:
            print("ML result: Traffic resembles the training baseline")

    print("\nDemonstration complete.")
    print("Note: This uses synthetic data, not real vehicle traffic.")


if __name__ == "__main__":
    main()
    

    

