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


# Set the colors on which the left mouse button will be clicked and released.
LEFT_MOUSE_HOLD_ON_RGB_VALUES = [0, 0, 0]
LEFT_MOUSE_RELEASE_ON_RGB_VALUES = [0, 150, 225]


# Set the precision for comparing two RGB values to each other.
PRECISION = 75


# Set the programm runtime interupt button.
KEYBOARD_INTERRUPT = "C"


# Set the screen position of the midpoint of each column.
# The Y-coordinates need to be set near the horizontal white line at the bottom, but not on it.
COLUMN_MIDPOINTS_X_CORRDINATES = [720, 860, 1000, 1140]
COLUMN_MIDPOINTS_Y_CORRDINATES = 540
COLUMN_MIDPOINTS = [COLUMN_MIDPOINTS_X_CORRDINATES[0], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[1], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[2], COLUMN_MIDPOINTS_Y_CORRDINATES, COLUMN_MIDPOINTS_X_CORRDINATES[3], COLUMN_MIDPOINTS_Y_CORRDINATES]


def get_rgb_values(x, y):
    """Get the RBG values of the pixels, which are located some screen position."""
    return pyautogui.pixel(x, y)


def check_rgb_match(sample_rgb, target_rgb, precision):
    """Check if some sample RGB values is the same or "close enough" to some target RGB values."""
    if abs(sum(sample_rgb) - sum(target_rgb)) <= precision:
        return True
    else:
        return False


def left_mouse_hold(x, y):
    """Register and hold a left mouse click at some screen position."""
    # Set the mouse cursor screen position.
    win32api.SetCursorPos((x, y))

    # The next mouse event needs to be generated dx = dy = 0 from the current cursor position.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def left_mouse_release():
    """Release an active left mouse click."""
    # This can be incorporated into the above function, but it is good to keep the separate.
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def main(column_midpoints, left_mouse_hold_on_rgb_values, left_mouse_release_on_rgb_values, precision, keyboard_interrupt):
    """This is the entry point of the program."""
    while not keyboard.is_pressed(keyboard_interrupt):

        # This line is for debugging purposes.
        start_measuring_runtime = time.time()

        # PyAutoGUI can throw an OSError for some reason. This block is for debugging purposes.
        try:
            column_1 = check_rgb_match(get_rgb_values(column_midpoints[0], column_midpoints[1]), left_mouse_hold_on_rgb_values, precision)
            column_2 = check_rgb_match(get_rgb_values(column_midpoints[2], column_midpoints[3]), left_mouse_hold_on_rgb_values, precision)
            column_3 = check_rgb_match(get_rgb_values(column_midpoints[4], column_midpoints[5]), left_mouse_hold_on_rgb_values, precision)
            column_4 = check_rgb_match(get_rgb_values(column_midpoints[6], column_midpoints[7]), left_mouse_hold_on_rgb_values, precision)

            column_12 = column_1 and column_2
            column_13 = column_1 and column_3
            column_14 = column_1 and column_4
            column_23 = column_2 and column_3
            column_24 = column_2 and column_4
            column_34 = column_3 and column_4

            # Case 1: The column doesn't have a gradient.
            if column_1 and not column_2 and not column_3 and not column_4:
                left_mouse_hold(column_midpoints[0], column_midpoints[1])
                left_mouse_release()
            elif column_2 and not column_3 and not column_4 and not column_1:
                left_mouse_hold(column_midpoints[2], column_midpoints[3])
                left_mouse_release()
            elif column_3 and not column_4 and not column_1 and not column_2:
                left_mouse_hold(column_midpoints[4], column_midpoints[5])
                left_mouse_release()
            elif column_4 and not column_1 and not column_2 and not column_3:
                left_mouse_hold(column_midpoints[6], column_midpoints[7])
                left_mouse_release()
            elif column_12:
                left_mouse_hold(column_midpoints[0], column_midpoints[1])
                left_mouse_release()

                left_mouse_hold(column_midpoints[2], column_midpoints[3])
                left_mouse_release()
            elif column_13:
                left_mouse_hold(column_midpoints[0], column_midpoints[1])
                left_mouse_release()

                left_mouse_hold(column_midpoints[4], column_midpoints[5])
                left_mouse_release()
            elif column_14:
                left_mouse_hold(column_midpoints[0], column_midpoints[1])
                left_mouse_release()

                left_mouse_hold(column_midpoints[6], column_midpoints[7])
                left_mouse_release()
            elif column_23:
                left_mouse_hold(column_midpoints[2], column_midpoints[3])
                left_mouse_release()

                left_mouse_hold(column_midpoints[4], column_midpoints[5])
                left_mouse_release()
            elif column_24:
                left_mouse_hold(column_midpoints[2], column_midpoints[3])
                left_mouse_release()

                left_mouse_hold(column_midpoints[6], column_midpoints[7])
                left_mouse_release()
            elif column_34:
                left_mouse_hold(column_midpoints[4], column_midpoints[5])
                left_mouse_release()

                left_mouse_hold(column_midpoints[6], column_midpoints[7])
                left_mouse_release()
        except OSError:
            pass

        # This line is for debugging purposes.
        # print("This loop took {} seconds.".format(time.time() - start_measuring_runtime))


if __name__ == "__main__":
    """Run the program."""
    # This helps bring the game screen out of the background.
    time.sleep(5)

    main(COLUMN_MIDPOINTS, LEFT_MOUSE_HOLD_ON_RGB_VALUES, LEFT_MOUSE_RELEASE_ON_RGB_VALUES, PRECISION, KEYBOARD_INTERRUPT)
