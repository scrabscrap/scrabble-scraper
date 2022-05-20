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

config = configparser.ConfigParser()
try:
    with open(WORK_DIR + '/scrabble.ini', "r") as config_file:
        config.read_file(config_file)
except Exception as e:
    logging.exception(f"INI-Datei kann nicht gelesen werden {e}")

SIMULATE = config.getboolean('development', 'simulate', fallback=False)
SIMULATE_PATH = config.get('development', 'simulate_path')

MALUS_DOUBT = config.getint('scrabble', 'malus_doubt', fallback=10)
MAX_TIME = config.getint('scrabble', 'max_time', fallback=1800)
MIN_TIME = config.getint('scrabble', 'min_time', fallback=-300)
DOUBT_TIMEOUT = config.getint('scrabble', 'doubt_timeout', fallback=20)

SCREEN = SIMULATE or config.getboolean('output', 'screen', fallback=False)

try:
    import wiringpi
    TM1637 = config.getboolean('output', 'tm1637', fallback=True)
except ImportError:
    TM1637 = False

WRITE_WEB = config.getboolean('output', 'web', fallback=True)
WEB_PATH = config.get('output', 'web_path', fallback=WORK_DIR + '/web/')
FTP = config.getboolean('output', 'ftp', fallback=False)

KEYBOARD = SIMULATE or config.getboolean('input', 'keyboard', fallback=True)

HOLD1 = config.getint('button', 'hold1', fallback=4)
HOLD2 = config.getint('button', 'hold2', fallback=8)

WARP = config.getboolean('video', 'warp', fallback=True)
IM_WIDTH = config.getint('video', 'size', fallback=1504)
IM_HEIGHT = config.getint('video', 'size', fallback=1504)
FPS = config.getint('video', 'fps', fallback=15)
ROTATE = config.getboolean('video', 'rotate', fallback=False)
BOARD_LAYOUT = config.get('board', 'layout', fallback='custom').replace('"', '')

CLK1 = config.getint('tm1637', 'clk1', fallback=24)
DIO1 = config.getint('tm1637', 'dio1', fallback=25)
CLK2 = config.getint('tm1637', 'clk2', fallback=18)
DIO2 = config.getint('tm1637', 'dio2', fallback=23)

SYSTEM_QUIT = config.get('system', 'quit', fallback='shutdown').replace('"', '')

MOTION_DETECTION = config.get('motion', 'detection', fallback='KNN')
MOTION_LEARNING_RATE = config.getfloat('motion', 'learningRate', fallback=0.1)
MOTION_WAIT = config.getfloat('motion', 'wait', fallback=0.3)
MOTION_AREA = config.getint('motion', 'area', fallback=1500)
