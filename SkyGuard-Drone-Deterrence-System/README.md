# 🛡️ SkyGuard: Adaptive Bird Deterrence System for Delivery Drones

An AI-powered deterrence system to detect and counter bird attacks in real-time, designed for drones delivering essential supplies in hilly or high-risk regions.

---

## 📌 Problem Statement

Bird strikes are a serious threat to low-flying drones, especially during autonomous medical or supply deliveries in mountainous terrain. Around the 5 km mark in a typical 10 km mission, drones are vulnerable to attacks by birds like eagles and crows.

---

## 🎯 Objective

To design a lightweight, cost-effective smart deterrent system that:
- Detects birds via thermal imaging
- Classifies threat level (mild/moderate/severe)
- Activates adaptive response systems
- Sends alerts and performs evasive maneuvers

---

## 🧠 Key Features

| Feature | Description |
|--------|-------------|
| **Thermal AI Detection** | MLX90640 thermal camera + AI to detect flying objects and analyze behavior |
| **Threat Classification** | Based on size, trajectory, and movement pattern (flying/circling/diving) |
| **Adaptive Deterrence** | LEDs, ultrasonic pulse, predator sound, evasive flight pattern |
| **Environmental Awareness** | Rain sensor disables LEDs during fog/drizzle |
| **Failsafe Alerts** | GSM/LoRa distress signal + flight log |
| **Geofenced Activation** | System only runs in danger zones to save power |

---

## 🧩 System Architecture

![Flowchart + Block Diagram](docs/flowchart_blockdiagram.png)

---

## 🛠️ Hardware Used

| Component | Model | Function | Cost (₹) |
|----------|-------|----------|----------|
| **Controller** | Raspberry Pi Zero 2 W | Central unit for AI & control | 2,500 |
| **Thermal Sensor** | MLX90640 | 32×24 IR heatmap of surroundings | 6,500 |
| **Ultrasonic Sensor** | HC-SR04 | Proximity/distance sensing | 50 |
| **Rain Sensor** | FC-37 IR Type | Detects drizzle conditions | 100 |
| **LED Module** | High-Intensity RGB | Visual deterrent | 400 |
| **Speaker Module** | Mini 3W sound | Predator bird call output | 300 |
| **Battery** | 2S LiPo 2200mAh | Power supply | 800 |
| **GSM Module** | SIM800L | Distress alert (optional) | 900 |

**Total Cost**: ~ ₹12,000  
**Weight**: ~1.3 kg

---

## 📁 Project Structure

SkyGuard-Drone-Deterrence-System/
│
├── code/
│ └── skyguard_main.py # Main Python script
│
├── docs/
│ ├── SkyGuard_Presentation.pptx # Hackathon presentation
│ ├── Bill_of_Materials.xlsx # Component list
│ └── flowchart_blockdiagram.png # Diagrams
│
├── media/
│ └── skyguard_demo_video.mp4 # Animation video
│
├── logs/
│ └── example_log.csv # Sensor + alert logs
│
├── README.md
└── LICENSE

---

## 🚀 Getting Started

> 📦 Requirements: Raspberry Pi OS, Python 3, OpenCV, NumPy, Adafruit MLX90640

```bash
sudo apt install python3-pip
pip3 install opencv-python numpy adafruit-circuitpython-mlx90640 RPi.GPIO pymavlink
 Sample Log Output
csv
Copy
Edit
Time,Threat,Distance,Raining
2025-08-01 10:34:05,moderate,142.50,False
2025-08-01 10:34:09,severe,92.30,True
🎥 Demo Video
Watch how SkyGuard adapts to threats:
📽️ skyguard_demo_video.mp4

📄 License
MIT License – feel free to use, adapt, and build upon SkyGuard with credit.

✨ Credits
Developed by Sania Firdose  as part of AeroHack 2025
Guided by [ChatGPT + Raspberry Pi community]