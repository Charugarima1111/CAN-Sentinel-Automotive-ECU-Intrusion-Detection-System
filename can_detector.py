
def detect_intrusion(can_id):
    suspicious_ids = ["0x666", "0x777"]

    if can_id in suspicious_ids:
        return "ALERT: Suspicious CAN message detected!"

    return "Normal CAN message"


def main():
    print("CAN-Sentinel: Automotive ECU Intrusion Detection System")

    can_id = input("Enter CAN ID (example: 0x123): ")
    result = detect_intrusion(can_id)

    print(result)


if __name__ == "__main__":
    main()
