# CAN-Sentinel – Practical Work

This folder contains practical testing and machine-learning experiments completed for the CAN-Sentinel Automotive ECU Intrusion Detection System.

## Files

- `can_ml_detector.py` – Isolation Forest anomaly-detection experiment using CAN traffic features.
- `live_can_ml_detector.py` – Live CAN traffic monitoring and ML-based anomaly detection on vcan0.
- `live_can_detector.py` – Rule-based live CAN intrusion detector.
- `live_ml_test_results.txt` – Results of live ML normal and high-frequency traffic tests.
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
- Isolation Forest experiments demonstrated anomaly detection using message frequency and payload entropy.
- Live rule-based detector successfully identified suspicious CAN ID `0x000`, unknown CAN ID `0x555`, and high-frequency traffic.
- Live ML detector classified normal virtual CAN traffic as NORMAL.
- Live ML detector classified a 100-frame high-frequency burst as ANOMALY DETECTED.

## Live ML test results

**Algorithm:** Isolation Forest

**Features:** Message frequency and average payload entropy.

| Test | Frames | Frequency | Entropy | Result |
|---|---:|---:|---:|---|
| Normal traffic | 10 | 8.85/sec | 3.000 | NORMAL |
| High-frequency burst | 100 | 6074.23/sec | 0.000 | ANOMALY DETECTED |

The live ML prototype collects CAN frames in five-second batches and evaluates each batch using its trained Isolation Forest model.

## Scope and limitations

These results are from a virtual CAN interface and simulated/sample traffic. The ML training baseline uses synthetic data and requires further validation with representative automotive CAN datasets.

These results do not represent testing on a physical vehicle. Full live C-sniffer integration and a PyQt dashboard remain outside this verified contribution.
