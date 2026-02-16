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
| *(Add a screenshot of your CV2 window here)* | *(Add a screenshot of your website here)* |

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
    git clone [https://github.com/your-username/Smart-Waste-Segregator.git](https://github.com/your-username/Smart-Waste-Segregator.git)
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
* Add a GSM module to send SMS alerts when bins are full.
* Implement solar panels for a self-sustaining system.
* Train the model on a larger dataset (TrashNet) for better accuracy.

## 👥 Contributors
* **[Your Name]** - *Lead Developer & ML Engineer*
* **[Teammate Name]** - *Hardware Integration*

---
*Built for Hackathon 2025*
