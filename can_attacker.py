"""
CAN-Sentinel - Day 5: DoS Attack Simulator Module
Project 1 - Automotive ECU Intrusion Detection System
Infotact Solutions - Week 2: Malware Injection
"""

import time
import random
import datetime

NORMAL_IDS = {
    0x0C0: "Engine RPM",
    0x0D0: "Vehicle Speed", 
    0x0B0: "Brake Status",
    0x0A0: "Steering Angle"
}

ATTACK_IDS = {
    0x000: "DoS Flood (Highest Priority)",
    0x0B0: "Spoofed Brake Release",
    0x0C0: "Spoofed RPM Override"
}

def log_frame(can_id, data, attack=False):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
    label = "!!! ATTACK !!!" if attack else "NORMAL"
    print(f"[{timestamp}] ID: 0x{can_id:03X} ({ATTACK_IDS.get(can_id, NORMAL_IDS.get(can_id, 'Unknown')):20s}) Data: {data} | {label}")

def normal_traffic_cycle():
    for can_id in NORMAL_IDS:
        data = [random.randint(0, 255) for _ in range(8)]
        hex_data = ' '.join(f'{b:02X}' for b in data)
        log_frame(can_id, hex_data, attack=False)
        time.sleep(0.05)

def dos_attack(num_frames=50, delay=0.01):
    print("\n" + "="*65)
    print(">>> LAUNCHING DoS ATTACK - Flooding ID 0x000")
    print("="*65 + "\n")
    for i in range(num_frames):
        hex_data = ' '.join(f'{0x00:02X}' for _ in range(8))
        log_frame(0x000, hex_data, attack=True)
        time.sleep(delay)
    print(f"\n[ATTACK COMPLETE] {num_frames} frames\n")

def spoofing_attack(num_frames=20):
    print("\n" + "="*65)
    print(">>> LAUNCHING SPOOFING ATTACK - Fake Brake Release")
    print("="*65 + "\n")
    for i in range(num_frames):
        fake_brake_data = [0x00, 0x00, 0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00]
        hex_data = ' '.join(f'{b:02X}' for b in fake_brake_data)
        log_frame(0x0B0, hex_data, attack=True)
        time.sleep(0.02)

def mixed_attack_demo():
    print("CAN-Sentinel: Week 2 Attack Simulation")
    print("Date:", datetime.datetime.now().strftime("%d %b %Y"))
    print("-"*65)
    print("\n[PHASE 1] Normal Traffic Baseline (2 sec)")
    for _ in range(2):
        normal_traffic_cycle()
        time.sleep(0.5)
    dos_attack(num_frames=30, delay=0.01)
    print("\n[PHASE 2] Recovery")
    normal_traffic_cycle()
    spoofing_attack(num_frames=15)
    print("\n" + "="*65)
    print("ANALYSIS FOR ML MODEL (Week 2):")
    print("- Normal: ~40 frames/sec, balanced IDs")
    print("- DoS: >100 frames/sec, ID 0x000 dominates")
    print("- Isolation Forest should flag frequency anomaly")
    print("="*65)

if __name__ == "__main__":
    mixed_attack_demo()
