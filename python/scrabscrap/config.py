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

import configparser
import logging
import os

WORK_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../../work")

class Config:

    def __init__(self):
        self.settings = {}
        self.read_config()

    def read_config(self):
        try:
            _config = configparser.ConfigParser()
            with open(WORK_DIR + '/scrabble.ini', "r") as config_file:
                _config.read_file(config_file)
            for sect in _config.sections():
                self.settings[sect] = {}
                for opt in _config.options(sect):
                    self.settings[sect][opt] = eval(_config.get(sect, opt))
        except Exception as e:
            logging.exception("INI-Datei kann nicht gelesen werden " + str(e))

    def get(self, section, option, fallback=None):
        try:
            ret = self.settings[section][option]
        except (AttributeError, KeyError):
            ret = fallback
        return ret


config = Config()

SIMULATE = config.get('development', 'simulate', fallback=False)
SIMULATE_PATH = config.get('development', 'simulate_path')

MALUS_DOUBT = config.get('scrabble', 'malus_doubt', fallback=10)
MAX_TIME = config.get('scrabble', 'max_time', fallback=1800)
MIN_TIME = config.get('scrabble', 'min_time', fallback=-300)
DOUBT_TIMEOUT = config.get('scrabble', 'doubt_timeout', fallback=20)

SCREEN = SIMULATE or config.get('output', 'screen', fallback=False)

try:
    import wiringpi
    TM1637 = config.get('output', 'tm1637', fallback=True)
except ImportError:
    TM1637 = False

WRITE_WEB = config.get('output', 'web', fallback=True)
WEB_PATH = config.get('output', 'web_path', fallback=WORK_DIR + '/web/')
FTP = config.get('output', 'ftp', fallback=False)

KEYBOARD = SIMULATE or config.get('input', 'keyboard', fallback=True)

HOLD1 = config.get('button', 'hold1', fallback=4)
HOLD2 = config.get('button', 'hold2', fallback=8)

WARP = config.get('video', 'warp', fallback=True)
IM_WIDTH = config.get('video', 'size', fallback=1504)
IM_HEIGHT = config.get('video', 'size', fallback=1504)
FPS = config.get('video', 'fps', fallback=15)
ROTATE = config.get('video', 'rotate', fallback=False)
BOARD_LAYOUT = config.get('board', 'layout', fallback="classic")

CLK1 = config.get('tm1637', 'clk1', fallback=24)
DIO1 = config.get('tm1637', 'dio1', fallback=25)
CLK2 = config.get('tm1637', 'clk2', fallback=18)
DIO2 = config.get('tm1637', 'dio2', fallback=23)

SYSTEM_QUIT = config.get('system', 'quit', fallback='shutdown')

MOTION_DETECTION = config.get('motion', 'detection', fallback='KNN')
MOTION_LEARNING_RATE = config.get('motion', 'learningRate', fallback=0.1)
MOTION_WAIT = config.get('motion', 'wait', fallback=0.3)
MOTION_AREA = config.get('motion', 'area', fallback=1500)
