
from intrusion_detector import detect_intrusions

print("CAN-Sentinel: Suspicious Message Test")
print("--------------------------------------")

# Simulate six messages from the same ECU
# and one message with an unexpected CAN ID.
test_messages = [
    {"can_id": 0x100},
    {"can_id": 0x100},
    {"can_id": 0x100},
    {"can_id": 0x100},
    {"can_id": 0x100},
    {"can_id": 0x100},
    {"can_id": 0x555},
]

print("Testing suspicious CAN traffic...\n")

alerts = detect_intrusions(test_messages)

if alerts:
    print("Suspicious activity detected:")
    for alert in alerts:
        print(alert)
else:
    print("No suspicious activity detected.")

print("\nTest complete.")
