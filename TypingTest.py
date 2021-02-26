"""This is a basic bot for most online CPM and WPM measurement tools."""
"""Copyright 2021 Dimitris Mantas"""


import time

import keyboard
import numpy as np

from PIL import ImageGrab
from PIL import ImageOps

import pytesseract


# This program requires Tesseract, an open-source OCR program, which was developed by Hewlett-Packard and is now maintained by Google [1].

# INSTALLATION INSTRUCTIONS

# 1. Install the latest stable version of Tesseract [2].
# 2. Install the Tesseract wrapper for Python [3].
# 3. 

# [1]: https://en.wikipedia.org/wiki/Tesseract_(software)
# [2]: https://github.com/UB-Mannheim/tesseract/wiki
# [3]: https://pypi.org/project/pytesseract/


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" # Copy and paste the location of the Tesseract excecutable file here.


# This is a hyperlink to the very first measurement tool, which shows up on Google. (26/02/2021)
# https://www.typingtest.com/


# This line is for debugging purposes.
# Print the screen coordinates and corresponding the pixel RGB values with respect to the current mouse position. 
# pyautogui.displayMousePosition()


# Register the dimensions of a bounding boxm which surely contains a single line of text.
BOUNDING_BOX = (1150, 320, 1800, 355) # (Top Left Corner, Bottom Right Corner)

# Register the vertical distance between two consecutive new lines of text in pixels.
BOUNDING_BOX_OFFSET = 100


BOUNDING_BOXES = {1: BOUNDING_BOX,
                  2: (BOUNDING_BOX[0], BOUNDING_BOX[1] + BOUNDING_BOX_OFFSET, BOUNDING_BOX[2], BOUNDING_BOX[3] + BOUNDING_BOX_OFFSET)}


# Register a program runtime interrupt key, so that the the infinite loop below can be stopped.
KEYBOARD_INTERRUPT = "C"


def grab_screenshot(bounding_box):
    # Grab a screenshot of a specific area of the screen and store it in memory as a PIL image.
    return ImageGrab.grab(bbox=bounding_box)


def ocr(image):
    """Perform OCR on a NumPy array, which encodes a B&W PIL image."""
    # Any image manipulation must implemented below this line.


    ocr_string = pytesseract.image_to_string(image)

    return ocr_string[:-2] + " " # The last value in the OCR string is a special return character, which must be ignored.


def write_ocr_string(ocr_string):
    """ """
    for i in range(len(ocr_string)):

        if ocr_string[i] == " ":
            keyboard.press_and_release("space")
        else:
            keyboard.write(ocr_string[i])


def main(bounding_boxes, keyboard_interrupt):
    """This is the entry point of the program."""
    #
    i = 1

    while not keyboard.is_pressed(keyboard_interrupt):
        # This line is for debugging purposes.
        # Start measuring the program runtime.
        # runtime = time.time()

        # The very first bounding box placed at its original location, while every second is placed dy down.
        if i == 1:
            bounding_box = bounding_boxes[1]
        else:
            # Wait for the next line of text tp be placed at the correct location.
            time.sleep(0.25)

            bounding_box = bounding_boxes[2]


        # Grab the required screenshot and reset its color mode from RGB to B&W.
        screenshot = ImageOps.grayscale(grab_screenshot(bounding_box))
        # This line is meant for debugging purposes only.
        # Display said screenshot as a PNG image.
        # screenshot.show()

        # Encode the corresponding PIL image data into a NumPy array.
        screenshot = np.array(screenshot)

        ocr_string = ocr(screenshot)

        write_ocr_string(ocr_string)

        i += 1
        
        # These lines are for debugging purposes.
        # Compute the runtime of each loop.
        # runtime = time.time() - runtime

        # print("This loop took {0} seconds. The application is being run at {1} FPS.".format(runtime, runtime ** -1))


if __name__ == "__main__":
    # Allow some buffer time in order to bring the game screen out of the current background.
    time.sleep(3)

    main(BOUNDING_BOXES, KEYBOARD_INTERRUPT)
