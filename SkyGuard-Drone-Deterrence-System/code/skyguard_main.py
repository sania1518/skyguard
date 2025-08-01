# Main Python script for Raspberry Pi
import time, datetime, board, busio, digitalio
import adafruit_mlx90640
import RPi.GPIO as GPIO
import numpy as np, cv2, serial
from pymavlink import mavutil

# GPIO Pin Definitions
TRIG = 23
ECHO = 24
LED = 18
SPEAKER = 25
RAIN_SENSOR = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup([TRIG, LED, SPEAKER], GPIO.OUT)
GPIO.setup([ECHO, RAIN_SENSOR], GPIO.IN)

# I2C Setup
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
frame = [0] * 768

# Pixhawk MAVLink
pixhawk = mavutil.mavlink_connection('/dev/ttyAMA0', baud=57600)

# Logging setup
log_file = open("/home/pi/skyguard_log.csv", "a")
log_file.write("Time,Threat,Distance,Raining\n")

# Ultrasonic Distance
def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start, stop = time.time(), time.time()
    while GPIO.input(ECHO) == 0: start = time.time()
    while GPIO.input(ECHO) == 1: stop = time.time()
    return ((stop - start) * 34300) / 2

# Blob detection → classify threat
def detect_threat_level(frame):
    img = np.reshape(frame, (24, 32))
    img_resized = cv2.resize(img, (160, 120), interpolation=cv2.INTER_CUBIC)
    _, thresh = cv2.threshold(img_resized, 33.0, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(np.uint8(thresh), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours: return "none"
    area = max([cv2.contourArea(c) for c in contours])
    return "mild" if area < 50 else "moderate" if area < 150 else "severe"

# Adaptive Deterrent Activation
def trigger_response(level, raining=False):
    if level == "mild":
        GPIO.output(SPEAKER, True)
        time.sleep(0.1)
        GPIO.output(SPEAKER, False)

    elif level == "moderate":
        if not raining: GPIO.output(LED, True)
        GPIO.output(SPEAKER, True)
        time.sleep(1)
        GPIO.output(LED, False)
        GPIO.output(SPEAKER, False)

    elif level == "severe":
        if not raining: GPIO.output(LED, True)
        GPIO.output(SPEAKER, True)
        evasive_maneuver()
        send_alert()
        time.sleep(2)
        GPIO.output(LED, False)
        GPIO.output(SPEAKER, False)

# Send alert to ground via GSM or LoRa
def send_alert():
    alert_msg = f"ALERT: Bird Attack at {datetime.datetime.now()}"
    try:
        with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as gsm:
            gsm.write(alert_msg.encode())
    except Exception as e:
        print("GSM/LoRa not responding:", e)

# Evasive command to Pixhawk (basic example: roll)
def evasive_maneuver():
    print("Sending evasive zigzag to Pixhawk...")
    pixhawk.mav.command_long_send(
        pixhawk.target_system,
        pixhawk.target_component,
        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
        0, 1, 5, -1, 0, 0, 0, 0
    )
    time.sleep(0.5)

# Log data
def log_event(threat, distance, rain):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file.write(f"{now},{threat},{distance:.2f},{rain}\n")
    log_file.flush()

# MAIN LOOP
try:
    print("SkyGuard Online")
    while True:
        rain = GPIO.input(RAIN_SENSOR) == GPIO.HIGH
        mlx.getFrame(frame)
        threat = detect_threat_level(frame)
        distance = get_distance()

        print(f"Threat: {threat} | Distance: {distance:.2f} cm | Rain: {rain}")
        if threat != "none":
            trigger_response(threat, raining=rain)
            log_event(threat, distance, rain)

        time.sleep(0.5)

except KeyboardInterrupt:
    print("Shutdown requested.")
    log_file.close()
    GPIO.cleanup()
