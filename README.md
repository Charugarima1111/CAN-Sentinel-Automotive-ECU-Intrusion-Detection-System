# CAN-Sentinel: Automotive ECU Intrusion Detection System

**Project Code:** ITS/CS/1076 | **Group No:** 1 | **Domain:** Cyber Security | **Duration:** 3 Months
**Status:** In Progress

### Team Members - Group No 1
- Garima Verma
- Ankita Modi
- Akhil Bojja
- Hardik Mittal

---

### 1. Project Aim
To design and develop an Intrusion Detection System (IDS) for automotive CAN (Controller Area Network) bus to detect and mitigate cyber-attacks targeting ECUs.

### 2. Problem Statement
Modern vehicles use CAN bus protocol which has no authentication and encryption. Attackers can inject malicious frames via OBD-II port or wireless interfaces, causing critical safety risks like brake failure and fake sensor readings. This project builds a defense layer to detect such intrusions in real-time.

### 3. Types of Attacks Detected
1.  **DoS Attack:** Flooding the bus with high-priority ID 0x000
2.  **Spoofing Attack:** Injecting fake RPM / Speed messages
3.  **Fuzzing Attack:** Injecting random CAN IDs with random data

### 4. Tech Stack
- Python, python-can, Scikit-Learn, Pandas
- Flask, HTML, CSS, JavaScript
- GitHub & VS Code Codespaces

### 5. System Architecture
`Virtual CAN Bus -> Normal ECU Traffic + Attack Injector -> IDS Detection Engine -> Web Dashboard (Alerts)`

### 6. Project Structure
- `/simulator` - CAN traffic simulator
- `/attacks` - Attack generation modules
- `/detection` - ML based anomaly detection
- `/dashboard` - Live monitoring dashboard

### 7. Day-wise Progress
- **Day 1:** Repository Created & Linked to Infotact Portal
- **Day 2:** Created initial index.html dashboard
- **Day 3:** Added detailed project documentation (README)
- **Day 4 Onwards:** Simulator and Attack modules development

### 8. How to Run
```bash
pip install python-can scikit-learn flask
python simulator.py
