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
import unittest

import config
import cv2
import logging.config
import os

from analyzer import analyze_picture
from scrabble import Scrabble

logging.config.fileConfig(fname=os.path.dirname(os.path.abspath(__file__)) + '/test_log.conf', disable_existing_loggers=True)
# kein FTP Upload beim Test
config.FTP = False


class ScrabbleMusterTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_names(self):

        files = ["test/board-neu/board-04.png"]
        last_board = None
        for f in files:
            img = cv2.imread(f)
            print(f)
            ret, _ = analyze_picture(img, must_warp=True, layout='custom', last_board=last_board)
            # last_board = ret  # falls der Test vorige Boards berücksichtigen soll
            res = {(3, 7): 'A',
                    (4, 7): 'N',
                    (5, 7): 'K',
                    (6, 7): 'E',
                    (7, 7): '_',
                    (8, 7): 'S',
                    (9, 7): 'T',
                    (10, 7): 'E',
                    (11, 7): 'F',
                    (12, 7): 'A',
                    (13, 7): 'N'}
            k = ret.keys()
            v = ret.values()
            k1 = [(x, y) for (x, y) in k]
            v1 = [t for (t, p) in v]
            out = Scrabble.print_board(ret, {}, {})
            logging.debug(out)
            self.assertEqual(dict(zip(*[k1, v1])), res, "Test")

    def test_err_images(self):

        files = ["test/board-neu/err-01.png", "test/board-neu/err-02.png", "test/board-neu/err-03.png",
                    "test/board-neu/err-04.png", "test/board-neu/err-05.png", "test/board-neu/err-06.png",
                    "test/board-neu/err-07.png", "test/board-neu/err-08.png", "test/board-neu/err-09.png",
                    "test/board-neu/err-10.png", "test/board-neu/err-11.png", "test/board-neu/err-12.png",
                    "test/board-neu/err-13.png", "test/board-neu/err-14.png", "test/board-neu/err-15.png",
                    "test/board-neu/err-16.png", "test/board-neu/err-17.png", "test/board-neu/err-18.png",
                    "test/board-neu/err-19.png", "test/board-neu/err-20.png", "test/board-neu/err-21.png",
                    "test/board-neu/err-22.png", "test/board-neu/err-23.png", "test/board-neu/err-24.png"
                    ]
        last_board = None
        for f in files:
            img = cv2.imread(f)
            print(f)
            ret, _ = analyze_picture(img, must_warp=True, layout='custom', last_board=last_board)
            # last_board = ret  # falls der Test vorige Boards berücksichtigen soll
            res = {(4, 11): 'G', (5, 7): 'Y', (5, 10): 'U', (5, 11): 'S', (6, 7): 'L', (6, 10): 'Ü',
                    (7, 7): 'A', (7, 8): 'E', (7, 9): 'E', (7, 10): 'N', (8, 7): 'T', (9, 7): 'Z',
                    (10, 5): 'W', (10, 6): 'Ö', (10, 7): 'I', (10, 8): 'U', (10, 9): 'Ä'}
            k = ret.keys()
            v = ret.values()
            k1 = [(x, y) for (x, y) in k]
            v1 = [t for (t, p) in v]
            out = Scrabble.print_board(ret, {}, {})
            logging.debug(out)
            self.assertEqual(dict(zip(*[k1, v1])), res, "Test")

    def test_new_images(self):

        files = ["test/board-neu/board-00.png", "test/board-neu/board-01.png",
                    "test/board-neu/board-03.png"]

        for f in files:
            img = cv2.imread(f)
            print(f)
            ret, _ = analyze_picture(img, must_warp=True, layout='custom')
            res = {(5, 7): 'V', (6, 6): 'M', (6, 7): 'Ä', (6, 8): 'Y',
                    (6, 9): 'X', (7, 7): 'L', (7, 9): 'G', (8, 7): 'S',
                    (8, 9): 'A', (8, 10): 'Ü', (8, 11): 'T'}
            k = ret.keys()
            v = ret.values()
            k1 = [(x, y) for (x, y) in k]
            v1 = [t for (t, p) in v]
            out = Scrabble.print_board(ret, {}, {})
            logging.debug(out)
            self.assertEqual(dict(zip(*[k1, v1])), res, "Test")


# unit tests per commandline
if __name__ == '__main__':
    unittest.main()
