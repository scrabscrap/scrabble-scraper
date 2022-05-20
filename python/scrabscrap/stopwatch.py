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

import datetime
import time
from datetime import timedelta
from threading import Thread

from config import TM1637, CLK1, CLK2, DIO1, DIO2, MAX_TIME, MIN_TIME, DOUBT_TIMEOUT


class StopWatch:

    def __init__(self, nummer, name="stopwatch"):
        # initialize the thread name
        self.name = name
        self.paused = True
        self.exit = False
        self.timer_date = None
        self.timer_left = timedelta(seconds=MAX_TIME)
        self.overtime_date = None
        self.overtime_left = timedelta(seconds=-MIN_TIME)
        self.counter_date = None
        self.counter_left = timedelta(seconds=0)
        self.callback = None

        if TM1637:
            from hardware import tm1637

            if nummer <= 0:
                self.display = tm1637.TM1637(clk=CLK1, dio=DIO1)
            else:
                self.display = tm1637.TM1637(clk=CLK2, dio=DIO2)
            self._fill = self.fill_display
        else:
            self.display = None
            self._fill = self.dummy

    def cleanup(self):
        self.reset()
        if TM1637:
            from hardware import tm1637
            self.display.write([0, 0, 0, 0])

    def init(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        self._fill()
        return self

    def start(self):
        if self.paused:
            _now = datetime.datetime.now()
            self.timer_date = _now + self.timer_left
            self.counter_date = _now + self.counter_left
            self.overtime_date = self.timer_date + self.overtime_left
        self.paused = False
        self._fill()

    def start_countdown(self, callback=None):
        self.counter_left = timedelta(seconds=DOUBT_TIMEOUT)
        if callback:
            self.callback = callback

    def end_countdown(self):
        self.callback = None
        self.counter_date = None
        self.counter_left = timedelta(seconds=0)

    def pause(self):
        self.paused = True
        _now = datetime.datetime.now()
        if self.timer_date is not None:
            self.timer_left = self.timer_date - _now
        if self.counter_date is not None:
            self.counter_left = self.counter_date - _now
        if self.overtime_date is not None:
            self.overtime_left = self.overtime_date - _now
        self.timer_date = None
        self.counter_date = None
        self.overtime_date = None
        self._fill()

    def stop(self):
        self.reset()
        self.exit = True

    def reset(self):
        self.paused = True
        self.timer_date = None
        self.timer_left = timedelta(seconds=MAX_TIME)
        self.overtime_date = None
        self.overtime_left = timedelta(seconds=-MIN_TIME)
        self.counter_date = None
        self.counter_left = timedelta(seconds=0)
        self._fill()

    def move_possible(self):
        _now = datetime.datetime.now()
        t_left = (self.timer_date - _now) if self.timer_date is not None else self.timer_left
        return MIN_TIME < t_left.total_seconds()

    def doubt_possible(self):
        c_left = (self.counter_date - datetime.datetime.now()) if self.counter_date is not None else self.counter_left
        return 0 < c_left.total_seconds() <= DOUBT_TIMEOUT, int(c_left.total_seconds())

    def current(self):
        _now = datetime.datetime.now()
        t_left = (self.timer_date - _now) if self.timer_date is not None else self.timer_left
        return int(t_left.total_seconds())

    def get_timer(self):
        _now = datetime.datetime.now()
        t_left = (self.timer_date - _now) if self.timer_date is not None else self.timer_left
        if 0 < t_left.total_seconds() <= MAX_TIME:  # innerhalb der normalen Zeit
            return f"{int((t_left.seconds // 60) % 60):02d}{int(t_left.seconds % 60):02d}"
        if MIN_TIME < t_left.total_seconds() <= 0:  # in der "Strafzeit"
            _s = int(-t_left.total_seconds())
            return f"-{int((_s // 60) % 60):01d}{int(_s % 60):02d}"
        return "----"

    def fill_display(self):
        if self.display is not None:
            self.display.show(self.get_timer(), True)

    def message(self, msg):
        if self.display is not None:
            self.display.show(msg)

    def _write(self, msg):
        if self.display is not None:
            self.display.write(msg)

    def dummy(self):
        pass

    def update(self):
        while True:
            if self.exit:
                return
            if not self.paused:
                self._fill()
                if self.callback:
                    self.callback()
            time.sleep(1)
