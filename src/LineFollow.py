import cv2
import numpy as np
import RPi.GPIO as GPIO
from time import sleep
import threading
import queue
import signal
import sys

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
AN2, AN1, DIG2, DIG1 = 12, 13, 19, 16
GPIO.setup(AN2, GPIO.OUT)
GPIO.setup(AN1, GPIO.OUT)
GPIO.setup(DIG2, GPIO.OUT)
GPIO.setup(DIG1, GPIO.OUT)
p1 = GPIO.PWM(AN1, 100)
p2 = GPIO.PWM(AN2, 100)

# Shared variables
direction_queue = queue.Queue()
exit_flag = threading.Event()

# Define the cleanup function for exiting
def handle_exit(signal, frame):
    print("\nExiting and cleaning up GPIO...")
    p1.stop()
    p2.stop()
    GPIO.cleanup()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, handle_exit)

def detect_line(frame):
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range of black color in HSV
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 30])
    
    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_black, upper_black)
    
    # Apply morphological operations to remove noise
    kernel = np.ones((5,5),np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    
    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Get the moments of the largest contour
        moments = cv2.moments(largest_contour)
        
        if moments["m00"] != 0:
            # Calculate the center of the contour
            cx = int(moments["m10"] / moments["m00"])
            cy = int(moments["m01"] / moments["m00"])
            
            # Draw the contour and center point
            cv2.drawContours(frame, [largest_contour], 0, (0,255,0), 2)
            cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)
            
            return frame, cx
    
    return frame, None

def camera_thread():
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Camera could not be opened")
        exit_flag.set()
        return

    while not exit_flag.is_set():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame, center_x = detect_line(frame)
        
        if center_x is not None:
            if center_x < frame.shape[1] / 3:
                direction_queue.put("LEFT")
            elif center_x > 2 * frame.shape[1] / 3:
                direction_queue.put("RIGHT")
            else:
                direction_queue.put("STRAIGHT")
        else:
            direction_queue.put("STOP")
        
        cv2.imshow('Line Tracer', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit_flag.set()
    
    cap.release()
    cv2.destroyAllWindows()

def motor_control_thread():
    while not exit_flag.is_set():
        try:
            direction = direction_queue.get(timeout=1)
            if direction == "LEFT":
                print("Turn Left")
                GPIO.output(DIG1, GPIO.HIGH)
                GPIO.output(DIG2, GPIO.HIGH)
                p1.start(30)
                p2.start(70)
            elif direction == "RIGHT":
                print("Turn Right")
                GPIO.output(DIG1, GPIO.HIGH)
                GPIO.output(DIG2, GPIO.HIGH)
                p1.start(70)
                p2.start(30)
            elif direction == "STRAIGHT":
                print("Go Straight")
                GPIO.output(DIG1, GPIO.HIGH)
                GPIO.output(DIG2, GPIO.HIGH)
                p1.start(50)
                p2.start(50)
            else:  # STOP
                print("Stop")
                p1.start(0)
                p2.start(0)
        except queue.Empty:
            pass
    
    # Clean up
    p1.stop()
    p2.stop()
    GPIO.cleanup()

# Start threads
camera_thread_instance = threading.Thread(target=camera_thread)
motor_thread_instance = threading.Thread(target=motor_control_thread)

try:
    camera_thread_instance.start()
    motor_thread_instance.start()

    # Wait for threads to finish
    camera_thread_instance.join()
    motor_thread_instance.join()
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    handle_exit(None, None)  # Ensure cleanup on unexpected errors
    `