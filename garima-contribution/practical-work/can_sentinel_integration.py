
import random
import time

from intrusion_detector import detect_intrusions


def generate_can_message():
    """Generate one simulated CAN message."""
    can_id = random.choice([0x100, 0x101, 0x200, 0x300])
    data = [random.randint(0, 255) for _ in range(8)]

    return {
        "can_id": can_id,
        "data": data,
        "timestamp": time.time()
    }


def main():
    print("CAN-Sentinel: Integrated Intrusion Detection System")
    print("Generating and checking 10 simulated CAN messages...\n")

    messages = []

    for _ in range(10):
        message = generate_can_message()
        messages.append(message)

        print(
            f"CAN ID: 0x{message['can_id']:03X} | "
            f"Data: {message['data']} | "
            f"Time: {message['timestamp']:.3f}"
        )

    print("\n--- Intrusion Detection Results ---")
    alerts = detect_intrusions(messages)

    if alerts:
        print("Suspicious activity detected:")
        for alert in alerts:
            print(alert)
    else:
        print("No suspicious activity detected.")

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()
