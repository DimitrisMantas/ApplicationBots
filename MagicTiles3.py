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


# Register the colors on which a mouse event will be generated.
LEFT_MOUSE_CLICK_ON_RGB_VALUES = [0, 0, 0]


# Register the precision for comparing two RGB values to each other.
PRECISION = 100 # Out of 3 * 255 = 765.


# Register the programm runtime interupt button.
KEYBOARD_INTERRUPT = "C"


# Register the screen position of the midpoint of each column in pixels.
COLUMN_MIDPOINTS = [720, 540, 860, 540, 1000, 540, 1140, 540] # [Column 1, Column 2, Column 3, Column 4]


def check_rgb_match(sample_rgb, target_rgb, precision):
    """Check if some sample RGB values is the same or "close enough" to some target RGB values."""
    return abs(sum(sample_rgb) - sum(target_rgb)) <= precision


def left_mouse_click(x, y):
    """Register and hold a left mouse click at some screen position."""
    # Register a guard clause, because we don't want to register a mouse event when the value of x is equal is False.
    if not x: return

    # Register the mouse cursor screen position.
    win32api.SetCursorPos((x, y))

    # The next mouse event needs to be generated dx = dy = 0 px. from the current cursor position.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main(column_midpoints, left_mouse_click_on_rgb_values, precision, keyboard_interrupt):
    """This is the entry point of the program."""
    # Sometimes the next mouse event needs to be generated dy > 0 px. from the current cursor position in order to account for the song speed.
    dy = 100

    while not keyboard.is_pressed(keyboard_interrupt):
        # This line is for debugging purposes.
        # runtime = time.time()

        # PyAutoGUI can throw an OSError for some reason. This block is for debugging purposes.
        try:
            left_mouse_click(column_midpoints[0] * check_rgb_match(pyautogui.pixel(column_midpoints[0], column_midpoints[1]), left_mouse_click_on_rgb_values, precision), column_midpoints[1] + dy)
            left_mouse_click(column_midpoints[2] * check_rgb_match(pyautogui.pixel(column_midpoints[2], column_midpoints[3]), left_mouse_click_on_rgb_values, precision), column_midpoints[3] + dy)
            left_mouse_click(column_midpoints[4] * check_rgb_match(pyautogui.pixel(column_midpoints[4], column_midpoints[5]), left_mouse_click_on_rgb_values, precision), column_midpoints[5] + dy)
            left_mouse_click(column_midpoints[6] * check_rgb_match(pyautogui.pixel(column_midpoints[6], column_midpoints[7]), left_mouse_click_on_rgb_values, precision), column_midpoints[7] + dy)
        except OSError:
            pass

        # These lines are for debugging purposes.
        # runtime = time.time() - runtime
        # print("This loop took {0} seconds. The game is being run at {1} FPS.".format(runtime, runtime ** -1))


if __name__ == "__main__":
    """Run the program."""
    # This helps bring the game screen out of the background.
    time.sleep(3)

    main(COLUMN_MIDPOINTS, LEFT_MOUSE_CLICK_ON_RGB_VALUES, PRECISION, KEYBOARD_INTERRUPT)
