""" Using Mouse click to crop a region and perform OCR and read date code on it."""
import re
import cv2
import argparse
import pytesseract
from pytesseract import Output
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
frame = cv2.imread(args["image"], 0)
frame_copy = frame.copy()

# Initializing x1, y1, x2, y2
(x1, y1) = (0, 0)
(x2, y2) = (0, 0)
# Keep looping until the 'q' key is pressed
while True:
    # Display the image and wait for a keypress
    # frame = cv2.resize(frame, (1920, 1080))
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
image_roi = frame[y1:y2, x1:x2]
# data =  pytesseract.image_to_string(image_roi, config='--oem 3 --psm 6 tessedit_char_whitelist=0123456789 outputbase digits')
data = pytesseract.image_to_data(image_roi, output_type=Output.DICT)
# print(data.keys())
print(data['text'])
# print(data['conf'])
n_boxes = len(data['text'])

# date_pattern = '^(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[012])/(19|20)\d\d$'
date_pattern = '^([0-9]{4})$'
for i in range(n_boxes):
    try:
        data['text'][i]
        data_to_check = data['text'][i]
        # print(data_to_check)
        if re.match(date_pattern, data_to_check):
            print(data_to_check)

    except:
        pass
        # else:
        # print('No date found')

cv2.imshow("Selected Region of Interest - Press any key to proceed", image_roi) 
cv2.waitKey(0)

