"""This is a bot for Magic Tiles 3 and most similar games."""
"""Copyright 2021 Dimitris Mantas"""

import time

import keyboard
import pyautogui

import win32api
import win32con


# This is a hyperlink to an online clone of the game.
# https://poki.com/en/g/piano-tiles-2


# This line is for debugging purposes.
# pyautogui.displayMousePosition()


# Register the colors on which the left mouse button will be clicked and released.
LEFT_MOUSE_HOLD_ON_RGB_VALUES = [0, 0, 0]


# Register the precision for comparing two RGB values to each other.
PRECISION = 100


# Register the programm runtime interupt button.
KEYBOARD_INTERRUPT = "C"


# Register the screen position of the midpoint of each column.
# The Y-coordinates need to be set near the horizontal white line at the bottom, but not on it.
COLUMN_MIDPOINTS_X_CORRDINATES = [720, 860, 1000, 1140]
COLUMN_MIDPOINTS_Y_CORRDINATES = 540

COLUMN_MIDPOINTS = [COLUMN_MIDPOINTS_X_CORRDINATES[0], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[1], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[2], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[3], COLUMN_MIDPOINTS_Y_CORRDINATES]


def get_rgb_values(x, y):
    """Get the RBG values of the px., which are located some screen position."""
    return pyautogui.pixel(x, y)


def check_rgb_match(sample_rgb, target_rgb, precision):
    """Check if some sample RGB values is the same or "close enough" to some target RGB values."""
    # Register the function return flag.
    return abs(sum(sample_rgb) - sum(target_rgb)) <= precision


def left_mouse_click(x, y):
    """Register and hold a left mouse click at some screen position."""

    # I'm gonna do what's called a pro-gamer move...
    if not x: return

    # Register the mouse cursor screen position.
    win32api.SetCursorPos((x, y))

    # The next mouse event needs to be generated dx = dy = 0 px. from the current cursor position.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main(column_midpoints, left_mouse_hold_on_rgb_values, precision, keyboard_interrupt):
    """This is the entry point of the program."""
    # Sometimes the next mouse event needs to be generated dy > 0 px. from the current cursor position in order to account for the song speed.
    dy = 100

    while not keyboard.is_pressed(keyboard_interrupt):
        # This line is for debugging purposes.
        # runtime = time.time()

        # PyAutoGUI can throw an OSError for some reason. This block is for debugging purposes.
        try:
            left_mouse_click(column_midpoints[0] * check_rgb_match(get_rgb_values(column_midpoints[0], column_midpoints[1]), left_mouse_hold_on_rgb_values, precision), column_midpoints[1] + dy)
            left_mouse_click(column_midpoints[2] * check_rgb_match(get_rgb_values(column_midpoints[2], column_midpoints[3]), left_mouse_hold_on_rgb_values, precision), column_midpoints[3] + dy)
            left_mouse_click(column_midpoints[4] * check_rgb_match(get_rgb_values(column_midpoints[4], column_midpoints[5]), left_mouse_hold_on_rgb_values, precision), column_midpoints[5] + dy)
            left_mouse_click(column_midpoints[6] * check_rgb_match(get_rgb_values(column_midpoints[6], column_midpoints[7]), left_mouse_hold_on_rgb_values, precision), column_midpoints[7] + dy)
        except OSError:
            pass

        # These lines are for debugging purposes.
        # runtime = time.time() - runtime
        # print("This loop took {0} seconds. The game is being run at {1} FPS.".format(runtime, runtime ** -1))


if __name__ == "__main__":
    """Run the program."""
    # This helps bring the game screen out of the background.
    time.sleep(3)

    main(COLUMN_MIDPOINTS, LEFT_MOUSE_HOLD_ON_RGB_VALUES, PRECISION, KEYBOARD_INTERRUPT)
