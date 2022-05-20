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
import logging
import logging.config
import os

from scrabble import Scrabble

TEST_DIR = os.path.dirname(__file__)

# import line_profiler
# import atexit
# profile = line_profiler.LineProfiler()
# atexit.register(profile.print_stats)

logging.config.fileConfig(fname=os.path.dirname(os.path.abspath(__file__)) + '/test_log.conf',
                          disable_existing_loggers=False)
game_logger = logging.getLogger('boardLogger')
# kein FTP Upload beim Test
config.FTP = False


class ScrabbleGameTestCase(unittest.TestCase):

    def setUp(self):
        # logging.disable(logging.DEBUG) # falls Info-Ausgaben erfolgen sollen
        # logging.disable(logging.ERROR)
        pass

    def test_spiel_12(self):
        from state import Start
        from event import PLAYER1, PLAYER2, RESET, PAUSE

        s = Scrabble()
        s.player = ['A', 'S']
        game_logger.info('')
        zustand = Start()
        for i in range(0, 26):
            img = cv2.imread(f"{TEST_DIR}/spiel-13/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER2
            else:
                action = PLAYER1
            zustand = zustand.next(action, img, s)
        zustand = zustand.next(PAUSE, None, s)
        zustand.scrabble_queue.join()  # vor der Auswertung queue erst abarbeiten !
        self.assertEqual(501, s.get_score("A"))
        self.assertEqual(421, s.get_score("S"))
        zustand.next(RESET, None, s)  # falls ftp eingeschaltet ist, muss das noch abgearbeitet werden
        del s

    def test_spiel_13(self):
        from state import Start
        from event import PLAYER1, PLAYER2, PAUSE, RESET

        s = Scrabble()
        s.player = ['A', 'S']
        game_logger.info('')
        zustand = Start()
        for i in range(0, 21):
            img = cv2.imread(f"{TEST_DIR}/spiel-12/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER2
            else:
                action = PLAYER1
            zustand = zustand.next(action, img, s)
        zustand = zustand.next(PAUSE, None, s)
        zustand.scrabble_queue.join()  # vor der Auswertung queue erst abarbeiten !
        logging.info(str(s))
        self.assertEqual(185, s.get_score("A"))
        self.assertEqual(208, s.get_score("S"))
        zustand.next(RESET, None, s)  # falls ftp eingeschaltet ist, muss das noch abgearbeitet werden
        del s

    def test_spiel_14(self):
        from state import Start
        from event import PLAYER1, PLAYER2, PAUSE, RESET

        s = Scrabble()
        s.player = ['INESSA', 'STEFAN']
        game_logger.info('')
        zustand = Start()
        for i in range(0, 28):
            img = cv2.imread(f"{TEST_DIR}/spiel-14/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER2
            else:
                action = PLAYER1
            zustand = zustand.next(action, img, s)
        zustand = zustand.next(PAUSE, None, s)
        zustand.scrabble_queue.join()  # vor der Auswertung queue erst abarbeiten !
        logging.info(str(s))
        self.assertEqual(425, s.get_score("INESSA"))
        self.assertEqual(362, s.get_score("STEFAN"))
        zustand.next(RESET, None, s)  # falls ftp eingeschaltet ist, muss das noch abgearbeitet werden
        del s

    def test_spiel_15(self):
        from state import Start
        from event import PLAYER1, PLAYER2, PAUSE, RESET, DOUBT

        s = Scrabble()
        s.player = ['JO', 'ST']
        game_logger.info('')
        zustand = Start()
        for i in range(0, 16):
            img = cv2.imread(f"{TEST_DIR}/spiel-15/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER2
            else:
                action = PLAYER1
            zustand = zustand.next(action, img, s)

        img = cv2.imread(f"{TEST_DIR}/spiel-15/board-16.png")
        zustand = zustand.next(PAUSE, img, s)
        zustand = zustand.next(DOUBT, img, s)
        zustand = zustand.next(PLAYER2, img, s)
        zustand = zustand.next(PAUSE, img, s)

        for i in range(16, 19):
            img = cv2.imread(f"{TEST_DIR}/spiel-15/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER1
            else:
                action = PLAYER2
            zustand = zustand.next(action, img, s)

        img = cv2.imread(f"{TEST_DIR}/spiel-15/board-19.png")
        zustand = zustand.next(PAUSE, img, s)
        zustand = zustand.next(DOUBT, img, s)
        zustand = zustand.next(PLAYER2, img, s)
        zustand = zustand.next(PAUSE, img, s)

        for i in range(19, 31):
            img = cv2.imread(f"{TEST_DIR}/spiel-15/board-{i:02d}.png")
            logging.debug(f"State {zustand} Spieler: {(i % 2)}/{s.player[(i % 2)]} read board-{i:02d}.png")
            if (i % 2) == 0:
                action = PLAYER2
            else:
                action = PLAYER1
            zustand = zustand.next(action, img, s)

        zustand = zustand.next(PAUSE, None, s)
        zustand.scrabble_queue.join()  # vor der Auswertung queue erst abarbeiten !
        logging.info(str(s))
        self.assertEqual(323, s.get_score("JO"))
        self.assertEqual(432, s.get_score("ST"))
        zustand.next(RESET, None, s)  # falls ftp eingeschaltet ist, muss das noch abgearbeitet werden
        del s


# unit tests per commandline
if __name__ == '__main__':
    unittest.main()
