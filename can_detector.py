from datetime import datetime

# Example rules for simulated CAN traffic
KNOWN_ECU_IDS = {0x100, 0x200, 0x300, 0x400}
SUSPICIOUS_IDS = {0x000, 0x7FF}

def detect_intrusion(can_id, dlc):
    timestamp = datetime.now().strftime("%H:%M:%S")

    if can_id in SUSPICIOUS_IDS:
        return f"[{timestamp}] ALERT: Suspicious CAN ID 0x{can_id:X}"

    if can_id not in KNOWN_ECU_IDS:
        return f"[{timestamp}] WARNING: Unknown CAN ID 0x{can_id:X}"

    if not 0 <= dlc <= 8:
        return f"[{timestamp}] ALERT: Invalid CAN data length"

    return f"[{timestamp}] NORMAL: Recognized ECU message"


if __name__ == "__main__":
    print("CAN-Sentinel Intrusion Detector")
    can_id = int(input("Enter CAN ID (example: 0x100): "), 16)
    dlc = int(input("Enter data length (0-8): "))

    print(detect_intrusion(can_id, dlc))
