"""
 This file is part of the scrabble-scraper distribution (https://github.com/scrabscrap/scrabble-scraper)
 Copyright (c) 2020 Rainer Rohloff.
 
 This program is free software: you can redistribute it and/or modify  
 it under the terms of the GNU General Public License as published by  
 the Free Software Foundation, version 3.

 This program is distributed in the hope that it will be useful, but 
 WITHOUT ANY WARRANTY; without even the implied warranty of 
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
 General Public License for more details.

 You should have received a copy of the GNU General Public License 
 along with this program. If not, see <http://www.gnu.org/licenses/>.
"""

import cv2
from gpiozero import Button
try:
    import RPi.GPIO
except:
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device
    Device.pin_factory = MockFactory()

from action import PLAYER1, PLAYER2, PAUSE, DOUBT, RESET, QUIT, CONFIG
from config import SIMULATE, KEYBOARD

# GROUND - pin 39
BLUE_SWITCH = 21    # GPIO21 - pin 40 - Schalter Blau
GREEN_SWITCH = 20   # GPIO20 - pin 38 - Schalter Grün
YELLOW_SWITCH = 16  # GPIO16 - pin 36 - Schalter Gelb
RED_SWITCH = 12     # GPIO12 - pin 32 - Schalter Rot
RESET_SWITCH = 4    # GPIO4 - pin 7 - Schalter Reset
REBOOT_SWITCH = 17  # GPI17 - pin 11 - Schalter Reboot
CONFIG_SWITCH = 27  # GPIO27 - pin 13 - Schalter Config

class EventButton:
    event = None

    def __init__(self):
        self.green = Button(GREEN_SWITCH)
        self.green.when_pressed = self.green_button_state
        self.yellow = Button(YELLOW_SWITCH)
        self.yellow.when_pressed = self.yellow_button_state
        self.blue = Button(BLUE_SWITCH)
        self.blue.when_pressed = self.blue_button_state
        self.red = Button(RED_SWITCH)
        self.red.when_pressed = self.red_button_state
        self.reset = Button(RESET_SWITCH, hold_time=3)
        self.reset.when_held = self.reset_button_state
        self.reboot = Button(REBOOT_SWITCH, hold_time=3)
        self.reboot.when_held = self.reboot_button_state
        self.config = Button(CONFIG_SWITCH, hold_time=3)
        self.config.when_held = self.config_button_state

    def green_button_state(self):
        self.event = PLAYER1

    def yellow_button_state(self):
        self.event = PAUSE

    def blue_button_state(self):
        self.event = DOUBT

    def red_button_state(self):
        self.event = PLAYER2

    def reset_button_state(self):
        self.event = RESET

    def reboot_button_state(self):
        self.event = QUIT

    def config_button_state(self):
        self.event = CONFIG

    def wait(self):
        result = self.event
        self.event = None
        return result


class EventKeyboard:

    def wait(self):
        key = cv2.waitKey(1 if not SIMULATE else 0) & 0xff

        if (key == 27) or (key == ord('q')):
            return QUIT
        if key == ord('1'):
            return PLAYER1
        if key == ord('2'):
            return PLAYER2
        if key == ord('p'):
            return PAUSE
        if key == ord('d'):
            return DOUBT
        if key == ord('r'):
            return RESET
        if key == ord('c'):
            return CONFIG
        return None


class Event:
    def __init__(self):
        self.keyboard_wait = None
        if KEYBOARD:
            keyboard = EventKeyboard()
            self.keyboard_wait = keyboard.wait
        button = EventButton()
        self.button_wait = button.wait

    def wait(self):
        result = None
        result = self.button_wait()
        if result is None and self.keyboard_wait:
            result = self.keyboard_wait()
        return result
