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

import logging
import queue

from action import PLAYER1, PLAYER2, PAUSE, DOUBT, RESET, QUIT, CONFIG
from stopwatch import StopWatch
from worker.scrabble import ScrabbleOp, WorkerScrabble
from hardware import led


class State:
    timer1 = StopWatch(0, "player1").init()
    timer2 = StopWatch(1, "player2").init()
    state_blue_led = ''
    scrabble_queue = queue.Queue(0)

    def __init__(self):
        led.led_off()
    
    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__class__.__name__

    def next(self, action, picture, scrabble):
        assert 0, "next nicht implementiert"

    def doubt_callback(self, _led_state="off"):
        pass


class Start(State):

    def __init__(self):
        super().__init__()
        self.timer1.message("STAR")
        self.timer2.message("TING")
        WorkerScrabble(self.scrabble_queue).start()
        led.red_blink()
        led.green_blink()
        led.yellow_blink()

    def next(self, action, _picture, _scrabble):
        if action == PAUSE:
            return Names()
        if action == PLAYER1:
            self.scrabble_queue.put(
                ScrabbleOp("start", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("start (next S2)")
            return S2()
        if action == PLAYER2:
            self.scrabble_queue.put(
                ScrabbleOp("start", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("start (next S1)")
            return S1()
        if action == RESET:
            self.timer1.message("  RE")
            self.timer2.message("SET ")
            led.led_off()
            self.scrabble_queue.put(
                ScrabbleOp("reset", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("reset der Anwendung")
            return Reset()
        if action == QUIT:
            self.timer1.message(" APP")
            self.timer2.message("END ")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("quit der Anwendung")
            return Quit()
        if action == CONFIG:
            self.timer1.message("CFG ")
            self.timer2.message("BOOT")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("starte config")
            return Config()
        return self


class Names(State):

    def __init__(self):
        super().__init__()
        led.red_blink()
        led.green_blink()
        led.yellow_blink()

    def next(self, action, _picture, _scrabble):
        if action == PAUSE:
            return Names()
        if action == PLAYER1:
            self.scrabble_queue.put(
                ScrabbleOp("start", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return S2()
        if action == PLAYER2:
            self.scrabble_queue.put(
                ScrabbleOp("start", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return S1()
        if action == RESET:
            self.timer1.message("  RE")
            self.timer2.message("SET ")
            led.led_off()
            self.scrabble_queue.put(
                ScrabbleOp("reset", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Reset()
        if action == QUIT:
            self.timer1.message(" APP")
            self.timer2.message("END ")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Quit()
        if action == CONFIG:
            self.timer1.message("CFG ")
            self.timer2.message("BOOT")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Config()
        return self


class S1(State):
 
    def __init__(self):
        super().__init__()
        led.green_led()
        self.timer1.start()
        self.timer2.pause()
        self.blue = 0
        if self.timer1.doubt_possible()[0]:
            self.timer1.callback = self.doubt_callback
            self.blue = 0

    def doubt_callback(self, _led_state="off"):
        d, t = self.timer1.doubt_possible()
        if not d and self.blue > 0:
            led.blue.off()
            self.blue = 0
            return
        if d and self.blue != 1 and 0 < t < 5:
            led.blue_blink()
            self.blue = 1

    def next(self, action, _picture, _scrabble):
        if action == PLAYER1:
            if not self.timer1.move_possible():
                return self
            self.scrabble_queue.put(
                ScrabbleOp("move", _picture, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            self.timer1.end_countdown()
            self.timer2.start_countdown()
            return S2()
        if action == PAUSE:
            logging.debug("pause (next P1)")
            return P1()
        return self


class P1(State):

    def __init__(self, message=None):
        super().__init__()
        led.green_led()
        led.yellow_led()
        self.timer1.pause()
        self.timer2.pause()
        self.message = message
        if self.timer1.doubt_possible()[0]:
            led.blue_blink()
        if message:
            self.timer1.message(message)

    def next(self, action, _picture, _scrabble):
        if self.message:
            self.timer1.fill_display()
        if action in (PAUSE, PLAYER2):
            logging.debug("continue (next S1)")
            return S1()
        if action == DOUBT and self.timer1.doubt_possible()[0]:
            logging.debug("doubt (next D1)")
            return D1()
        if action == RESET:
            self.timer1.message("  RE")
            self.timer2.message("SET ")
            led.led_off()
            self.scrabble_queue.put(
                ScrabbleOp("reset", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Reset()
        if action == QUIT:
            self.timer1.message(" APP")
            self.timer2.message("END ")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Quit()
        if action == CONFIG:
            self.timer1.message("CFG ")
            self.timer2.message("BOOT")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Config()
        return self


class D1(State):

    def __init__(self, message=None):
        super().__init__()
        led.green_led()
        led.blue_led()
        if message:
            self.timer2.message(message)

    def next(self, action, _picture, _scrabble):
        if action == PLAYER2:
            # display spieler 1 = -10
            self.scrabble_queue.put(
                ScrabbleOp("challenge", _picture, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("invalid challenge (next P1)")
            return P1(" -10")
        if action == PLAYER1:
            logging.debug("correct challenge (next D1P1)")
            return D1P1()
        if action == PAUSE:
            logging.debug("cancel challenge (next P1)")
            return P1()
        if action == DOUBT:
            return self
        return self


class D1P1(State):

    def __init__(self):
        super().__init__()
        led.green_led()
        led.yellow_led()
        led.blue_blink()
        self.timer2.message("UNDO")

    def next(self, action, _picture, _scrabble):
        if action in (PAUSE, PLAYER2):
            # korrektes Anzweifeln
            # display spieler 2 = undo
            # self.timer2.message("undo")
            self.scrabble_queue.put(
                ScrabbleOp("--", _picture, 0, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("continue after correct challenge (next S1)")
            return S1()
        if action == DOUBT:
            self.timer1.fill_display()
            logging.debug("cancel correct challenge (next D1)")
            return D1()
        return self


class S2(State):

    def __init__(self):
        super().__init__()
        led.red_led()
        self.timer1.pause()
        self.timer2.start()
        self.blue = 0
        if self.timer2.doubt_possible()[0]:
            self.blue = 0
            self.timer2.callback = self.doubt_callback

    def doubt_callback(self, _led_state="off"):
        d, t = self.timer2.doubt_possible()
        if not d and self.blue > 0:
            led.blue.off()
            self.blue = 0
            return
        if d and self.blue != 1 and 0 < t < 5:
            led.blue_blink()
            self.blue = 1

    def next(self, action, _picture, _scrabble):
        if action == PLAYER2:
            if not self.timer2.move_possible():
                return self
            self.scrabble_queue.put(
                ScrabbleOp("move", _picture, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            self.timer2.end_countdown()
            self.timer1.start_countdown()
            return S1()
        if action == PAUSE:
            logging.debug("pause (next P2)")
            return P2()
        return self


class P2(State):

    def __init__(self, message=None):
        super().__init__()
        led.red_led()
        led.yellow_led()
        self.timer1.pause()
        self.timer2.pause()
        self.message = message
        if self.timer2.doubt_possible()[0]:
            led.blue_blink()
        if message:
            self.timer2.message(message)

    def next(self, action, _picture, _scrabble):
        if self.message:
            self.timer2.fill_display()
        if action in (PAUSE, PLAYER1):
            logging.debug("continue (next S2)")
            return S2()
        if action == DOUBT and self.timer2.doubt_possible()[0]:
            logging.debug("doubt (next D1)")
            return D2()
        if action == RESET:
            self.timer1.message("  RE")
            self.timer2.message("SET ")
            led.led_off()
            self.scrabble_queue.put(
                ScrabbleOp("reset", None, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Reset()
        if action == QUIT:
            self.timer1.message(" APP")
            self.timer2.message("END ")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Quit()
        if action == CONFIG:
            self.timer1.message("CFG ")
            self.timer2.message("BOOT")
            self.scrabble_queue.put(
                ScrabbleOp("quit", None, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            return Config()
        return self


class D2(State):

    def __init__(self):
        super().__init__()
        led.red_led()
        led.blue_led()

    def next(self, action, _picture, _scrabble):
        if action == PLAYER1:
            # display spieler 2 = -10
            self.scrabble_queue.put(
                ScrabbleOp("challenge", _picture, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("invalid challenge (next P2)")
            return P2(" -10")
        if action == PLAYER2:
            logging.debug("correct challenge (next D2P2)")
            return D2P2()
        if action == PAUSE:
            logging.debug("cancel challenge (next P1)")
            return P2()
        if action == DOUBT:
            return self
        return self


class D2P2(State):

    def __init__(self):
        super().__init__()
        led.red_led()
        led.yellow_led()
        led.blue_blink()
        self.timer1.message("UNDO")

    def next(self, action, _picture, _scrabble):
        if action in (PAUSE, PLAYER1):
            # korrektes Anzweifeln
            # display spieler 1 = undo
            # self.timer1.message("undo")
            self.scrabble_queue.put(
                ScrabbleOp("--", _picture, 1, _scrabble, [self.timer1.current(), self.timer2.current()]))
            logging.debug("continue after correct challenge (next S2)")
            return S2()
        if action == DOUBT:
            self.timer1.fill_display()
            logging.debug("cancel correct challenge (next D2)")
            return D2()
        return self


class Reset(State):

    def __init__(self):
        super().__init__()
        led.led_off()
        self.timer1.reset()
        self.timer2.reset()
        self.scrabble_queue.put(None)
        self.scrabble_queue.join()

    def next(self, action, _picture, _scrabble):
        if PAUSE == action:
            logging.info("neues Spiel beginnt")
            return Start()
        return self


class Quit(State):

    def __init__(self):
        super().__init__()
        led.led_off()
        self.timer1.stop()
        self.timer2.stop()
        self.timer1.message("END ")
        self.timer2.message("    ")
        self.scrabble_queue.put(None)
        self.scrabble_queue.join()

    def next(self, action, _picture, _scrabble):
        return self


class Config(State):

    def __init__(self):
        super().__init__()
        led.led_off()
        self.timer1.stop()
        self.timer2.stop()
        self.timer1.message("CFG ")
        self.timer2.message("BOOT")
        self.scrabble_queue.put(None)
        self.scrabble_queue.join()

    def next(self, action, _picture, _scrabble):
        return self

