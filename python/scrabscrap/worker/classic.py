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
import threading

import cv2
import imutils

from board import tiles
from board.board import get_x_position, get_y_position, GRID_W, GRID_H


class WorkerClassic(threading.Thread):

    def __init__(self, q):
        self.__queue = q
        threading.Thread.__init__(self)
        self.setDaemon(True)

    @staticmethod
    def __find_tile(col, row, gray, _board, blank_candidates):

        def __match(img, suggest_tile, suggest_prop):
            for _tile in tiles.tiles:
                res = cv2.matchTemplate(img, _tile.img, cv2.TM_CCOEFF_NORMED)
                _, thresh, _, _ = cv2.minMaxLoc(res)
                if thresh > (suggest_prop / 100):
                    suggest_tile = _tile.name
                    suggest_prop = int(thresh * 100)
            return suggest_tile, suggest_prop

        if (col, row) in _board:
            tile, prop = _board[(col, row)]
        else:
            tile, prop = None, 76
        if prop > 90:
            logging.debug("{}{:2}: tile on board prop > 90 {} ({})".format(chr(ord('A') + col), row + 1, tile, prop))
            return _board[(col, row)]
        y = get_y_position(row)
        x = get_x_position(col)
        test = gray[y - 10:y + GRID_H + 10, x - 10:x + GRID_W + 10]
        tile, prop = __match(test, tile, prop)
        if prop < 90:
            img_r = imutils.rotate(test, -10)
            tile, prop = __match(img_r, tile, prop)
        if prop < 90:
            img_r = imutils.rotate(test, 10)
            tile, prop = __match(img_r, tile, prop)
        if tile is None and (col, row) in blank_candidates:
            tile, prop = blank_candidates[(col, row)]
        if tile is None:
            return '/', prop
        _board[(col, row)] = (tile, prop)
        return _board[(col, row)]

    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                self.__queue.task_done()
                break  # reached end of queue
            col = item[0][0]
            row = item[0][1]
            img = item[1]
            _board = item[2]
            blank_candidates = item[3]
            tile, prop = self.__find_tile(col, row, img, _board, blank_candidates)
            self.__queue.task_done()
            logging.debug("{}{:2}: {} ({:2}) task finished".format(chr(ord('A') + col), row + 1, tile, prop))
