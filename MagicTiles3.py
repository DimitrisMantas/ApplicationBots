"""This is a basic bot for the Adroid game, Magic Tiles 3, but it also works with most of its clones with minimal modifications."""
"""Copyright 2021 Dimitris Mantas"""


import time

import keyboard
import pyautogui

import win32api
import win32con


# This is a hyperlink to an online clone of Magic Tiles 3.
# https://poki.com/en/g/piano-tiles-2


# This line is for debugging purposes.
# Print the screen coordinates and corresponding the pixel RGB values with respect to the current mouse position. 
# pyautogui.displayMousePosition()


# Register the RBG values on which a left mouse click must be generated.
LEFT_MOUSE_CLICK_ON_RGB_VALUES = (0, 0, 0)


# Register the precision for comparing two RGB values to one another.
PRECISION = 100 # Out of 3 * 255 = 765.

# Register the verical distance between the screen positions of the midpoint of each column and of said click in pixels.
# This can help account for the fact that movement speed of the interactive objects can be greater than the program runtime.
DY = 100

# Register a program runtime interrupt key, so that the the infinite loop below can be stopped.
KEYBOARD_INTERRUPT = "C"


# Register the screen position of said points in pixels.
COLUMN_MIDPOINTS = (720, 540, 860, 540, 1000, 540, 1140, 540) # (Column 1, Column 2, Column 3, Column 4)


def check_rgb_match(sample_rgb, target_rgb, precision):
    """Check if a triplet of some sample RGB values can be considered to be the same as a triplet of some target RGB values."""
    return abs(sum(sample_rgb) - sum(target_rgb)) <= precision


def left_mouse_click(x, y):
    """Register a left mouse click at a specific screen position."""
    # This guard clause makes sure that a click will be generated only when the value of the given x-coordinate is not equal to False.
    if not x: return

    # Move the mouse cursor to the appropriate screen position.
    win32api.SetCursorPos((x, y)) # This function input is a single tuple.

    # The click will be generated at said screen position, which is dx = dy = 0 pixels from the current cursor position.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main(column_midpoints, left_mouse_click_on_rgb_values, precision, dy, keyboard_interrupt):
    """This is the entry point of the program."""
    while not keyboard.is_pressed(keyboard_interrupt):
        # This line is for debugging purposes.
        # Start measuring the program runtime.
        # runtime = time.time()

        # PyAutoGUI can throw an OSError because of a currently unknown reason (26/02/2021).
        # This block is for debugging purposes.
        try:
            left_mouse_click(column_midpoints[0] * check_rgb_match(pyautogui.pixel(column_midpoints[0], column_midpoints[1]), left_mouse_click_on_rgb_values, precision), column_midpoints[1] + DY)
            left_mouse_click(column_midpoints[2] * check_rgb_match(pyautogui.pixel(column_midpoints[2], column_midpoints[3]), left_mouse_click_on_rgb_values, precision), column_midpoints[3] + DY)
            left_mouse_click(column_midpoints[4] * check_rgb_match(pyautogui.pixel(column_midpoints[4], column_midpoints[5]), left_mouse_click_on_rgb_values, precision), column_midpoints[5] + DY)
            left_mouse_click(column_midpoints[6] * check_rgb_match(pyautogui.pixel(column_midpoints[6], column_midpoints[7]), left_mouse_click_on_rgb_values, precision), column_midpoints[7] + DY)
        except OSError:
            pass

        # These lines are for debugging purposes.
        # Compute the runtime of each loop.
        # runtime = time.time() - runtime
        # print("This loop took {0} seconds. The game is being run at {1} FPS.".format(runtime, runtime ** -1))


if __name__ == "__main__":
    # Allow some buffer time in order to bring the game screen out of the current background.
    time.sleep(3)

    main(COLUMN_MIDPOINTS, LEFT_MOUSE_CLICK_ON_RGB_VALUES, PRECISION, DY, KEYBOARD_INTERRUPT)
