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
import logging
from gpiozero import Button
from threading import Event
try:
    import RPi.GPIO
except ImportError:
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


class ButtonEvent:
    event = None

    def __init__(self, end_of_wait: Event):
        self.end_of_wait = end_of_wait
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
        self.end_of_wait.set()

    def yellow_button_state(self):
        self.event = PAUSE
        self.end_of_wait.set()

    def blue_button_state(self):
        self.event = DOUBT
        self.end_of_wait.set()

    def red_button_state(self):
        self.event = PLAYER2
        self.end_of_wait.set()

    def reset_button_state(self):
        self.event = RESET
        self.end_of_wait.set()

    def reboot_button_state(self):
        self.event = QUIT
        self.end_of_wait.set()

    def config_button_state(self):
        self.event = CONFIG
        self.end_of_wait.set()

    def wait(self, end_of_wait: Event):
        self.event = None
        self.end_of_wait = end_of_wait


class KeyboardEvent:
    event = None

    # noinspection PyMethodMayBeStatic
    def wait(self, end_of_wait: Event):
        self.event = None
        key = cv2.waitKey(1 if not SIMULATE else 0) & 0xff

        self.event = None
        if (key == 27) or (key == ord('q')):
            self.event = QUIT
        if key == ord('1'):
            self.event = PLAYER1
        if key == ord('2'):
            self.event = PLAYER2
        if key == ord('p'):
            self.event = PAUSE
        if key == ord('d'):
            self.event = DOUBT
        if key == ord('r'):
            self.event = RESET
        if key == ord('c'):
            self.event = CONFIG
        end_of_wait.set()


class ActionEvent:
    def __init__(self, end_of_wait: Event):
        self.button = ButtonEvent(end_of_wait)
        if KEYBOARD:
            self.keyboard = KeyboardEvent()

    def wait(self, end_of_wait: Event):
        self.button.wait(end_of_wait)
        if KEYBOARD:
            self.keyboard.wait(end_of_wait)

    def get_event(self):
        # Button hat Priorität
        if self.button.event is not None:
            logging.debug("event: Button pressed {}".format(self.button.event))
            return self.button.event
        if KEYBOARD and self.keyboard.event is not None:
            logging.debug("event: Keyboard pressed {}".format(self.keyboard.event))
            return self.keyboard.event
        return None
