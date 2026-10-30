
import random
import time

def generate_can_message():
    """Generate a simulated CAN message."""
    can_id = random.choice([0x100, 0x101, 0x200, 0x300])
    data = [random.randint(0, 255) for _ in range(8)]

    return {
        "can_id": can_id,
        "data": data,
        "timestamp": time.time()
    }

def main():
    print("CAN-Sentinel: CAN Traffic Simulator")
    print("Generating 10 simulated CAN messages...\n")

    for _ in range(10):
        message = generate_can_message()
        print(
            f"CAN ID: 0x{message['can_id']:03X} | "
            f"Data: {message['data']} | "
            f"Time: {message['timestamp']:.3f}"
        )

if __name__ == "__main__":
    main()
