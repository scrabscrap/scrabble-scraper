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
import logging
import logging.config
import os

from scrabble import Scrabble

logging.config.fileConfig(fname=os.path.dirname(os.path.abspath(__file__)) + '/test_log.conf',
                          disable_existing_loggers=False)
# kein FTP Upload beim Test
config.FTP = False


class AlgorithmusTestCase(unittest.TestCase):

    def setUp(self):
        # logging.disable(logging.DEBUG)  # falls Info-Ausgaben erfolgen sollen
        # logging.disable(logging.ERROR)
        pass

    def test_10(self):
        # Testfall 10 - Hand auf dem Spielfeld
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        board = {(0, 0): ('_', 75), (0, 1): ('_', 75), (0, 2): ('_', 75), (0, 3): ('_', 75),
                 (1, 0): ('_', 75), (1, 1): ('_', 75), (1, 2): ('_', 75), (1, 3): ('_', 75),
                 (2, 0): ('_', 75), (2, 1): ('_', 75), (2, 2): ('_', 75), (2, 3): ('_', 75),
                 (2, 4): ('_', 75), (2, 5): ('_', 75), (2, 6): ('_', 75), (2, 7): ('_', 75),
                 (3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        s.move(board, "Spieler2")
        expected = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}

        logging.info(s.print_board(s.game[-1][s.DICT_BOARD], {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        self.assertEqual(0, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[expected.keys(), [t for (t, p) in expected.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 10")
        del s

    def test_101(self):
        # Testfall 101 - Algorithmus: Tauschen bei leerem Board
        s = Scrabble()
        board = {}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(1, len(s.game))
        self.assertEqual(0, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual({}, cmp, "Test 101")
        del s

    def test_102(self):
        # Testfall 102 - Algorithmus: erster Zug auf dem Spielfeld
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(1, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 102")
        del s

    def test_103(self):
        # Testfall 103 - Algorithmus: gekreuzter Zug
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 5G V.TEN
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        self.assertEqual(20, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 103")
        del s

    def test_104(self):
        # Testfall 104 - Algorithmus: Zug am oberen Rand (waagerecht)
        s = Scrabble()
        # H4 TURNeNS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8A SAUNIER.
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (7, 0): ('S', 75), (7, 1): ('A', 75), (7, 2): ('U', 75), (7, 3): ('N', 75), (7, 4): ('I', 75),
                 (7, 5): ('E', 75), (7, 6): ('R', 75)}
        s.move(board, "Spieler2")
        # A8 .UPER
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (7, 0): ('S', 75), (7, 1): ('A', 75), (7, 2): ('U', 75), (7, 3): ('N', 75), (7, 4): ('I', 75),
                 (7, 5): ('E', 75), (7, 6): ('R', 75),
                 (8, 0): ('U', 75), (9, 0): ('P', 75), (10, 0): ('E', 75), (11, 0): ('R', 75)}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(3, len(s.game))
        self.assertEqual(74, s.get_score("Spieler2"))
        self.assertEqual(73, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 104")
        del s

    def test_105(self):
        # Testfall 105 - Algorithmus: Zug am oberen Rand (senkrecht)
        s = Scrabble()
        # H4 TURNeNS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8A SAUNIER.
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (7, 0): ('S', 75), (7, 1): ('A', 75), (7, 2): ('U', 75), (7, 3): ('N', 75), (7, 4): ('I', 75),
                 (7, 5): ('E', 75), (7, 6): ('R', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(74, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 105")
        del s

    def test_106(self):
        # Testfall 106 - Algorithmus: Zug am unteren Rand (waagerecht)
        s = Scrabble()
        # H2 TURNeNS
        board = {(1, 7): ('T', 75), (2, 7): ('U', 75), (3, 7): ('R', 75), (4, 7): ('N', 75), (5, 7): ('_', 75),
                 (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8H .AUNIERE
        board = {(1, 7): ('T', 75), (2, 7): ('U', 75), (3, 7): ('R', 75), (4, 7): ('N', 75), (5, 7): ('_', 75),
                 (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (7, 8): ('A', 75), (7, 9): ('U', 75), (7, 10): ('N', 75), (7, 11): ('I', 75),
                 (7, 12): ('E', 75), (7, 13): ('R', 75), (7, 14): ('E', 75)}
        s.move(board, "Spieler2")
        # O5 SUP.R
        board = {(1, 7): ('T', 75), (2, 7): ('U', 75), (3, 7): ('R', 75), (4, 7): ('N', 75), (5, 7): ('_', 75),
                 (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (7, 8): ('A', 75), (7, 9): ('U', 75), (7, 10): ('N', 75), (7, 11): ('I', 75),
                 (7, 12): ('E', 75), (7, 13): ('R', 75), (7, 14): ('E', 75),
                 (4, 14): ('S', 75), (5, 14): ('U', 75), (6, 14): ('P', 75), (8, 14): ('R', 75)}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(3, len(s.game))
        self.assertEqual(77, s.get_score("Spieler2"))
        self.assertEqual(72, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 106")
        del s

    def test_107(self):
        # Testfall 107 - Algorithmus: Zug am unteren Rand (senkrecht)
        s = Scrabble()
        # H2 TURNeNS
        board = {(1, 7): ('T', 75), (2, 7): ('U', 75), (3, 7): ('R', 75), (4, 7): ('N', 75), (5, 7): ('_', 75),
                 (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8H SAUNIER.
        board = {(1, 7): ('T', 75), (2, 7): ('U', 75), (3, 7): ('R', 75), (4, 7): ('N', 75), (5, 7): ('_', 75),
                 (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (7, 8): ('A', 75), (7, 9): ('U', 75), (7, 10): ('N', 75), (7, 11): ('I', 75),
                 (7, 12): ('E', 75), (7, 13): ('R', 75), (7, 14): ('E', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(77, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 107")
        del s

    def test_108(self):
        # Testfall 108 - Algorithmus: Zug am linken Rand (waagerecht)
        s = Scrabble()
        # 8D TURNeNS
        board = {(7, 3): ('T', 75), (7, 4): ('U', 75), (7, 5): ('R', 75), (7, 6): ('N', 75), (7, 7): ('_', 75),
                 (7, 8): ('N', 75), (7, 9): ('S', 75)}
        s.move(board, "Spieler1")
        # H1 SAUNIER.
        board = {(7, 3): ('T', 75), (7, 4): ('U', 75), (7, 5): ('R', 75), (7, 6): ('N', 75), (7, 7): ('_', 75),
                 (7, 8): ('N', 75), (7, 9): ('S', 75),
                 (0, 7): ('S', 75), (1, 7): ('A', 75), (2, 7): ('U', 75), (3, 7): ('N', 75), (4, 7): ('I', 75),
                 (5, 7): ('E', 75), (6, 7): ('R', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(74, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 108")
        del s

    def test_109(self):
        # Testfall 109 - Algorithmus: Zug am linken Rand (senkrecht)
        s = Scrabble()
        # 8D TURNeNS
        board = {(7, 3): ('T', 75), (7, 4): ('U', 75), (7, 5): ('R', 75), (7, 6): ('N', 75), (7, 7): ('_', 75),
                 (7, 8): ('N', 75), (7, 9): ('S', 75)}
        s.move(board, "Spieler1")
        # H1 SAUNIER.
        board = {(7, 3): ('T', 75), (7, 4): ('U', 75), (7, 5): ('R', 75), (7, 6): ('N', 75), (7, 7): ('_', 75),
                 (7, 8): ('N', 75), (7, 9): ('S', 75),
                 (0, 7): ('S', 75), (1, 7): ('A', 75), (2, 7): ('U', 75), (3, 7): ('N', 75), (4, 7): ('I', 75),
                 (5, 7): ('E', 75), (6, 7): ('R', 75)}
        s.move(board, "Spieler2")
        # 1H .UPER
        board = {(7, 3): ('T', 75), (7, 4): ('U', 75), (7, 5): ('R', 75), (7, 6): ('N', 75), (7, 7): ('_', 75),
                 (7, 8): ('N', 75), (7, 9): ('S', 75),
                 (0, 7): ('S', 75), (1, 7): ('A', 75), (2, 7): ('U', 75), (3, 7): ('N', 75), (4, 7): ('I', 75),
                 (5, 7): ('E', 75), (6, 7): ('R', 75),
                 (0, 8): ('U', 75), (0, 9): ('P', 75), (0, 10): ('E', 75), (0, 11): ('R', 75)
                 }
        s.move(board, "Spieler1")

        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(3, len(s.game))
        self.assertEqual(74, s.get_score("Spieler2"))
        self.assertEqual(73, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 109")
        del s

    def test_110(self):
        # Testfall 110 - Algorithmus: Zug am rechten Rand (waagerecht)
        s = Scrabble()
        # 8B TURNeNS
        board = {(7, 1): ('T', 75), (7, 2): ('U', 75), (7, 3): ('R', 75), (7, 4): ('N', 75), (7, 5): ('_', 75),
                 (7, 6): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # H8 .AUNIERE
        board = {(7, 1): ('T', 75), (7, 2): ('U', 75), (7, 3): ('R', 75), (7, 4): ('N', 75), (7, 5): ('_', 75),
                 (7, 6): ('N', 75), (7, 7): ('S', 75),
                 (8, 7): ('A', 75), (9, 7): ('U', 75), (10, 7): ('N', 75), (11, 7): ('I', 75),
                 (12, 7): ('E', 75), (13, 7): ('R', 75), (14, 7): ('E', 75)}
        s.move(board, "Spieler2")

        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(77, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 110")
        del s

    def test_111(self):
        # Testfall 111 - Algorithmus: Zug am rechten Rand (senkrecht)
        s = Scrabble()
        # 8B TURNeNS
        board = {(7, 1): ('T', 75), (7, 2): ('U', 75), (7, 3): ('R', 75), (7, 4): ('N', 75), (7, 5): ('_', 75),
                 (7, 6): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # H8 .AUNIERE
        board = {(7, 1): ('T', 75), (7, 2): ('U', 75), (7, 3): ('R', 75), (7, 4): ('N', 75), (7, 5): ('_', 75),
                 (7, 6): ('N', 75), (7, 7): ('S', 75),
                 (8, 7): ('A', 75), (9, 7): ('U', 75), (10, 7): ('N', 75), (11, 7): ('I', 75),
                 (12, 7): ('E', 75), (13, 7): ('R', 75), (14, 7): ('E', 75)}
        s.move(board, "Spieler2")
        # 15E SUP.R
        board = {(7, 1): ('T', 75), (7, 2): ('U', 75), (7, 3): ('R', 75), (7, 4): ('N', 75), (7, 5): ('_', 75),
                 (7, 6): ('N', 75), (7, 7): ('S', 75),
                 (8, 7): ('A', 75), (9, 7): ('U', 75), (10, 7): ('N', 75), (11, 7): ('I', 75),
                 (12, 7): ('E', 75), (13, 7): ('R', 75), (14, 7): ('E', 75),
                 (14, 4): ('S', 75), (14, 5): ('U', 75), (14, 6): ('P', 75), (14, 8): ('R', 75)}
        s.move(board, "Spieler1")

        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(3, len(s.game))
        self.assertEqual(77, s.get_score("Spieler2"))
        self.assertEqual(72, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 111")
        del s

    def test_112(self):
        # Testfall 112 - Algorithmus: Anzweifeln ohne Zug
        s = Scrabble()
        try:
            s.valid_challenge()
        except Exception:
            pass
        else:
            self.fail("Test 112 Exception expected")
        del s

    def test_113(self):
        # Testfall 113 - Algorithmus: Anzweifeln ohne genug Punkte
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        s.invalid_challenge("Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        self.assertEqual(-10, s.get_score("Spieler2"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 113")
        del s

    def test_114(self):
        # Testfall 114 - Algorithmus: korrektes Anzweifeln
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        board = {}
        s.valid_challenge()
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(0, s.get_score("Spieler1"))
        self.assertEqual(0, s.get_score("Spieler2"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 114")
        del s

    def test_115(self):
        # Testfall 115 - Algorithmus: inkorrektes Anzweifeln
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 5G V.TEN
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        s.move(board, "Spieler2")
        s.invalid_challenge("Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(3, len(s.game))
        self.assertEqual(14, s.get_score("Spieler1"))
        self.assertEqual(20, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 115")
        del s

    def test_116(self):
        # Testfall 116 - Algorithmus: korrektes Anzweifeln - Board nicht geleert
        # diesen Testfall gibt's nicht mehr, da keine Analyse des Boards mehr
        # durchgeführt wird
        # s = Scrabble()
        # # H4 FIRNS
        # board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        # s.move(board, "Spieler1")
        # # 5G V.TEN
        # board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
        #          (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        # s.move(board, "Spieler2")
        # s.valid_challenge(board, "Spieler1")
        # logging.info(s.print_board(board, {}, {}))
        # logging.info(str(s))
        # self.assertEqual(2, len(s.game))
        # self.assertEqual(24, s.get_score("Spieler1"))
        # self.assertEqual(20, s.get_score("Spieler2"))
        # b = s.game[-1][s.DICT_BOARD]
        # expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        # cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        # self.assertEqual(cmp, expected, "Test 116")
        # del s
        pass

    def test_117(self):
        # Testfall 117 - Algorithmus: Anlegen an vorhandenem Wort
        s = Scrabble()
        # H5 TEST
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75)}
        s.move(board, "Spieler1")
        # H5 ....ER
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75),
                 (8, 7): ('E', 75), (9, 7): ('R', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(8, s.get_score("Spieler1"))
        self.assertEqual(6, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 117")
        del s

    def test_118(self):
        # Testfall 118 - Algorithmus: Anlegen zwischen zwei Worten
        s = Scrabble()
        # H5 TEST
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75)}
        s.move(board, "Spieler1")
        # 5H .AT
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75),
                 (4, 8): ('A', 75), (4, 9): ('T', 75)}
        s.move(board, "Spieler2")
        # 8H .UT
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75),
                 (4, 8): ('A', 75), (4, 9): ('T', 75),
                 (7, 8): ('U', 75), (7, 9): ('T', 75)}
        s.move(board, "Spieler1")
        # J5 .ES.
        board = {(4, 7): ('T', 75), (5, 7): ('E', 75), (6, 7): ('S', 75), (7, 7): ('T', 75),
                 (4, 8): ('A', 75), (4, 9): ('T', 75),
                 (7, 8): ('U', 75), (7, 9): ('T', 75),
                 (5, 9): ('E', 75), (6, 9): ('S', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(4, len(s.game))
        self.assertEqual(11, s.get_score("Spieler1"))
        self.assertEqual(9, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 118")
        del s

    def test_119(self):
        # Testfall 119 - Algorithmus: Berechnung doppelter Buchstabenwert
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(1, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 119")
        del s

    def test_120(self):
        # Testfall 120 - Algorithmus: Berechnung dreifacher Buchstabenwert
        s = Scrabble()
        # H4 TURNeNS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 6B SAUNIER.
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (5, 1): ('S', 75), (5, 2): ('A', 75), (5, 3): ('U', 75), (5, 4): ('N', 75), (5, 5): ('I', 75),
                 (5, 6): ('E', 75), (5, 8): ('E', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(62, s.get_score("Spieler2"))
        self.assertEqual(64, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 120")
        del s

    def test_121(self):
        # Testfall 121 - Algorithmus: Berechnung doppelter Wortwert
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 5G V.TEN
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        self.assertEqual(20, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 121")
        del s

    def test_122(self):
        # Testfall 122 - Algorithmus: Berechnung dreifacher Wortwert
        s = Scrabble()
        # H4 TURNeNS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8A SAUNIER.
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (7, 0): ('S', 75), (7, 1): ('A', 75), (7, 2): ('U', 75), (7, 3): ('N', 75), (7, 4): ('I', 75),
                 (7, 5): ('E', 75), (7, 6): ('R', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(74, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 122")
        del s

    def test_123(self):
        # Testfall 123 - Algorithmus: Berechnung doppelter Buchstabenwert (Blank auf dem Sonderfeld)
        s = Scrabble()
        # H4 fIRNS
        board = {(3, 7): ('_', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(1, len(s.game))
        self.assertEqual(8, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 123")
        del s

    def test_124(self):
        # Testfall 124 - Algorithmus: Berechnung dreifacher Buchstabenwert (Blank auf dem Sonderfeld)
        s = Scrabble()
        # H4 TURNENS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('E', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 6B sAUNiE.E
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('E', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (5, 1): ('_', 75), (5, 2): ('A', 75), (5, 3): ('U', 75), (5, 4): ('N', 75), (5, 5): ('_', 75),
                 (5, 6): ('E', 75), (5, 8): ('E', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(56, s.get_score("Spieler2"))
        self.assertEqual(66, s.get_score("Spieler1"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 124")
        del s

    def test_125(self):
        # Testfall 125 - Algorithmus: Berechnung doppelter Wortwert (Blank auf dem Sonderfeld)
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 5G V.TEn
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
                 (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('_', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        self.assertEqual(18, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 125")
        del s

    def test_126(self):
        # Testfall 126 - Algorithmus: Berechnung dreifacher Wortwert (Blank auf dem Sonderfeld)
        s = Scrabble()
        # H4 TURNeNS
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75)}
        s.move(board, "Spieler1")
        # 8A sAUNIER.
        board = {(3, 7): ('T', 75), (4, 7): ('U', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('_', 75),
                 (8, 7): ('N', 75), (9, 7): ('S', 75),
                 (7, 0): ('_', 75), (7, 1): ('A', 75), (7, 2): ('U', 75), (7, 3): ('N', 75), (7, 4): ('I', 75),
                 (7, 5): ('E', 75), (7, 6): ('R', 75)}
        s.move(board, "Spieler2")
        logging.info(s.print_board(board, {}, {}))
        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(64, s.get_score("Spieler1"))
        self.assertEqual(71, s.get_score("Spieler2"))
        b = s.game[-1][s.DICT_BOARD]
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(cmp, expected, "Test 126")
        del s

    def test_127(self):
        # Testfall 127 - Algorithmus: Buchstabe wird entfernt / nicht mehr erkannt (ohne Anzweifeln)
        return
        # s = Scrabble()
        # # H4 FIRNS
        # board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        # s.move(board, "Spieler1")
        # # 5G V.TEN
        # # F von FIRNS fehlt
        # board = {(4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
        #          (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        # s.move(board, "Spieler2")
        # logging.info(s.print_board(board, {}, {}))
        # logging.info(str(s))
        # self.assertEqual(2, len(s.game))
        # self.assertEqual(24, s.get_score("Spieler1"))
        # self.assertEqual(20, s.get_score("Spieler2"))
        # b = s.game[-1][s.DICT_BOARD]
        # expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        # cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        # self.assertEqual(cmp, expected, "Test 103")
        # del s

    def test_128(self):
        # Testfall 128 - Algorithmus: entfernter / nicht mehr erkannter Buchstabe wird wieder auf das Board gelegt
        return
        # s = Scrabble()
        # # H4 FIRNS
        # board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        # s.move(board, "Spieler1")
        # # 5G V.TEN
        # # F von FIRNS fehlt
        # board = {(4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
        #          (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75)}
        # s.move(board, "Spieler2")
        # # B8 GÄL.
        # # F von FIRNS ist wieder da
        # board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75),
        #          (4, 6): ('V', 75), (4, 8): ('T', 75), (4, 9): ('E', 75), (4, 10): ('N', 75),
        #          (1, 9): ('G', 75), (2, 9): ('Ä', 75), (3, 9): ('L', 75)}
        # s.move(board, "Spieler1")
        # logging.info(s.print_board(board, {}, {}))
        # logging.info(str(s))
        # self.assertEqual(3, len(s.game))
        # self.assertEqual(39, s.get_score("Spieler1"))
        # self.assertEqual(20, s.get_score("Spieler2"))
        # b = s.game[-1][s.DICT_BOARD]
        # expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        # cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        # self.assertEqual(cmp, expected, "Test 103")
        # del s

    def test_129(self):
        # Testfall 129 - Algorithmus: es werden nicht zusammenhängende Buchstaben gelegt
        s = Scrabble()
        # H4 FJRNS
        board = {(3, 7): ('F', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")

        logging.info(str(s))
        self.assertEqual(1, len(s.game))
        self.assertEqual(8, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 130")
        del s

    def test_130(self):
        # Testfall 130 - Algorithmus: ein abweichender Buchstabe wird mit einer höheren Wahrscheinlichkeit erkannt
        s = Scrabble()
        # H4 FJRNS
        board = {(3, 7): ('F', 75), (4, 7): ('J', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        self.assertEqual(34, s.get_score("Spieler1"))

        # j -> i
        board = {(3, 7): ('F', 75), (4, 7): ('I', 80), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler2")

        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 130")
        del s

    def test_131(self):
        # Testfall 131 - Algorithmus: statt Buchstabe wird jetzt ein Blank erkannt
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 75), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        self.assertEqual(24, s.get_score("Spieler1"))

        # i -> Blank
        board = {(3, 7): ('F', 75), (4, 7): ('_', 80), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler2")

        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(22, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 131")
        del s

    def test_132(self):
        # Testfall 132 - Algorithmus: ein abweichender Buchstabe wird mit einer niedrigeren Wahrscheinlichkeit erkannt
        s = Scrabble()
        # H4 FIRNS
        board = {(3, 7): ('F', 75), (4, 7): ('I', 85), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler1")
        self.assertEqual(24, s.get_score("Spieler1"))

        # i -> j
        board = {(3, 7): ('F', 75), (4, 7): ('J', 80), (5, 7): ('R', 75), (6, 7): ('N', 75), (7, 7): ('S', 75)}
        s.move(board, "Spieler2")

        logging.info(str(s))
        self.assertEqual(2, len(s.game))
        self.assertEqual(24, s.get_score("Spieler1"))
        expected = dict(zip(*[board.keys(), [t for (t, p) in board.values()]]))
        b = s.game[-1][s.DICT_BOARD]
        cmp = dict(zip(*[b.keys(), [t for (t, p) in b.values()]]))
        self.assertEqual(expected, cmp, "Test 132")
        del s

    def test_133(self):

        s = Scrabble()
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (7, 7): ('S', 89), (3, 7): ('M', 90), (5, 7): ('L', 87)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 5): ('M', 88), (5, 6): ('O', 95)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (5, 5): ('M', 89)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (6, 6): ('B', 88), (5, 5): ('M', 89)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (6, 6): ('B', 87),
                 (7, 6): ('E', 91), (4, 6): ('T', 94), (5, 5): ('M', 89)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (5, 5): ('M', 86), (6, 6): ('B', 88), (4, 5): ('A', 95),
                 (4, 8): ('M', 88)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (5, 9): ('Ö', 87), (6, 6): ('B', 88),
                 (5, 5): ('M', 89), (5, 11): ('E', 86), (4, 8): ('M', 91), (5, 10): ('S', 89)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (5, 5): ('M', 87),
                 (5, 9): ('Ö', 85), (5, 11): ('E', 86), (7, 10): ('I', 95), (7, 9): ('E', 90), (5, 10): ('S', 90),
                 (6, 6): ('B', 87), (7, 11): ('D', 90)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 9): ('Ö', 85), (5, 11): ('E', 88),
                 (5, 5): ('M', 87), (5, 12): ('N', 95), (6, 6): ('B', 88), (6, 12): ('E', 86), (7, 12): ('S', 91),
                 (3, 12): ('E', 89), (4, 12): ('I', 96), (2, 12): ('F', 89)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (3, 14): ('T', 89), (5, 9): ('Ö', 87), (3, 13): ('H', 86), (6, 6): ('B', 88),
                 (5, 5): ('M', 85), (5, 11): ('E', 88), (6, 12): ('E', 92), (3, 12): ('E', 91), (3, 11): ('G', 89),
                 (2, 12): ('F', 92)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (5, 9): ('Ö', 86),
                 (3, 14): ('T', 89), (6, 6): ('B', 88), (5, 11): ('E', 89), (5, 5): ('M', 87), (0, 14): ('H', 93),
                 (1, 14): ('E', 88), (2, 14): ('F', 89), (3, 11): ('G', 89), (3, 13): ('H', 86)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (5, 9): ('Ö', 87), (3, 14): ('T', 89), (6, 6): ('B', 88), (5, 11): ('E', 88), (5, 5): ('M', 87),
                 (3, 11): ('G', 88), (1, 14): ('E', 83), (2, 14): ('F', 87), (8, 9): ('S', 92), (9, 9): ('T', 95),
                 (3, 13): ('H', 87)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (5, 5): ('M', 87),
                 (5, 9): ('Ö', 86), (1, 14): ('E', 90), (5, 11): ('E', 89), (2, 14): ('F', 90), (6, 6): ('B', 86),
                 (3, 11): ('G', 92), (8, 3): ('A', 89), (3, 13): ('H', 85), (8, 4): ('C', 93)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (7, 3): ('J', 87), (5, 5): ('M', 85),
                 (5, 11): ('E', 88), (5, 9): ('Ö', 86), (9, 3): ('_', 96), (8, 3): ('A', 90), (6, 6): ('B', 88),
                 (10, 3): ('K', 87), (11, 3): ('E', 85), (3, 13): ('H', 87)}
        s.move(board, "Spieler2")
        # (5,9): ('Ö',87)
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (5, 5): ('M', 89), (9, 3): ('_', 96),
                 (5, 9): ('Q', 87),
                 (6, 6): ('B', 88), (11, 3): ('E', 83),
                 (10, 3): ('K', 87), (9, 5): ('Ü', 92), (3, 13): ('H', 86), (5, 11): ('E', 86)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (5, 9): ('Ö', 87), (5, 5): ('M', 86), (9, 3): ('_', 96), (6, 6): ('B', 88),
                 (10, 3): ('K', 85), (11, 3): ('E', 85), (3, 13): ('H', 86), (5, 11): ('E', 89)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (5, 11): ('E', 89), (5, 5): ('M', 89), (12, 1): ('E', 88),
                 (9, 3): ('_', 96), (12, 6): ('S', 91), (5, 9): ('Ö', 86), (12, 3): ('N', 91), (6, 6): ('B', 86),
                 (12, 5): ('R', 87), (10, 3): ('K', 89), (11, 3): ('E', 85), (12, 4): ('E', 86), (3, 13): ('H', 85)}
        s.move(board, "Spieler1")
        # (5,9): ('Ö',87)
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (5, 11): ('E', 87), (12, 1): ('E', 88), (9, 3): ('_', 96),
                 (5, 9): ('Q', 87),
                 (6, 6): ('B', 87),
                 (3, 13): ('H', 85), (12, 5): ('R', 90), (11, 3): ('E', 88), (10, 3): ('K', 89), (12, 4): ('E', 87)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (9, 3): ('_', 96), (12, 1): ('E', 88), (13, 1): ('Y', 92), (5, 9): ('Ö', 85),
                 (11, 3): ('E', 85), (12, 4): ('E', 86), (6, 6): ('B', 88), (3, 13): ('H', 86), (5, 11): ('E', 87),
                 (13, 0): ('N', 93), (10, 3): ('K', 88)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (12, 1): ('E', 86), (10, 11): ('E', 87),
                 (9, 3): ('_', 96), (5, 9): ('Ö', 86), (9, 11): ('V', 94), (11, 11): ('N', 90), (5, 11): ('E', 86),
                 (6, 6): ('B', 88), (10, 3): ('K', 90), (11, 3): ('E', 86), (3, 13): ('H', 87), (12, 4): ('E', 86),
                 (8, 11): ('I', 95)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (9, 3): ('_', 96), (10, 11): ('E', 88),
                 (5, 9): ('Ö', 87), (6, 6): ('B', 87), (5, 11): ('E', 89), (3, 5): ('U', 92), (2, 5): ('Q', 84),
                 (11, 3): ('E', 84), (12, 4): ('E', 88), (3, 13): ('H', 85)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 11): ('E', 88),
                 (5, 9): ('Ö', 88), (5, 11): ('E', 88), (6, 6): ('B', 87), (10, 5): ('T', 94), (10, 6): ('E', 91),
                 (2, 5): ('Q', 83), (10, 4): ('O', 94), (11, 3): ('E', 87), (3, 13): ('H', 85), (12, 4): ('E', 93),
                 (9, 3): ('_', 96)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 87), (10, 12): ('B', 88),
                 (9, 3): ('_', 96), (6, 6): ('B', 87), (5, 11): ('E', 86), (5, 9): ('Ö', 88), (2, 5): ('Q', 84),
                 (10, 10): ('L', 88), (11, 3): ('E', 85), (3, 13): ('H', 87)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (9, 3): ('_', 96), (6, 6): ('B', 85), (13, 13): ('D', 92), (5, 9): ('Ö', 85),
                 (11, 13): ('A', 93), (10, 13): ('T', 89), (5, 11): ('E', 88), (10, 10): ('L', 89), (2, 5): ('Q', 86),
                 (11, 3): ('E', 85), (3, 13): ('H', 86)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (5, 9): ('Ö', 87), (6, 6): ('B', 88),
                 (9, 3): ('_', 96), (14, 14): ('R', 88), (10, 13): ('T', 89), (5, 11): ('E', 88), (10, 10): ('L', 87),
                 (2, 5): ('Q', 85), (13, 14): ('U', 90), (3, 13): ('H', 85), (11, 3): ('E', 87)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (6, 6): ('B', 87), (9, 3): ('_', 96), (5, 9): ('Ö', 86), (14, 14): ('R', 90), (10, 13): ('T', 88),
                 (12, 10): ('K', 85), (5, 11): ('E', 88), (2, 5): ('Q', 84), (10, 10): ('L', 87), (11, 3): ('E', 84),
                 (3, 13): ('H', 87)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (6, 6): ('B', 88), (5, 9): ('Ö', 87), (9, 3): ('_', 96), (10, 0): ('G', 90),
                 (10, 13): ('T', 89), (12, 10): ('K', 84), (14, 0): ('S', 91), (5, 11): ('E', 87), (11, 0): ('A', 92),
                 (12, 0): ('R', 90), (2, 5): ('Q', 85), (10, 10): ('L', 87), (3, 13): ('H', 86), (11, 3): ('E', 85)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (5, 9): ('Ö', 88), (10, 10): ('L', 88), (2, 5): ('Q', 84), (6, 6): ('B', 87), (11, 3): ('E', 87),
                 (12, 10): ('K', 85), (12, 9): ('U', 91), (3, 13): ('H', 85), (5, 11): ('E', 86), (10, 13): ('T', 88),
                 (9, 3): ('_', 96), (12, 8): ('P', 92)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 6): ('Ä', 89), (5, 9): ('Ö', 87), (2, 5): ('Q', 85),
                 (10, 10): ('L', 88), (6, 6): ('B', 87), (13, 7): ('S', 91), (11, 3): ('E', 86), (12, 10): ('K', 83),
                 (3, 13): ('H', 86), (5, 11): ('E', 88), (10, 13): ('T', 89), (9, 3): ('_', 96)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 7): ('S', 91), (6, 14): ('U', 94), (13, 6): ('Ä', 90),
                 (5, 9): ('Ö', 88), (10, 10): ('L', 88), (2, 5): ('Q', 86), (6, 6): ('B', 87), (8, 14): ('Z', 90),
                 (11, 3): ('E', 86), (12, 10): ('K', 84), (11, 14): ('I', 87), (9, 14): ('W', 92), (3, 13): ('H', 86),
                 (7, 14): ('M', 88), (5, 11): ('E', 87), (10, 13): ('T', 92), (9, 3): ('_', 96), (10, 14): ('E', 84)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 7): ('S', 91), (6, 14): ('U', 94), (13, 6): ('Ä', 90),
                 (8, 14): ('Z', 90), (9, 14): ('W', 92), (10, 13): ('T', 92), (13, 4): ('X', 92), (5, 9): ('Ö', 86),
                 (10, 10): ('L', 88), (11, 3): ('E', 83), (6, 6): ('B', 88), (2, 5): ('Q', 84), (11, 14): ('I', 88),
                 (12, 10): ('K', 85), (7, 14): ('M', 89), (3, 13): ('H', 86), (5, 11): ('E', 86), (9, 3): ('_', 96),
                 (10, 14): ('E', 89)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 7): ('S', 91), (6, 14): ('U', 94), (13, 6): ('Ä', 90),
                 (8, 14): ('Z', 90), (9, 14): ('W', 92), (10, 13): ('T', 92), (13, 4): ('X', 92), (5, 9): ('Ö', 86),
                 (0, 11): ('R', 88), (10, 10): ('L', 88), (6, 6): ('B', 88), (2, 5): ('Q', 84), (11, 3): ('E', 83),
                 (12, 10): ('K', 85), (11, 14): ('I', 89), (3, 13): ('H', 86), (7, 14): ('M', 89), (0, 13): ('C', 92),
                 (0, 12): ('E', 86), (5, 11): ('E', 87), (9, 3): ('_', 96), (10, 14): ('E', 89)}
        s.move(board, "Spieler2")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 7): ('S', 91), (6, 14): ('U', 94), (13, 6): ('Ä', 90),
                 (8, 14): ('Z', 90), (9, 14): ('W', 92), (10, 13): ('T', 92), (13, 4): ('X', 92), (0, 13): ('C', 92),
                 (0, 11): ('R', 89), (14, 7): ('_', 96), (2, 5): ('Q', 84), (5, 9): ('Ö', 87), (14, 6): ('E', 89),
                 (6, 6): ('B', 89), (10, 10): ('L', 87), (12, 10): ('K', 85), (11, 3): ('E', 85), (3, 13): ('H', 86),
                 (11, 14): ('I', 88), (7, 14): ('M', 90), (5, 11): ('E', 84), (0, 12): ('E', 87), (9, 3): ('_', 96),
                 (10, 14): ('E', 88), (14, 8): ('N', 93)}
        s.move(board, "Spieler1")
        board = {(4, 7): ('U', 94), (6, 7): ('I', 92), (3, 7): ('M', 90), (5, 7): ('L', 91), (7, 7): ('S', 93),
                 (5, 6): ('O', 95), (6, 8): ('N', 96), (6, 9): ('D', 91), (8, 6): ('T', 94), (7, 6): ('E', 91),
                 (4, 6): ('T', 94), (4, 4): ('D', 90), (4, 5): ('A', 95), (4, 8): ('M', 91), (7, 10): ('I', 95),
                 (7, 9): ('E', 90), (5, 10): ('S', 90), (7, 11): ('D', 90), (5, 12): ('N', 95), (7, 12): ('S', 91),
                 (4, 12): ('I', 96), (6, 12): ('E', 92), (3, 12): ('E', 91), (2, 12): ('F', 92), (0, 14): ('H', 93),
                 (8, 9): ('S', 92), (9, 9): ('T', 95), (8, 5): ('H', 94), (3, 14): ('T', 94), (1, 14): ('E', 90),
                 (2, 14): ('F', 90), (3, 11): ('G', 92), (8, 4): ('C', 93), (8, 3): ('A', 90), (7, 3): ('J', 90),
                 (9, 5): ('Ü', 92), (12, 2): ('I', 92), (12, 6): ('S', 91), (12, 3): ('N', 91), (5, 5): ('M', 91),
                 (12, 5): ('R', 90), (13, 1): ('Y', 92), (13, 0): ('N', 93), (9, 11): ('V', 94), (11, 11): ('N', 90),
                 (10, 3): ('K', 90), (8, 11): ('I', 95), (12, 1): ('E', 90), (3, 5): ('U', 92), (10, 5): ('T', 94),
                 (10, 6): ('E', 91), (10, 4): ('O', 94), (12, 4): ('E', 93), (10, 11): ('E', 92), (12, 13): ('N', 93),
                 (10, 12): ('B', 91), (13, 13): ('D', 92), (11, 13): ('A', 93), (13, 14): ('U', 90),
                 (11, 10): ('O', 92),
                 (14, 14): ('R', 90), (10, 0): ('G', 90), (14, 0): ('S', 91), (11, 0): ('A', 92), (12, 0): ('R', 90),
                 (12, 9): ('U', 91), (12, 8): ('P', 92), (13, 7): ('S', 91), (6, 14): ('U', 94), (13, 6): ('Ä', 90),
                 (8, 14): ('Z', 90), (9, 14): ('W', 92), (10, 13): ('T', 92), (13, 4): ('X', 92), (0, 13): ('C', 92),
                 (7, 14): ('M', 90), (14, 8): ('N', 93), (1, 5): ('E', 87), (14, 7): ('_', 96), (1, 6): ('L', 90),
                 (1, 7): ('N', 96), (0, 11): ('R', 87), (2, 5): ('Q', 89), (5, 9): ('Ö', 87), (1, 1): ('H', 89),
                 (6, 6): ('B', 85), (14, 6): ('E', 88), (10, 10): ('L', 90), (1, 2): ('A', 90), (11, 3): ('E', 88),
                 (1, 3): ('R', 91), (12, 10): ('K', 84), (3, 13): ('H', 85), (5, 11): ('E', 89), (11, 14): ('I', 87),
                 (1, 4): ('R', 93), (9, 3): ('_', 96), (0, 12): ('E', 87), (10, 14): ('E', 89)}
        s.move(board, "Spieler2")
        logging.info(str(s))
        self.assertEqual(34, len(s.game))
        self.assertEqual(347, s.get_score("Spieler1"))
        self.assertEqual(360, s.get_score("Spieler2"))


if __name__ == '__main__':
    unittest.main()
