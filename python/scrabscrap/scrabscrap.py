#! /usr/bin/env python3
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

import atexit
import logging
import logging.config
import os
import signal
import sys
import time

import cv2
import imutils
import numpy as np

from action import PLAYER1, PLAYER2
from config import SIMULATE, SCREEN, SYSTEM_QUIT, MOTION_DETECTION, MOTION_LEARNING_RATE, MOTION_AREA, BOARD_LAYOUT
from event import ActionEvent
from hardware import videostream as vs
from hardware import led
from scrabble import Scrabble
from state import Start
from threading import Event

logging.config.fileConfig(fname='log.conf', disable_existing_loggers=False)

IS_RPI = os.uname()[4].startswith("arm")


# noinspection PyUnresolvedReferences
class Game:

    def __init__(self):
        logging.info(os.uname())
        self.scrabble = Scrabble()
        self.picture = None
        self.resized = None
        if MOTION_DETECTION == 'KNN':
            self.subtractor = cv2.createBackgroundSubtractorKNN(history=20, dist2Threshold=50.0, detectShadows=False)
            # self.subtractor = cv2.createBackgroundSubtractorKNN(history=20, dist2Threshold=25, detectShadows=False)
        elif MOTION_DETECTION == 'MOG2':
            self.subtractor = cv2.createBackgroundSubtractorMOG2(detectShadows=False)
            # self.subtractor = cv2.createBackgroundSubtractorMOG2(history=20, varThreshold=16, detectShadows=False)
        if BOARD_LAYOUT == 'custom':
            self.filter = self.custom_filter
        else:
            self.filter = self.classic_filter
        self.state = Start()
        try:
            self.cap = vs.get_video()
        except Exception as e:
            logging.error(f"(camera) Exception {e}")
            self.state.timer1.message("CAM ")
            self.state.timer2.message("ERR ")
            led.led_off()
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        signal.signal(signal.SIGINT, self.cleanup)

    def cleanup(self):
        self.state.timer1.message("    ")
        self.state.timer2.message("    ")
        logging.getLogger('').handlers[0].doRollover()
        logging.getLogger('cameraLogger').handlers[0].doRollover()
        logging.getLogger('visualLogger').handlers[0].doRollover()
        led.led_off()
        cv2.destroyAllWindows()
        self.cap.stop()
        if not self.cap.camera.closed:
            self.cap.close()

    @staticmethod
    def classic_filter(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray

    @staticmethod
    def custom_filter(image):
        blur = cv2.blur(image, (5, 5))
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        lower = np.array([45, 50, 10])
        upper = np.array([95, 255, 255])
        m = cv2.inRange(hsv, lower, upper)
        m = cv2.bitwise_not(m)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_and(gray, gray, mask=m)
        return gray

    def motion_detection(self, frame):
        if SIMULATE:
            return False, frame
        filtered = self.filter(frame)
        thresh = self.subtractor.apply(filtered, learningRate=MOTION_LEARNING_RATE)
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]

        # height, width, _ = frame.shape
        motion = False
        # if the contour is too small, ignore it
        if len(cnts) > 0 and cv2.contourArea(cnts[0]) > MOTION_AREA:
            (x, y, w, h) = cv2.boundingRect(cnts[0])
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
            # if x < 1 or y < 1 or (x+w) > width-1 or (y+h) > (height+1):
            # only motion from outside
            motion = True
        return motion, frame

    def set_names(self):
        from analyzer import analyze_picture

        motion = True
        while motion:
            _, self.resized = self.cap.read()
            motion, _ = self.motion_detection(self.resized)
            time.sleep(0.7)

        _, self.picture = self.cap.read()
        board, _ = analyze_picture(self.picture)
        erg1 = ""
        erg2 = ""
        for i in range(0, 7):
            if (i, 7) in board.keys():
                erg1 += board[(i, 7)][0]
            if (i + 8, 7) in board.keys():
                erg2 += board[(i + 8, 7)][0]
        if len(erg1) <= 0:
            erg1 = "Spieler1"
        if len(erg2) <= 0:
            erg2 = "Spieler2"
        self.scrabble.player = [erg1, erg2]
        logging.info(f"set names {self.scrabble.player}")

    def reset(self):
        logging.info("(reset) game restart")
        self.state.timer1.message("  RE")
        self.state.timer2.message("SET ")
        time.sleep(5)
        logging.getLogger('').handlers[0].doRollover()
        logging.getLogger('cameraLogger').handlers[0].doRollover()
        logging.getLogger('visualLogger').handlers[0].doRollover()
        cv2.destroyAllWindows()
        self.cap.stop()
        if not self.cap.camera.closed:
            self.cap.close()
        # restart app in current pid
        os.sync()
        argv = [sys.executable] + sys.argv
        os.execv(sys.executable, argv)

    def start_config_server(self):
        script_dir = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + "/../../script")

        logging.info("(config) start config server")
        self.state.timer1.message("CFG ")
        self.state.timer2.message("BOOT")
        time.sleep(5)
        logging.getLogger('').handlers[0].doRollover()
        logging.getLogger('cameraLogger').handlers[0].doRollover()
        logging.getLogger('visualLogger').handlers[0].doRollover()
        self.cap.stop()
        if not self.cap.camera.closed:
            self.cap.close()

        os.sync()
        script = script_dir + "/server.sh"
        os.system(script)
        sys.exit(0)

    def main(self):
        self.state.timer1.message("CAM ")
        self.state.timer2.message("    ")
        try:
            self.cap.start()
            _, self.resized = self.cap.read()
            self.state.timer1.fill_display()
            self.state.timer2.fill_display()
        except Exception as e:
            logging.error(f"cam exception {e}")
            self.state.timer2.message("ERR ")
            time.sleep(30)

        if SIMULATE:
            self.cap.cnt = 0
        action_event = Event()
        event_provider = ActionEvent(action_event)
        while True:
            action = None
            motion = False
            while action is None:
                event_provider.wait(action_event)
                action_event.wait(0.4)
                action = event_provider.get_event()

                # motion detection
                _, self.resized = self.cap.read()
                motion, _ = self.motion_detection(self.resized)

            # nur während des aktiven Spiels bei Zugbestätigung Foto machen
            if action in (PLAYER1, PLAYER2) \
                    and str(self.state) not in ('P1', 'P2', 'D1', 'D2', 'D1P1', 'D2P2'):

                logging.debug("main: start read picture (motion={})".format(motion))
                for _ in range(0, 10):
                    if not motion:
                        break
                    _, self.resized = self.cap.read()
                    motion, _ = self.motion_detection(self.resized)
                    time.sleep(0.04)
                self.picture = self.cap.picture()
                logging.debug("main: end read picture")
            else:
                self.picture = None

            self.state = self.state.next(action, self.picture, self.scrabble)

            if SCREEN:
                cv2.imshow("Live", self.resized)

            if str(self.state) == 'Start':
                logging.info('main: start the game with 1/2')
            elif str(self.state) == 'Names':
                self.state.timer1.message('    ')
                self.state.timer2.message('    ')
                self.set_names()
                self.state.timer1.message(self.scrabble.player[0][:4].upper())
                self.state.timer2.message(self.scrabble.player[1][:4].upper())
            elif str(self.state) == 'Reset':
                self.reset()
            elif str(self.state) == 'Config':
                self.start_config_server()
            elif str(self.state) == 'Quit':
                break
            logging.info("main: state {} timer 1={:d} timer 2={:d}".format(str(self.state), self.state.timer1.current(),
                                                                      self.state.timer2.current()))
        led.led_off()
        if SYSTEM_QUIT == 'reboot':
            logging.info("main: reboot")
            self.state.timer1.message("  RE")
            self.state.timer2.message("BOOT")
            time.sleep(2)
            os.system('sudo reboot')
        elif SYSTEM_QUIT == 'shutdown':
            logging.info("main: shutdown")
            self.state.timer1.message("SHUT")
            self.state.timer2.message("DOWN")
            time.sleep(2)
            os.system('sudo poweroff')
        logging.info("main: exit app")
        self.state.timer1.message("END ")
        self.state.timer2.message("APP ")
        time.sleep(2)
        self.state.timer1.message("    ")
        self.state.timer2.message("    ")
        sys.exit(0)


if __name__ == '__main__':
    Game().main()
