import cv2
import numpy as np

def nothing(x):
    pass

# Initialize Camera
cap = cv2.VideoCapture(0)
cap.set(3, 640) # resize for Celeron performance
cap.set(4, 480)

# Create a window for sliders
cv2.namedWindow("Calibration Tool")

# Create 6 sliders to adjust Hue, Saturation, and Value (Min and Max)
# Initial values set to detect "Green" approx.
cv2.createTrackbar("H Min", "Calibration Tool", 35, 179, nothing)
cv2.createTrackbar("S Min", "Calibration Tool", 100, 255, nothing)
cv2.createTrackbar("V Min", "Calibration Tool", 100, 255, nothing)

cv2.createTrackbar("H Max", "Calibration Tool", 85, 179, nothing)
cv2.createTrackbar("S Max", "Calibration Tool", 255, 255, nothing)
cv2.createTrackbar("V Max", "Calibration Tool", 255, 255, nothing)

print("Adjust the sliders until your background turns WHITE and you turn BLACK.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    
    # Convert to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Read current slider positions
    h_min = cv2.getTrackbarPos("H Min", "Calibration Tool")
    s_min = cv2.getTrackbarPos("S Min", "Calibration Tool")
    v_min = cv2.getTrackbarPos("V Min", "Calibration Tool")

    h_max = cv2.getTrackbarPos("H Max", "Calibration Tool")
    s_max = cv2.getTrackbarPos("S Max", "Calibration Tool")
    v_max = cv2.getTrackbarPos("V Max", "Calibration Tool")

    # Create the Lower and Upper arrays
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])

    # Create Mask
    mask = cv2.inRange(hsv, lower, upper)

    # Show the result
    # White areas = What will be removed (Background)
    # Black areas = What will be kept (You)
    cv2.imshow("Calibration Tool", mask)
    cv2.imshow("Original", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()