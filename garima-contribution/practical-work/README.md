# CAN-Sentinel – Practical Work

This folder contains practical testing and machine-learning experiments completed for the CAN-Sentinel Automotive ECU Intrusion Detection System.

## Files
- `can_ml_detector.py` – Isolation Forest anomaly-detection experiment using CAN traffic features.
- `can_sentinel_integration.py` – Integration test for simulated CAN messages and intrusion detection.
- `test_intrusion_detection.py` – Tests unexpected CAN IDs and excessive message counts.
- `can_traffic.csv` – Sample CAN traffic dataset.
- `can_traffic.log` – Captured CAN traffic log.
- `high_count.log` – Test log for high message frequency.
- `multi_id.log` – Test log containing multiple CAN IDs, including an unexpected ID.

## Verified test observations
- Virtual CAN (`vcan0`) transmission test: 100 frames sent and 100 received, with zero missing.
- Rule-based detector identified unexpected CAN ID `0x555`.
- Rule-based detector identified a high message count for CAN ID `0x100`.
- Isolation Forest experiments demonstrated anomaly detection using message frequency and CAN ID entropy.

## Scope and limitations
These results are from a virtual CAN interface and simulated/sample traffic. They do not represent testing on a physical vehicle. Full live C-sniffer integration and a PyQt dashboard remain outside this verified contribution.
