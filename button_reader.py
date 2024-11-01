#!env python3

from enum import Enum

from pprint import pprint
from gpiozero import Button

from random import randrange

from signal import pause

import requests
import json

import subprocess
import os
import signal
import time
import sys
from functools import partial

# Add a property to Button
Button.was_held = False

MR_ROBOTO_COMMAND=['play', '-q', '/home/jgillis/robocalypse/audio/Mr. Roboto.mp3']
# THRILLER_COMMAND=['play', '-q', '/home/jgillis/robocalypse/audio/Thriller.mp3']
WALKING_COMMAND=['play', '-q', '/home/jgillis/robocalypse/audio/walking.mp3', 'tempo', '0.75', 'repeat', '10']
THINKING_COMMAND=['play', '-q', '/home/jgillis/robocalypse/audio/thinking.mp3', 'repeat']
UNMUTE_MIC_COMMAND=['amixer', '-q', '-c', '1', 'sset', 'Mic', 'on']
MUTE_MIC_COMMAND=['amixer', '-q', '-c', '1', 'sset', 'Mic', 'off']
TALKING_COMMAND=['play', '-q', '|rec -d gain 30 band 1.2k 1.5k highpass 20 compand .1,.2 -inf,-30.1,-inf,-30,-30 0 -90 .1 pitch -350 equalizer 100 50 12 equalizer 900 50 -46 equalizer 2500 50 12 treble 0.6 phaser 0.6 0.66 3 0.6 2 -t bass -7 overdrive 10']
def FARTING_COMMAND():
    return ['play', '-q', f'/home/jgillis/robocalypse/audio/fart{randrange(1,5)}.ogg']
def MUSIC_COMMAND():
    files = ['Thriller.mp3', 'Ghostbusters.mp3']
    return ['play', '-q', f'/home/jgillis/robocalypse/audio/{files[randrange(1,2)]}']



GPIO_3=3
GPIO_4=4
GPIO_14=14
GPIO_15=15
GPIO_18=18
GPIO_17=17
GPIO_27=27

RED_BUTTON      = { 'color': 'red', 'gpio': GPIO_14 }
BLUE_BUTTON     = { 'color': 'blue', 'gpio': GPIO_18 }
R_WHITE_BUTTON  = { 'color': 'r_white', 'gpio': GPIO_17 }
GREEN_BUTTON    = { 'color': 'green', 'gpio': GPIO_27 }

YELLOW_BUTTON   = { 'color': 'yellow', 'gpio': GPIO_3 }
BLACK_BUTTON    = { 'color': 'black', 'gpio': GPIO_4 }
L_WHITE_BUTTON  = { 'color': 'l_white', 'gpio': GPIO_15 }

ALL_BUTTONS = [ RED_BUTTON, BLUE_BUTTON, R_WHITE_BUTTON,
                GREEN_BUTTON, YELLOW_BUTTON, BLACK_BUTTON,
                L_WHITE_BUTTON ]

class LightBoard:

    MAX_ATTEMPTS = 5
    FIELD_BREATHE = {"id":4,"fx":2,"sx":52,"ix": 128, "bri":255,
                     "pal":0,"col":[[255,0,0],[0,0,0],[85,0,255]]}
    FIELD_MUSIC = {"id":4,"fx":48,"sx":66,"ix":192,"bri":128,
                   "pal":5,"col":[[255,0,0],[255,166,0],[0,255,21]]}
    FIELD_WALKING = { "id": 4, "on": True, "bri": 255,
                      "col": [[255,0,0],[0,0,0],[85,0,255]],
                      "fx": 67, "sx": 58, "ix": 128, "pal": 61 }
    FIELD_THINKING = { "id": 4, "on": True, "bri": 255,
                       "col": [[255,0,0],[0,0,0],[85,0,255]],
                       "fx": 13, "sx": 205, "ix": 10, "pal": 10 }

    FIELD_TALKING = { "id": 4, "on": True, "bri": 255,
                      "fx": 111, "sx": 231, "ix": 168, "pal": 55 }

    HEADLIGHTS = { 'transition': 1, 'bri': 128,
                   'seg': [
                       {'id': 0, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 1, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 2, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 3, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 4, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 5, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 6, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 7, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 8, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 9, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]},
                       {'id': 11, 'fx': 0, 'sx': 128, 'ix': 128, 'bri': 128,
                        'col': [[255,255,255],[0,0,0],[85,0,255]]}],
                  }

    color_id_map = {
        'red': 0,
        'blue': 1,
        'r_white': 2,
        'green': 3,
        'l_white': 5,
        'black': 6,
        'yellow': 7
    }

    button_lights = [
        { 'id': 0, 'on': False, 'col': [[255,25,25]], 'fx': 0  },
        { 'id': 1, 'on': False, 'col': [[25,25,255]], 'fx': 0  },
        { 'id': 2, 'on': False, 'col': [[255,255,255]], 'fx': 0  },
        { 'id': 3, 'on': False, 'col': [[25,255,25]], 'fx': 0  },
        { 'id': 5, 'on': False, 'col': [[255,255,255]], 'fx': 0  },
        { 'id': 6, 'on': False, 'col': [[25,25,25]], 'fx': 0  },
        { 'id': 7, 'on': False, 'col': [[255,255,25]], 'fx': 0  }
    ]

    shoulder_lights = {
        'id': 8, 'on': True, 'col': [[255,170,0],[36,255,3],[0,0,0]],
        'fx': 62, 'sx': 128, 'ix': 128, 'pal': 0
    }

    nose_light = {
        "id": 9, "on": True, "col": [[255,0,0],[0,0,0],[0,0,0]],
        "fx": 100, "sx": 128, "ix": 128, "pal": 0
    }

    eye_bar = {
      "id": 10, "on": True, "col": [[255,25,25],[0,0,0],[0,0,0]],
      "fx": 92, "sx": 255, "ix": 255,
    }

    top_light = {
      "id": 11, "on": True, "col": [[255,25,25],[0,0,0],[0,0,0]],
      "fx": 24, "sx": 222, "ix": 128,
    }

    field  = {'id': 4, 'fx': 2, 'sx': 128, 'ix': 128,
              'bri':64, 'on': False, 'pal': 0,
              'col': [[255,0,0],[0,0,0],[85,0,255]]}


    def __init__(self, url_base: str, brightness: int = 16):
        self.url_base = url_base
        self.brightness = brightness
        headers = { 'Content-Type': 'application/json' }
        request_data = { 'ps': 7 }

        connect_count = 0
        initialized = False

        while connect_count < self.MAX_ATTEMPTS and not initialized:
            try:
                r = requests.post(self.url_base, json=request_data, headers=headers)

                if r.status_code == 200:
                    print(f'Initialized light board OK:  {r.status_code}')
                    initialized = True
                else:
                    print(f'Problem with light board init:  {r.status_code}')
            except ConnectionError:
                print(f'Error connecting to {self.url_base}.')
                connect_count += 1
                time.sleep(5)

        # Not being able to initialize is fatal
        if not initialized:
            print(f'Failed connecting to {self.url_base}')
            sys.exit(1)

    def color_switch(self, color: str, state: bool):
        """Switch the requested light to be on or off.  The other
        lights should be the opposite state."""
        print(f'color = {color} , id = {self.color_id_map[color]}')
        if color in self.color_id_map:
            for idx in range(0,7):
                if self.button_lights[idx]['id'] == self.color_id_map[color]:
                    self.button_lights[idx]['on'] = state
                else:
                    self.button_lights[idx]['on'] = not state
        # pprint(self.button_lights)

    def set_field(self, new_field):
        self.field = new_field

    def color_on(self, color: str):
        self.color_switch(color, True)

    def color_off(self, color: str):
        self.color_switch(color, False)

    def headlights(self):
        self.push_state(LightBoard.HEADLIGHTS)

    def default_head(self):
        request_data = { "transition": 1,
                         'bri': self.brightness,
                         'seg': [ self.shoulder_lights,
                                  self.nose_light,
                                  self.eye_bar,
                                  self.top_light ] }

        self.push_state(request_data)

    def push_state(self, request_data: dict = {}):
        headers = { 'Content-Type': 'application/json' }
        if request_data == {}:
            request_data = { "transition": 1,
                             'bri': self.brightness,
                             "seg": self.button_lights + [ self.field ] }

        attempts = 0
        sent = False
        while attempts < self.MAX_ATTEMPTS and not sent:
            try:
                r = requests.post(self.url_base, json=request_data, headers=headers)

                if r.status_code != 200:
                    print(f'Error in POST {r.status_code}:  {r.text}')
                else:
                    sent = True
            except ConnectionError:
                attempts += 1
                time.sleep(1)

        if not sent:
            print('Not able to send light board update.')



class AudioState(Enum):
    STOPPED = 0
    WALKING = 1
    THINKING = 2
    MUSIC = 3
    TALKING = 6
    FARTING = 7

class Robocalypse:

    def __init__(self,
                 gpios: list[dict] = []):
        """Initialize the system.  gpios contains information for each
        button containing the color and GPIO pin."""
        self.subproc = None
        self.audio_state = AudioState.STOPPED

        self.buttons: dict[str, Button] = {}

        self.gpios = gpios
        self.init_buttons()

        self.headlights_on = False

        # The red button is the start button.  Wait for this press to
        # allow the WLED to boot up.  Once pressed, the rest of the
        # buttons are activated.
        self.buttons['red'].when_released = self.startup_button

    def startup_button(self):
        """Initialize the light board and set up the buttons."""
        self.light_board = LightBoard('http://192.168.199.2/json/state')

        # Activate all the buttons
        for button in self.buttons:
            # self.buttons[button].when_held = self.handle_button
            self.buttons[button].when_released = self.handle_button
            self.buttons[button].when_held = self.handle_held

    def init_buttons(self):
        """Initialize the buttons using GPIOs on the Raspberry Pi"""
        print('Initializing buttons:')
        for gpio in self.gpios:
            print(f' - Button for GPIO {gpio}')
            #new_button = Button(gpio['gpio'], pull_up=True,
            #                    hold_repeat=False, hold_time=0.125)
            new_button = Button(gpio['gpio'], pull_up=True, hold_time=2.0)
            # new_button.when_held = self.handle_button
            # new_button.when_released = self.released
            self.buttons[gpio['color']] = new_button
        print('Done.')

    def released(self, button: Button):
        print(f'Button.held_time = {button.held_time}')

    def handle_held(self, button: Button):
        button_info = list(filter(lambda x: x['gpio'] == button.pin.number,
                                  self.gpios))[0]

        self.buttons[button_info['color']].was_held = True


    def handle_button(self, button: Button):
        button_info = list(filter(lambda x: x['gpio'] == button.pin.number,
                                  self.gpios))[0]
        long_press = self.buttons[button_info['color']].was_held

        # print(f'\n+++ Received button press on GPIO {button_info["color"]} - {button_info["gpio"]}.')

        self.light_board.color_on(button_info['color'])
        self.light_board.push_state()

        if button_info["color"] == "red":
            self.handle_red_button()
        elif button_info["color"] == 'blue':
            self.handle_blue_button()
        elif button_info["color"] == 'r_white':
            self.handle_r_white_button()
        elif button_info["color"] == 'l_white':
            if long_press:
                self.headlights()
            else:
                self.handle_l_white_button()
        elif button_info["color"] == 'green':
            self.handle_green_button()
        elif button_info["color"] == 'black':
            self.handle_black_button()
        elif button_info["color"] == 'yellow':
            self.handle_yellow_button()



    def go(self):
        try:
            while True:
                time.sleep(1)
                print('.', end='')
                sys.stdout.flush()
        except KeyboardInterrupt:
            print('\nExiting')
            sys.exit(0)

    def check_process(self) -> AudioState:
        """Check the status of the command and update the audio state"""
        if self.subproc is not None and self.subproc.poll() is not None:
            self.audio_state = AudioState.STOPPED

        return self.audio_state

    def start_process(self, command: list[str]):
        """Launch the process specified by command and store the
        popen information in subproc."""
        self.subproc = subprocess.Popen(command,
                                        stdin=subprocess.PIPE,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)

    def terminate_process(self):
        # Only terminate if the process is still running.  This is
        # determined by poll()ing to see if a return value is present.
        if self.subproc.poll() is None:
            # Just calling terminate on the process didn't work when
            # talking command was in use.  This just caused the top
            # level play command to become a zombie and the rec
            # process was still going.  Sending a CTRL-C to the
            # process via stdin seems to fix that.
            self.subproc.stdin.write('\x03'.encode())
            self.subproc.stdin.flush()
            self.subproc.terminate()
            self.subproc.wait()
            # print('Done')

        subprocess.run(MUTE_MIC_COMMAND)

        self.subproc = None

    def handle_red_button(self):
        """Stop all audio and reset the field to 'breathe'"""
        # field_config = {"id":4,"fx":2,"sx":52,"ix": 128, "bri":255,
        #                 "pal":0,"col":[[255,0,0],[0,0,0],[85,0,255]]}
        self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()
        self.light_board.default_head()

        if ( self.check_process() != AudioState.STOPPED and
             self.subproc is not None ):
            self.terminate_process()
            self.audio_state = AudioState.STOPPED

    def handle_blue_button(self):
        print('Blue button')
        started = self.start_or_stop(AudioState.MUSIC, MR_ROBOTO_COMMAND)

        # field_config = {"id":4,"fx":48,"sx":66,"ix":192,"bri":128,
        #                 "pal":5,"col":[[255,0,0],[255,166,0],[0,255,21]]}
        if started:
            self.light_board.set_field(LightBoard.FIELD_MUSIC)
        else:
            self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()

    def handle_yellow_button(self):
        print('Yellow button')
        started = self.start_or_stop(AudioState.TALKING, TALKING_COMMAND)
        if started:
            self.light_board.set_field(LightBoard.FIELD_TALKING)
        else:
            self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()


    def handle_black_button(self):
        print('Black button')
        self.start_or_stop(AudioState.FARTING, FARTING_COMMAND())

    def handle_r_white_button(self):
        """Play the walking sound on a loop."""
        print('R White Button')
        started = self.start_or_stop(AudioState.WALKING, WALKING_COMMAND)
        if started:
            self.light_board.set_field(LightBoard.FIELD_WALKING)
        else:
            self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()

    def handle_l_white_button(self):
        print('L White Button')
        started = self.start_or_stop(AudioState.THINKING, THINKING_COMMAND)
        if started:
            self.light_board.set_field(LightBoard.FIELD_THINKING)
        else:
            self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()

    def handle_green_button(self):
        print('Green Button')
        started = self.start_or_stop(AudioState.MUSIC, MUSIC_COMMAND())

        if started:
            self.light_board.set_field(LightBoard.FIELD_MUSIC)
        else:
            self.light_board.set_field(LightBoard.FIELD_BREATHE)
        self.light_board.push_state()

    def headlights(self):
        """It's dark outside and it's hard to see.  Turn on some light."""
        if self.headlights_on:
            self.headlights_on = False
            self.handle_red_button()
        else:
            self.headlights_on = True
            self.light_board.headlights()

    def start_or_stop(self, action: AudioState, command: list[str]) -> bool:
        should_start = True

        # Terminate the running process if one is running
        if ( self.check_process() != AudioState.STOPPED and
             self.subproc is not None ):
            if self.audio_state == action:
                should_start = False
            self.terminate_process()
            self.audio_state = AudioState.STOPPED
        if should_start:
            self.audio_state = action
            self.start_process(command)

        return should_start


def main():

    robo = Robocalypse(gpios = ALL_BUTTONS)

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
