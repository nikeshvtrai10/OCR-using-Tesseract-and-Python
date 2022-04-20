""" Using Mouse click to crop a region and perform OCR and read date code on it."""
import re
import cv2
import argparse
import pytesseract
# Initializing the list for storing the coordinates
ref_coord = []

def click_and_crop(event, x, y, flags, param):
    global ref_coord
    if event == cv2.EVENT_LBUTTONDOWN:
        ref_coord = [(x, y)]
        print(ref_coord)
    elif event == cv2.EVENT_LBUTTONUP:
        ref_coord.append((x, y))

# Add argument parser to read the image path
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

# Setup window name and mouse callback function
cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

# Read the image
frame = cv2.imread(args["image"])

# Initializing x1, y1, x2, y2
(x1, y1) = (0, 0)
(x2, y2) = (0, 0)
# Keep looping until the 'q' key is pressed
while True:
    # Display the image and wait for a keypress
    cv2.imshow("image", frame)
    key = cv2.waitKey(1) & 0xFF

    # If the 'r' key is pressed, reset the cropping region
    if key == ord("r"):
        ref_coord = []
    # If the 'q' key is pressed, break from the loop
    elif key == ord("q"):
        break
    
    if len(ref_coord)==2:
        (x1, y1) = (ref_coord[0][0], ref_coord[0][1])
        (x2, y2) = (ref_coord[1][0], ref_coord[1][1])
        break
# Closing all open windows
cv2.destroyAllWindows()
ocr_img = frame[y1:y2, x1:x2]
data =  pytesseract.image_to_string(ocr_img, config='--oem 3 --psm 6 tessedit_char_whitelist=0123456789 outputbase digits')
# data = re.sub('[^A-Za-z0-9-]+', '', data)
print(data)

