# Smart-Waste-Segregation-System
An IoT-enabled Smart Waste Segregation System using Raspberry Pi, TensorFlow Lite, and Firebase. Automatically classifies waste as Organic, Recyclable, Hazardous.



# ♻️ Smart Waste Segregation System (IoT + ML)

![Python](https://img.shields.io/badge/Python-3.9-blue) ![Platform](https://img.shields.io/badge/Platform-Raspberry%20Pi%204-red) ![ML](https://img.shields.io/badge/ML-TensorFlow%20Lite-orange) ![IoT](https://img.shields.io/badge/IoT-Firebase-yellow)

An automated waste management system built for the **Smart India Hackathon**. This project uses **Computer Vision (Edge AI)** to detect waste types and **IoT** to monitor waste levels in real-time.

## 🚀 Features
* **Automated Sorting:** Classifies waste into 3 categories: **Organic**, **Recyclable**, and **Hazardous**.
* **Edge Computing:** Runs the ML model locally on Raspberry Pi 4 (no internet required for sorting).
* **IoT Dashboard:** Real-time web monitoring of waste counts and bin status using **Google Firebase**.
* **Smart Mechanism:** Uses Servo motors (MG996R) for a Pan-Tilt sorting mechanism.
* **Live Feedback:** Displays detection confidence and class on a local screen.

## 🛠️ Tech Stack
* **Hardware:** Raspberry Pi 4, Pi Camera Module v2, MG996R Servo Motors, IR Sensors.
* **Software:** Python 3, OpenCV (Computer Vision), TensorFlow Lite (ML Model).
* **IoT/Cloud:** Google Firebase Realtime Database.
* **Frontend:** HTML5, JavaScript (Chart.js) for the Dashboard.

## 📸 Screenshots
| **Detection Feed** | **IoT Dashboard** |
|:---:|:---:|
| <img width="805" height="634" alt="detection_demo" src="https://github.com/user-attachments/assets/8d7797c5-e357-4a5b-a094-cd225759db2c" />| <img width="1920" height="919" alt="Dashboard" src="https://github.com/user-attachments/assets/dea72cc0-6dfc-415a-a9c2-af2833526fcd" />
|


## ⚙️ How It Works
1.  **Detection:** An IR sensor detects the presence of waste.
2.  **Capture:** The Pi Camera captures an image.
3.  **Classification:** A custom-trained **MobileNetV2** model (via Teachable Machine) analyzes the image.
4.  **Actuation:**
    * **Organic:** Servo moves to 0°.
    * **Recyclable:** Servo moves to -55°.
    * **Hazardous:** Servo moves to +55°.
5.  **Cloud Upload:** The system uploads the data (Type, Timestamp, Confidence) to Firebase.

## 🔌 Circuit Diagram
*(You can upload a photo of your wiring or a Fritzing diagram here)*
* **Servo 1 (Base):** GPIO 17
* **Servo 2 (Flap):** GPIO 27
* **IR Sensor:** GPIO 22
* **Power:** External 5V 2A supply for servos (Common Ground with Pi).

## 🏃‍♂️ How to Run
1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/mayanksh0311/Smart-Waste-Segregator.git](https://github.com/mayanksh0311/Smart-Waste-Segregator.git)
    cd Smart-Waste-Segregator
    ```
2.  **Install Dependencies:**
    ```bash
    pip3 install opencv-python tensorflow tflite-runtime gpiozero requests
    ```
3.  **Run the Main Script:**
    ```bash
    python3 main.py
    ```
4.  **Open Dashboard:**
    Open `index.html` in any web browser to see live statistics.

## 🔮 Future Improvements
* **RFID User Authentication:** Integrating **RFID tags** to identify users. This allows for a "Rewards System" where users earn points for every item they correctly recycle.
* **GSM Alert Module:** Automatically sends SMS alerts to municipal authorities when the bins are full.
* **Solar Power Integration:** Making the system self-sustaining for outdoor deployment in parks and streets.
* **Dataset Expansion:** Retraining the model on a larger dataset (e.g., TrashNet) to improve detection accuracy in diverse lighting conditions.

## 👥 Contributors
* **Mayank Sharma**
* **[Mahima Bhardwaj](https://github.com/Mahimabhardwaj21)**
* **Abhishek Gautam**
* **Amit Pal**
* **Shreyanshi Mishra**
* **Aman Narayan**

---
*Built for SIH 2025*
