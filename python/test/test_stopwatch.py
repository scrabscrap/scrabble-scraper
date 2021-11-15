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

import time
import unittest
from datetime import timedelta

import stopwatch


class StopWatchTestCase(unittest.TestCase):

    def test_stopwatch(self):
        # 0-0.9 => 1 s
        # 1-1.9 => 2 s
        timer1 = stopwatch.StopWatch(0, "spieler1").init()
        timer2 = stopwatch.StopWatch(1, "spieler2").init()

        stopwatch.DOUBT_TIMEOUT = 2
        timer1.start_countdown()
        timer1.start()
        timer2.start()
        self.assertEqual(timer1.doubt_possible()[0], True, "Doubt possible")
        time.sleep(3)
        timer1.pause()
        timer2.pause()
        self.assertEqual(timer1.doubt_possible()[0], False, "Doubt not possible")

        self.assertEqual(timer1.get_timer(), "2956", "timer1 29:56 Restlaufzeit")
        self.assertEqual(timer2.get_timer(), "2956", "timer2 29:56 Restlaufzeit")

        timer1.start()
        time.sleep(2)
        timer1.pause()

        self.assertEqual(timer1.get_timer(), "2954", "timer1 29:54 Restlaufzeit")
        self.assertEqual(timer2.get_timer(), "2956", "timer2 29:56 Restlaufzeit")

        timer2.start()
        time.sleep(2)
        timer2.pause()

        self.assertEqual(timer1.get_timer(), "2954", "timer1 29:54 Restlaufzeit")
        self.assertEqual(timer2.get_timer(), "2954", "timer2 29:54 Restlaufzeit")

        timer2.start()
        time.sleep(0.9)
        timer2.pause()
        timer1.start()
        time.sleep(1)
        timer1.pause()

        self.assertEqual(timer1.get_timer(), "2953", "timer1 29:53 Restlaufzeit")
        self.assertEqual(timer2.get_timer(), "2954", "timer2 29:54 Restlaufzeit")

        timer1.reset()
        self.assertEqual(timer1.get_timer(), "3000", "timer1 reset")

        timer1.timer_left = timedelta(seconds=2)
        timer1.start()
        time.sleep(3)
        timer1.pause()
        self.assertEqual(timer1.get_timer(), "-001", "timer1 1s überzogen")

        timer1.start()
        time.sleep(3)
        timer1.pause()
        self.assertEqual(timer1.get_timer(), "-004", "timer1 4s überzogen")

        timer1.timer_left = timedelta(seconds=-299)
        timer1.start()
        time.sleep(3)
        timer1.pause()
        self.assertEqual(timer1.get_timer(), "----", "timer1 komplett überzogen")


# unit tests per commandline
if __name__ == '__main__':
    unittest.main()
