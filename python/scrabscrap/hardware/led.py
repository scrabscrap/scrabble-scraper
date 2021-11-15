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

from gpiozero import LED
try:
    import RPi.GPIO
except:
    from gpiozero.pins.mock import MockFactory
    from gpiozero import Device
    Device.pin_factory = MockFactory()

# GROUND - pin 39
BLUE_GPIO = 26  # GPIO26 - pin 37 - led Blau
GREEN_GPIO = 19  # GPIO19 - pin 35 - led Grün
YELLOW_GPIO = 13  # GPIO13 - pin 33 - led Gelb
RED_GPIO = 6  # GPIO6  - pin 31 - led Rot

green = LED(GREEN_GPIO)
yellow = LED(YELLOW_GPIO)
blue = LED(BLUE_GPIO)
red = LED(RED_GPIO)


def green_led():
    green.on()


def yellow_led():
    yellow.on()


def blue_led():
    blue.on()


def red_led():
    red.on()


def led_off():
    green.off()
    yellow.off()
    blue.off()
    red.off()


def yellow_blink():
    yellow.blink()


def blue_blink():
    blue.blink()


def red_blink():
    red.blink()


def green_blink():
    green.blink()
