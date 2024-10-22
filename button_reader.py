#!env python3

from gpiozero import Button

from signal import pause

import subprocess
import time
import sys
from functools import partial

MR_ROBOTO_COMMAND=['play', '-q', '/home/jgillis/audio/Mr. Roboto.mp3']
ROBOT_VOICE_COMMAND=['play', '-q', '|rec ']
RED_BUTTON_GPIO=18
YELLOW_BUTTON_GPIO=24
BLACK_BUTTON_GPIO=11

class Robocalypse:

    def __init__(self,
                 red_button_gpio: int = 18,
                 yellow_button_gpio: int = 24):
        self.red_button_gpio = red_button_gpio
        self.yellow_button_gpio = yellow_button_gpio
        self.subproc = None
        self.buttons: dict[str, Button] = {}

        self.init_red_button()
        self.init_yellow_button()

    def init_red_button(self):
        print('Initializing the red button')
        self.buttons['red'] = Button(self.red_button_gpio, pull_up=True,
                                     hold_repeat=False, hold_time=0.25)
        self.buttons['red'].when_held = self.handle_red_button
        print('Done init')

    def init_yellow_button(self):
        print('Initializing the yellow button')
        self.buttons['yellow'] = Button(self.yellow_button_gpio, pull_up=True,
                                     hold_repeat=False, hold_time=0.25)
        self.buttons['yellow'].when_held = self.handle_yellow_button
        print('Done init')

    def go(self):
        while True:
            time.sleep(1)
            print('.', end='')
            sys.stdout.flush()

    def start_process(self, command: list[str]):
        self.subproc = subprocess.Popen(command)

    def terminate_process(self):
        # Only terminate if the process is still running.  This is
        # determined by poll()ing to see if a return value is present.
        if self.subproc.poll() is None:
            self.subproc.terminate()
            self.subproc.wait()

        self.subproc = None

    def handle_red_button(self):
        print('Button!')

        # Terminate the running process if one is running
        if self.subproc is not None:
            self.terminate_process()
        else:
            self.start_process(MR_ROBOTO_COMMAND)

    def handle_yellow_button(self):
        print('Yellow Button!')

        # Terminate the running process if one is running
        if self.subproc is not None:
            self.terminate_process()
        else:
            self.start_process(MR_ROBOTO_COMMAND)

def main():
    robo = Robocalypse(red_button_gpio = RED_BUTTON_GPIO,
                       yellow_button_gpio = YELLOW_BUTTON_GPIO)

    robo.go()
    # # Create the a button object with a pull up resistor in place.
    # # Hold time is 0.25 seconds
    # red_button = Button(RED_BUTTON_GPIO, pull_up=True,
    #                     hold_repeat=False, hold_time=0.25)
    # red_button.when_held = handle_red_button

    # while True:
    #     time.sleep(1)
    #     print('.', end='')
    #     sys.stdout.flush()

    return


if __name__ == '__main__':
    main()
