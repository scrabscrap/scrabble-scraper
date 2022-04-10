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
import logging
import re
from enum import Enum

from board import board, tiles
from config import MALUS_DOUBT

visualLogger = logging.getLogger("visualLogger")
# regex für gcg
GCG_NICKNAME1 = re.compile("^#player1\\s+(\\w+)\\s+.*$")
GCG_NICKNAME2 = re.compile("^#player2\\s+(\\w+)\\s+.*$")
GCG_HEADER = re.compile("^#.*$")
GCG_MOVE = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+([A-Oa-o0-9]+)\\s+([\\w\\?\\.]+)\\s+(\\+?\\d+)\\s(\\d+)\\s*$")
GCG_PASS = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+(\\-)\\s+(\\+?\\d+)\\s+(\\d+)\\s*$")
GCG_EXCHANGE = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+(\\-[\\w\\?]+)\\s+(\\+?\\d+)\\s(\\d+)\\s*$")
GCG_WITHDRAW = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+(\\-\\-)\\s+(\\-\\d+)\\s+(\\d+)\\s*$")
GCG_CHALLENGE = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+(\\([\\w\\?]+\\))\\s+(\\+?\\d+)\\s+(\\d+)\\s*$")
GCG_SCORE_OPP = re.compile("^>(\\w+):\\s+\\(([\\w\\?]+)\\)\\s+(\\+?\\d+)\\s+(\\d+)\\s*$")
GCG_SCORE_RACK = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+\\(([\\w\\?]+)\\)\\s+(\\-\\d+)\\s+(\\d+)\\s*$")
GCG_SCORE_TIME = re.compile("^>(\\w+):\\s+([\\w\\?]+)\\s+(\\(time\\))\\s+(\\-\\d+)\\s+(\\d+)\\s*$")

GCG_COORD_V = re.compile("([A-Oa-o])(\\d+)")
GCG_COORD_H = re.compile("(\\d+)([A-Oa-o])")


class MoveType(Enum):
    regular = 1
    pass_turn = 2
    exchange = 3
    withdraw = 4
    challenge_bonus = 5
    last_rack_bonus = 6
    last_rack_malus = 7
    time_malus = 8
    unknown = 9


class Move:

    def __init__(self, _board=None, nickname=None):
        self.type = None
        self.nickname = nickname
        self.row = None
        self.col = None
        self.is_vertical = None
        self.coord = None
        self.word = None
        self.score = 0
        self.sum = 0
        self.board = _board
        self.exchange = None
        self.rack = None
        self.opp_rack = None

    def __str__(self):
        result = ">" + self.nickname + ": "
        if self.type != MoveType.last_rack_bonus:
            result += (self.rack + " ") if self.rack is not None else ""
        if self.type == MoveType.regular:
            result += str(self.col + 1) + chr(ord('A') + self.row) if self.is_vertical else chr(
                ord('A') + self.row) + str(self.col + 1)
            result += " " + self.word + " "
        elif self.type == MoveType.pass_turn:
            result += "- "
        elif self.type == MoveType.exchange:
            result += "-" + self.exchange + " "
        elif self.type == MoveType.withdraw:
            result += "-- "
        elif self.type == MoveType.last_rack_bonus:
            result += "(" + self.opp_rack + ") "
        elif self.type == MoveType.last_rack_malus:
            result += "(" + self.rack + ") "
        elif self.type == MoveType.challenge_bonus:
            result += "(challenge) "
        elif self.type == MoveType.time_malus:
            result += "(time) "
        elif self.type == MoveType.unknown:
            result += "(unknown) "
        result += "{:+d} {:+d}".format(self.score, self.sum)
        return result

    def set_from_string(self, line):
        m = GCG_MOVE.match(line)
        if m is not None:
            self.type = MoveType.regular
            self.nickname = m.group(1)
            self.rack = m.group(2)
            self.coord = m.group(3)
            self.word = m.group(4)
            self.score = int(m.group(5))
            self.sum = int(m.group(6))
            self.is_vertical, self.row, self.col = self.__get_coord(self.coord)
            return
        m = GCG_PASS.match(line)
        if m is not None:
            self.type = MoveType.pass_turn
            self.nickname = m.group(1)
            return
        m = GCG_EXCHANGE.match(line)
        if m is not None:
            self.type = MoveType.exchange
            self.nickname = m.group(1)
            self.exchange = m.group(2)
            return
        m = GCG_WITHDRAW.match(line)
        if m is not None:
            self.type = MoveType.withdraw
            self.nickname = m.group(1)
            self.score = int(m.group(4))
            self.sum = int(m.group(5))
            return
        m = GCG_CHALLENGE.match(line)
        if m is not None:
            self.type = MoveType.challenge_bonus
            self.nickname = m.group(1)
            self.score = int(m.group(4))
            self.sum = int(m.group(5))
            return
        m = GCG_SCORE_OPP.match(line)
        if m is not None:
            self.type = MoveType.last_rack_bonus
            self.nickname = m.group(1)
            self.opp_rack = m.group(2)
            self.score = int(m.group(3))
            self.sum = int(m.group(4))
            return
        m = GCG_SCORE_TIME.match(line)
        if m is not None:
            self.type = MoveType.time_malus
            self.nickname = m.group(1)
            self.score = int(m.group(3))
            self.sum = int(m.group(4))
            return
        m = GCG_SCORE_RACK.match(line)
        if m is not None:
            self.type = MoveType.last_rack_malus
            self.nickname = m.group(1)
            self.score = int(m.group(3))
            self.sum = int(m.group(4))
            return

    def set_from_board(self, vertical, row, col, word):
        self.type = MoveType.regular
        self.row = row
        self.col = col
        self.is_vertical = vertical
        self.word = word
        self.rack = None

    def calc_score(self):
        def crossing_points(_row, _col):
            x = _col
            y = _row
            word = ""
            if self.is_vertical:
                while x > 0 and (x - 1, y) in self.board:
                    x -= 1
                while x < 15 and (x, y) in self.board:
                    word += self.board[(x, y)][0]
                    x += 1
            else:
                while y > 0 and (x, y - 1) in self.board:
                    y -= 1
                while y < 15 and (x, y) in self.board:
                    word += self.board[(x, y)][0]
                    y += 1
            if len(word) > 1:
                xval = sum([tiles.scores[letter] for letter in word])
                if (_col, _row) in board.DOUBLE_LETTER:
                    xval += tiles.scores[self.board[(_col, _row)][0]]
                elif (_col, _row) in board.TRIPLE_LETTER:
                    xval += tiles.scores[self.board[(_col, _row)][0]] * 2
                elif (_col, _row) in board.DOUBLE_WORDS:
                    xval *= 2
                elif (_col, _row) in board.TRIPLE_WORDS:
                    xval *= 3
                return xval
            return 0

        if self.board is None or self.type is not MoveType.regular:
            return 0
        val = 0
        crossing_words = 0
        letter_bonus = 0
        word_bonus = 1
        row = self.row
        col = self.col
        for i in range(len(self.word)):
            if self.board[(col, row)] is None:
                # Stein liegt nicht mehr auf dem Board
                continue
            if self.is_vertical:
                row = self.row + i
            else:
                col = self.col + i
            if self.word[i] != '.':
                # crossing word
                crossing_words += crossing_points(row, col)
                # check for bonus
                if (col, row) in board.DOUBLE_LETTER:
                    letter_bonus += tiles.scores[self.board[(col, row)][0]]
                elif (col, row) in board.TRIPLE_LETTER:
                    letter_bonus += tiles.scores[self.board[(col, row)][0]] * 2
                elif (col, row) in board.DOUBLE_WORDS:
                    word_bonus *= 2
                elif (col, row) in board.TRIPLE_WORDS:
                    word_bonus *= 3
                val += tiles.scores[self.board[(col, row)][0]]
            else:
                # zaehle den Wert des Steines
                val += tiles.scores[self.board[(col, row)][0]]
        val += letter_bonus
        val *= word_bonus
        val += crossing_words
        # falls 7 Steine, dann +50 Punkte
        if len(list(filter(lambda x: x != '.', self.word))) >= 7:
            val += 50
        self.score = val
        return val

    @staticmethod
    def __get_coord(value):
        if value is None:
            return None, None, None
        m = GCG_COORD_H.match(value)
        if m is not None:
            col = int(m.group(1)) - 1
            row = int(ord(m.group(2).capitalize()) - ord('A'))
            return True, row, col
        m = GCG_COORD_V.match(value)
        if m is not None:
            col = int(m.group(2)) - 1
            row = int(ord(m.group(1).capitalize()) - ord('A'))
            return False, row, col
        return None, None, None


class Scrabble:
    DICT_IMG = 0
    DICT_BOARD = 1
    DICT_MOVE = 2
    DICT_REMOVE = 3
    DICT_CHANGED = 4

    player = ["Spieler1", "Spieler2"]
    header = []  # für die GCG Datei
    game = []  # img, dict(board), Move, dict(remove), dict(changed)

    def __init__(self):
        self.header = []
        self.game = []

    def __str__(self):
        result = "\n"
        for s in self.header:
            result += s + "\n"
        for g in self.game:
            result += str(g[self.DICT_MOVE]) + "\n"
        return result

    @staticmethod
    def print_board(_board, new_tiles, removed_tiles):
        result = "Board:\n\n"
        result += "  |"
        for i in range(0, 15):
            result += "{:2d} ".format(i + 1)
        result += " | "
        for i in range(0, 15):
            result += "{:2d} ".format(i + 1)
        result += "\n"
        for y in range(0, 15):
            result += chr(ord('A') + y) + " |"
            for x in range(0, 15):
                if (x, y) in _board:
                    result += "[" if (x, y) in new_tiles else " "
                    result += _board[(x, y)][0]
                    result += "]" if (x, y) in new_tiles else " "
                else:
                    result += "-" if (x, y) in removed_tiles else " "
                    result += "."
                    result += "-" if (x, y) in removed_tiles else " "
            result += " | "
            for x in range(0, 15):
                if (x, y) in _board:
                    result += " " + str(_board[(x, y)][1])
                else:
                    result += " . "
            result += " | "
            result += "\n"
        return result

    def read_gcg_file(self, filename):
        file = open(filename, encoding="ISO-8859-1")
        for line in file:
            line = line.strip()
            if len(line) <= 0:
                continue
            m = GCG_NICKNAME1.match(line)
            if m is not None:
                self.header.append(line)
                # self.nick1 = m.group(0)
                continue
            m = GCG_NICKNAME2.match(line)
            if m is not None:
                self.header.append(line)
                # self.nick2 = m.group(0)
                continue
            m = GCG_HEADER.match(line)
            if m is not None:
                self.header.append(line)
                continue
            move = Move()
            move.set_from_string(line)
            _board = self.game[-1][self.DICT_BOARD].copy() if len(self.game) > 0 else {}
            if move.type == MoveType.regular:
                for i in range(0, len(move.word)):
                    if move.word[i] != '.':
                        if move.is_vertical:
                            _board[(move.col, move.row + i)] = (move.word[i], 99)
                        else:
                            _board[(move.col + i, move.row)] = (move.word[i], 99)
            elif move.type == MoveType.withdraw:
                prev_move = self.game[-1][self.DICT_MOVE]
                for i in range(0, len(prev_move.word)):
                    if prev_move.word[i] != '.':
                        if move.is_vertical:
                            del _board[(prev_move.col, prev_move.row + i)]
                        else:
                            del _board[(prev_move.col + i, prev_move.row)]
            self.game.append((None, _board, move, {}, {}))
        file.close()

    def get_score(self, nickname):
        cnt = len(self.game) - 1
        if cnt < 0:
            return 0
        while cnt >= 0:
            if nickname == self.game[cnt][self.DICT_MOVE].nickname:
                return self.game[cnt][self.DICT_MOVE].sum
            cnt -= 1
        return 0

    def correct_tiles(self, _board, _changed):
        calc = False
        sums = {}
        for g in self.game:
            m = g[self.DICT_MOVE]
            if m.nickname not in sums.keys():  # ein neuer nickname
                sums[m.nickname] = 0
            for t in _changed:
                if t in g[self.DICT_BOARD]:
                    calc = True
                    # dieser Stein (t) auf dem Board (g) vorhanden
                    logging.info("korrigiere {:s}:{:d}".format(chr(ord('A') + t[1]), t[0] + 1))
                    logging.debug("im Zug " + str(g[self.DICT_MOVE]))
                    g[self.DICT_BOARD][t] = _changed[t]
                    m.board[t] = _changed[t]
            if calc:
                w = ""
                if m.word:
                    for i in range(0, len(m.word)):
                        if m.word[i] == '.':
                            w += '.'
                        elif m.is_vertical:
                            w += m.board[(m.col, m.row + i)][0]
                        else:
                            w += m.board[(m.col + i, m.row)][0]
                logging.info("correct word:" + w)
                m.word = w
            m.score = m.calc_score()
            sums[m.nickname] += m.score
            m.sum = sums[m.nickname]

    def _prepare_board(self, new_board):
        cur_board = {} if len(self.game) < 1 else self.game[-1][self.DICT_BOARD]
        for i in cur_board.keys():
            if i in new_board.keys() and cur_board[i][1] > new_board[i][1]:
                logging.debug("nehme den besseren Wert des alten Boards {}".format(str(i)))
                new_board[i] = cur_board[i]
        new_tiles = {i: new_board[i] for i in set(new_board.keys()).difference(cur_board)}
        removed_tiles = {i: cur_board[i] for i in set(cur_board.keys()).difference(new_board)}
        changed_tiles = {i: new_board[i] for i in cur_board if
                         i not in removed_tiles and cur_board[i][0] != new_board[i][0]}
        logging.info(self.print_board(new_board, new_tiles, removed_tiles))
        if len(changed_tiles) > 0:
            logging.debug("changed tiles:" + str(changed_tiles))
            self.correct_tiles(new_board, changed_tiles)
        return new_board, new_tiles, removed_tiles, changed_tiles

    def move(self, new_board, nickname):

        def find_word(_board, changed):
            horizontal = len(set([x for x, _ in changed])) > 1
            vertical = len(set([y for _, y in changed])) > 1
            if len(changed) == 1:
                (x, y) = changed[-1]
                if x - 1 >= 0 and (x - 1, y) in _board:
                    horizontal = True
                elif x + 1 <= 14 and (x + 1, y) in _board:
                    horizontal = True
                elif y - 1 >= 0 and (x, y - 1) in _board:
                    vertical = True
                elif y + 1 <= 14 and (x, y + 1) in _board:
                    vertical = True
            elif len(changed) < 1:
                horizontal = True
            if vertical and horizontal:
                logging.warning("illegal move: {}".format(changed))
                raise Exception("move: neue Steine sowohl in abweichenden Spalten und Zeilen (illegaler Zug)")
            (x, y) = changed[0]
            minx = x
            miny = y
            _word = ""
            if vertical:
                while y > 0 and (x, y - 1) in _board:
                    y -= 1
                miny = y
                while y < 15 and (x, y) in _board:
                    _word += _board[(x, y)][0] if (x, y) in changed else '.'
                    y += 1
            else:
                while x > 0 and (x - 1, y) in _board:
                    x -= 1
                minx = x
                while x < 15 and (x, y) in _board:
                    _word += _board[(x, y)][0] if (x, y) in changed else '.'
                    x += 1
            return vertical, (minx, miny), _word

        start = datetime.datetime.now()
        if len(new_board) == 1 and new_board[(7, 7)][0] == '_':
            new_board = {}
        new_board, new_tiles, removed_tiles, changed_tiles = self._prepare_board(new_board)
        move = Move(new_board.copy(), nickname)
        # TODO: new_tiles dürfen nur aus den vorhandenen Steinen des bag kommen
        if len(new_tiles) <= 0:
            # Wechsel
            move.type = MoveType.exchange
            move.exchange = ""
            move.sum = self.get_score(nickname)
        else:
            try:
                v, (col, row), word = find_word(new_board, sorted(new_tiles))
                move.set_from_board(v, row, col, word)
                move.sum = move.calc_score() + self.get_score(nickname)
            except Exception:
                move.type = MoveType.unknown
                move.sum = self.get_score(nickname)
                move.score = -1
        self.game.append((None, new_board, move, removed_tiles, changed_tiles))
        logging.info("scrabble: move - time: {}".format(datetime.datetime.now() - start))

    def valid_challenge(self):
        start = datetime.datetime.now()
        if len(self.game) < 1:
            raise Exception("anzweifeln: kann nicht als erster Zug verwendet werden")
        # angezweifelter Zug
        last_move = self.game[-1][self.DICT_MOVE]
        if last_move.type not in (MoveType.regular, MoveType.challenge_bonus):
            logging.info("scrabble: double valid_challenge - time: {}".format(datetime.datetime.now() - start))
            return
        # Zustand des Bretts vor dem letzten Zug (vor dem ersten Zug leer)
        last_board = {} if len(self.game) < 2 else self.game[-2][self.DICT_BOARD]
        new_board, new_tiles, removed_tiles, changed_tiles = self._prepare_board(last_board)
        move = Move(last_board.copy(), last_move.nickname)
        move.type = MoveType.withdraw
        move.score = -last_move.score
        move.is_vertical = last_move.is_vertical
        move.word = last_move.word
        move.sum = last_move.sum - last_move.score
        self.game.append((None, new_board, move, removed_tiles, changed_tiles))
        logging.info("scrabble: challenge - time: {}".format(datetime.datetime.now() - start))

    def invalid_challenge(self, nickname):
        start = datetime.datetime.now()
        if len(self.game) < 1:
            raise Exception("anzweifeln: kann nicht als erster Zug verwendet werden")
        last_move = self.game[-1][self.DICT_MOVE]
        if last_move.type not in (MoveType.regular, MoveType.challenge_bonus):
            logging.info("scrabble: invalid_challenge not allowed - time: {}".format(datetime.datetime.now() - start))
            return
        last_board = self.game[-1][self.DICT_BOARD]
        logging.debug("scrabble: analyse invalid challenge")
        move = Move(last_board.copy(), nickname)
        move.type = MoveType.challenge_bonus
        move.score = -MALUS_DOUBT
        move.sum = self.get_score(nickname) - MALUS_DOUBT
        move.word = ""
        self.game.append((None, last_board, move, {}, {}))
        logging.info("scrabble: invalid_challenge - time: {}".format(datetime.datetime.now() - start))

    def reset(self):
        self.game.clear()
        self.header.clear()
        self.player = ["Spieler1", "Spieler2"]
        logging.info("scrabble: reset game")
