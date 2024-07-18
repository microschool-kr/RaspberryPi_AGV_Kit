import cv2
import numpy as np

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

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame, center_x = detect_line(frame)
    
    if center_x is not None:
        # Determine direction based on the center of the line
        if center_x < frame.shape[1] / 3:
            print("Turn Left")
        elif center_x > 2 * frame.shape[1] / 3:
            print("Turn Right")
        else:
            print("Go Straight")
    
    cv2.imshow('Line Tracer', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
