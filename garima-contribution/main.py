
from can_simulator import generate_can_message
from intrusion_detector import detect_intrusions


def main():
    print("CAN-Sentinel: Automotive ECU Intrusion Detection System")
    print("-" * 55)

    messages = []

    for _ in range(10):
        messages.append(generate_can_message())

    print(f"Generated {len(messages)} simulated CAN messages.")

    alerts = detect_intrusions(messages)

    print("\nIntrusion Detection Results:")

    if alerts:
        for alert in alerts:
            print(alert)
    else:
        print("No suspicious patterns detected.")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()

