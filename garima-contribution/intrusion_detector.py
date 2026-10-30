
ALLOWED_CAN_IDS = {0x100, 0x101, 0x200, 0x300}
MAX_MESSAGES_PER_ID = 5


def detect_intrusions(messages):
    alerts = []
    id_counts = {}

    for message in messages:
        can_id = message["can_id"]

        # Check for an unexpected CAN identifier
        if can_id not in ALLOWED_CAN_IDS:
            alerts.append(
                f"ALERT: Unexpected CAN ID 0x{can_id:03X}"
            )

        # Count messages for each CAN identifier
        id_counts[can_id] = id_counts.get(can_id, 0) + 1

        if id_counts[can_id] > MAX_MESSAGES_PER_ID:
            alerts.append(
                f"ALERT: High message count for CAN ID 0x{can_id:03X}"
            )

    return alerts


if __name__ == "__main__":
    test_messages = [
        {"can_id": 0x100},
        {"can_id": 0x100},
        {"can_id": 0x555},
        {"can_id": 0x100},
        {"can_id": 0x100},
        {"can_id": 0x100},
        {"can_id": 0x100},
    ]

    results = detect_intrusions(test_messages)

    if results:
        print("Suspicious activity detected:")
        for alert in results:
            print(alert)
    else:
        print("No suspicious activity detected.")
