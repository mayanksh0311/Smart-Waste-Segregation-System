import time
import RPi.GPIO as GPIO
from picamera2 import Picamera2
from PIL import Image
import numpy as np
import os

#  --- GPIO Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# IR Sensor Pin
IR_SENSOR_PIN = 17
GPIO.setup(IR_SENSOR_PIN, GPIO.IN)

# Servo Motor Pins
SERVO_HORIZONTAL_PIN = 18  # Bin Selection
SERVO_VERTICAL_PIN = 13    # Drop Mechanism
GPIO.setup(SERVO_HORIZONTAL_PIN, GPIO.OUT)
GPIO.setup(SERVO_VERTICAL_PIN, GPIO.OUT)

# Initialize Servo PWM
pwm_horizontal = GPIO.PWM(SERVO_HORIZONTAL_PIN, 50)
pwm_vertical = GPIO.PWM(SERVO_VERTICAL_PIN, 50)
pwm_horizontal.start(0)
pwm_vertical.start(0)

# Servo duty cycles for each waste category
BIN_POSITIONS = {
    'hazardous': 5.0,     # Left position
    'organic': 7.5,       # Center position
    'recyclable': 10.0    # Right position
}

VERTICAL_POSITIONS = {
    'up': 7.5,     # Up position
    'down': 12.0   # Down position
}

# --- Camera Setup for Camera Module 1.3 ---
picam2 = Picamera2()

# Camera Module 1.3 optimized configuration
config = picam2.create_still_configuration(
    main={"size": (1296, 972)},  # Optimal for OV5647 sensor
    buffer_count=4
)
picam2.configure(config)

# Set camera controls
controls = {
    "FrameRate": 15,
    "AwbMode": 0,  # Auto white balance
    "ExposureTime": 10000
}
picam2.set_controls(controls)

# AI Model Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'waste_model.tflite')
LABELS_PATH = os.path.join(SCRIPT_DIR, 'class_indices.txt')


# Load the class labels
try:
    with open(LABELS_PATH, 'r') as f:
        CLASS_LABELS = [line.strip() for line in f.readlines() if line.strip()]
    print(f"Labels loaded: {CLASS_LABELS}")
except FileNotFoundError:
    print(f"ERROR: Labels file not found at {LABELS_PATH}")
    CLASS_LABELS = ["hazardous", "organic", "recyclable"]  # Default fallback

# Load the TFLite model
try:
    from tflite_runtime.interpreter import Interpreter
    interpreter = Interpreter(model_path=MODEL_PATH)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print("AI Model loaded successfully.")
    MODEL_LOADED = True
except Exception as e:
    print(f"ERROR loading model: {e}")
    print("Running in DEMO MODE - will cycle through all waste types.")
    interpreter = None
    MODEL_LOADED = False

# --- Function Definitions ---
def set_servo_angle(servo_pwm, duty_cycle):
    """Moves a servo to a specific duty cycle (2.5% to 12.5%)."""
    duty_cycle = max(2.5, min(12.5, duty_cycle))
    servo_pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.8)  # Time for servo to move
    servo_pwm.ChangeDutyCycle(0)  # Stop signal to prevent jitter

def capture_and_classify():
    """Captures image and returns waste type prediction."""
    if not MODEL_LOADED:
        print("Using DEMO MODE - cycling through waste types")
        # Cycle through: hazardous -> organic -> recyclable
        if not hasattr(capture_and_classify, "demo_counter"):
            capture_and_classify.demo_counter = 0
        
        waste_types = ["hazardous", "organic", "recyclable"]
        waste_type = waste_types[capture_and_classify.demo_counter % 3]
        capture_and_classify.demo_counter += 1
        return waste_type, 0.95

    # Start camera and capture image
    picam2.start()
    time.sleep(2)  # Let camera adjust to light
    image_array = picam2.capture_array()
    picam2.stop()

    # Convert and preprocess image
    rgb_image = image_array[:, :, ::-1]  # BGR to RGB
    pil_image = Image.fromarray(rgb_image).resize((128, 128))
    input_data = np.array(pil_image, dtype=np.float32) / 255.0
    input_data = np.expand_dims(input_data, axis=0)

    # Run AI model inference
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    results = interpreter.get_tensor(output_details[0]['index'])
    
    # Get prediction
    predicted_class_idx = np.argmax(results[0])
    confidence = results[0][predicted_class_idx]
    
    # Get label name
    if CLASS_LABELS and predicted_class_idx < len(CLASS_LABELS):
        predicted_label = CLASS_LABELS[predicted_class_idx]
        if ':' in predicted_label:
            predicted_label = predicted_label.split(':')[1]
    else:
        predicted_label = "organic"  # Default fallback

    return predicted_label, confidence

def process_waste(waste_type):
    """Complete waste sorting sequence."""
    print(f"\nProcessing {waste_type} waste...")
    
    # 1. Move horizontal servo to bin position
    target_duty = BIN_POSITIONS.get(waste_type, 7.5)
    print(f"  Moving to {waste_type} bin (duty: {target_duty}%)")
    set_servo_angle(pwm_horizontal, target_duty)
    time.sleep(1)
    
    # 2. Move vertical servo down to drop item
    print("  Dropping item...")
    set_servo_angle(pwm_vertical, VERTICAL_POSITIONS['down'])
    time.sleep(2)  # Wait for item to fall
    
    # 3. Move vertical servo back up
    print("  Resetting dropper...")
    set_servo_angle(pwm_vertical, VERTICAL_POSITIONS['up'])
    time.sleep(1)
    
    # 4. Return to center position
    print("  Returning to center...")
    set_servo_angle(pwm_horizontal, BIN_POSITIONS['organic'])
    
    print(f"  {waste_type} waste sorted successfully!")

# --- Main Program ---
print("""
###############################################
      AUTOMATIC WASTE SEGREGATION SYSTEM
      Using Raspberry Pi Camera Module 1.3
###############################################
""")

print("System Initializing...")
print("Horizontal Servo: Bin Selection (Left, Center, Right)")
print("Vertical Servo: Drop Mechanism (Up, Down)")
print("IR Sensor: Object Detection")
print("Camera: Waste Classification")

# Test servos on startup
print("\nTesting servos on startup...")
set_servo_angle(pwm_horizontal, BIN_POSITIONS['organic'])
set_servo_angle(pwm_vertical, VERTICAL_POSITIONS['up'])
print("Servo test completed.")

print("\nSystem ready! Waiting for waste detection...")
print("Place waste in front of IR sensor to begin.")
print("Press Ctrl+C to stop the system\n")

try:
    while True:
        # Check IR sensor (0 = object detected)
        if GPIO.input(IR_SENSOR_PIN) == 0:
            print("\n" + "="*50)
            print("WASTE DETECTED!")
            print("Please place item in front of camera...")
            time.sleep(3)  # Time to place item
            
            # Capture and classify
            print("Analyzing waste...")
            waste_type, confidence = capture_and_classify()
            print(f"CLASSIFICATION: {waste_type.upper()} ({confidence:.1%} confidence)")
            
            # Sort the waste
            process_waste(waste_type)
            
            print("\nReady for next item...")
            print("="*50)
        
        time.sleep(0.1)  # Small delay

except KeyboardInterrupt:
    print("\n\nShutting down system...")

finally:
    # Cleanup - always runs
    print("Stopping servos and cleaning up...")
    pwm_horizontal.stop()
    pwm_vertical.stop()
    GPIO.cleanup()
    print("System shutdown complete. Thank you!")
