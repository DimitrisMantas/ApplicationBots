"""This is a basic bot for most online typing speed tests, as well as standalone CPM and WPM measurment tools."""
"""Copyright 2021 Dimitris Mantas"""


import time

import keyboard
import numpy as np

from PIL import ImageGrab
from PIL import ImageOps

import pytesseract


# This program requires Tesseract, an open-source OCR engine, which was originally developed by Hewlett-Packard and is now maintained by Google [1].

# INSTALLATION INSTRUCTIONS

# 1. Install the latest version of Tesseract for Microsoft Windows [2].
# 2. Install the Tesseract wrapper for Python [3].
# 3. Note the location of the Tesseract executable file.

# [1]: https://en.wikipedia.org/wiki/Tesseract_(software)
# [2]: https://github.com/UB-Mannheim/tesseract/wiki
# [3]: https://pypi.org/project/pytesseract/


# Copy and paste the location of the Tesseract executable file here.
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# This is a hyperlink to the very first typing test, which shows up on Google. (26/02/2021)
# https://www.typingtest.com/


# This line is for debugging purposes.
# Print the screen coordinates and corresponding the pixel RGB values with respect to the current mouse position. 
# pyautogui.displayMousePosition()


# Register the coordinates of the maximum area bounding box, which contains the very first single line of text.
FIRST_BOUNDING_BOX = (1150, 320, 1800, 355) # (Top Left Corner, Bottom Right Corner)


# Register the vertical screen distance between two consecutive new lines of text in pixels.
DY = 100


# Register the bounding boxes for the first, as well as the second lines of text as a tuple of said tuples.
BOUNDING_BOXES = (FIRST_BOUNDING_BOX,(FIRST_BOUNDING_BOX[0], FIRST_BOUNDING_BOX[1] + DY, FIRST_BOUNDING_BOX[2], FIRST_BOUNDING_BOX[3] + DY))


# Register a program runtime interrupt key, so that the the infinite loop below can be stopped.
KEYBOARD_INTERRUPT = "C"


def ocr(image):
    """Perform OCR on a NumPy array, which encodes a PIL image."""
    # Any image manipulation must performed below this line. Color profile assignment is meant to be performed outside this function block.


    string = pytesseract.image_to_string(image)

    # The last character in the resulting OCR string is a special return character, which must be ignored.
    # Also, a single space must be registered at the end of each word.
    return string[:-2] + " " 


def write(string):
    """Write a string of characters by simulating the keyboard."""
    for i in range(len(string)):
        # Spaces between consecutive characters are normally ignored.
        if string[i] == " ":
            keyboard.press_and_release("space")
        else:
            keyboard.write(string[i])


def main(bounding_box):
    """This is the entry point of the program."""
    # Grab the required screenshot and convert its color mode from RGB to B&W.
    screenshot = ImageOps.grayscale(ImageGrab.grab(bbox=bounding_box))

    # This line is meant for debugging purposes only.
    # Print said screenshot to a temporary PNG image.
    # screenshot.show()

    # Encode the required screenshot into a NumPy array, perform OCR on it and write the resulting string of characters.
    write(ocr(np.array(screenshot)))


if __name__ == "__main__":
    # Allow some buffer time in order to bring the game screen out of the current background.
    time.sleep(3)

    # The very first bounding box placed must be placed where it should, while every other one must be placed DY below. 
    main(BOUNDING_BOXES[0])

    while not keyboard.is_pressed(KEYBOARD_INTERRUPT):
        # This line is for debugging purposes.
        # Start measuring the program runtime.
        # runtime = time.time()

        # Wait for the next line of text to be placed where it should.
        time.sleep(0.25)

        main(BOUNDING_BOXES[1])

        # These lines are for debugging purposes.
        # Compute the runtime of each loop.
        # runtime = time.time() - runtime
        # print("This loop took {0} seconds. The application is being run at {1} FPS.".format(runtime, runtime ** -1))
