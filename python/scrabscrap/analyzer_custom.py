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
import datetime
import logging
import logging.config
import queue

import cv2
import imutils
import numpy as np
from vlogging import VisualRecord

from board.board import overlay_grid, overlay_tiles, get_x_position, get_y_position, GRID_W, GRID_H
from worker.custom import WorkerCustom

WORKERS = 4
visualLogger = logging.getLogger("visualLogger")

last_warp = None


class AnalyzerCustom:
    def __init__(self, _img=None, _board=None):
        self.img = _img
        if _board is None:
            self.board = dict()
        else:
            self.board = _board
        self.gray = None
        self.warped = None

    @staticmethod
    def _warp(__image):
        global last_warp

        warp = configparser.ConfigParser()
        warp.read('warp.ini')
        if warp.has_section('warp'):
            rect = np.zeros((4, 2), dtype="float32")
            rect[0][0] = warp['warp']['top-left-x']
            rect[0][1] = warp['warp']['top-left-y']
            rect[1][0] = warp['warp']['top-right-x']
            rect[1][1] = warp['warp']['top-right-y']
            rect[2][0] = warp['warp']['bottom-right-x']
            rect[2][1] = warp['warp']['bottom-right-y']
            rect[3][0] = warp['warp']['bottom-left-x']
            rect[3][1] = warp['warp']['bottom-left-y']
            logging.debug("warp.ini {}".format(rect))
        else:
            # based on: https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
            (blue, _, _) = cv2.split(__image.copy())

            # Otsu's thresholding after Gaussian filtering
            blur = cv2.GaussianBlur(blue, (5, 5), 0)
            ret3, th3 = cv2.threshold(
                blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
            dilated = cv2.dilate(th3, kernel)

            cnts = cv2.findContours(
                dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:1]
            c = cnts[0]
            peri = 1
            approx = cv2.approxPolyDP(c, peri, True)
            while len(approx) > 4:
                peri += 1
                approx = cv2.approxPolyDP(c, peri, True)

            pts = approx.reshape(4, 2)
            rect = np.zeros((4, 2), dtype="float32")

            # the top-left point has the smallest sum whereas the
            # bottom-right has the largest sum
            s = pts.sum(axis=1)
            rect[0] = pts[np.argmin(s)]
            rect[2] = pts[np.argmax(s)]

            # compute the difference between the points -- the top-right
            # will have the minimum difference and the bottom-left will
            # have the maximum difference
            diff = np.diff(pts, axis=1)
            rect[1] = pts[np.argmin(diff)]
            rect[3] = pts[np.argmax(diff)]
            logging.debug("warp calculation {}".format(rect))

            # evtl. auch nur eine Heuristik bzgl. der Abweichungen der Ecken?
            (x1, y1) = rect[0]
            (w1, y2) = rect[1]
            (w2, h1) = rect[2]
            (x2, h2) = rect[3]
            if abs(x1 - x2) > 40 or x1 < 15 or x2 < 15:
                if last_warp is not None:
                    rect[0][0] = last_warp[0][0]
                    rect[3][0] = last_warp[3][0]
                else:
                    x = max(x1, x2)
                    rect[0][0] = rect[3][0] = x
                    logging.warning("korrigiere x auf {}".format(x))
            if abs(w1 - w2) > 40 or w1 > 1490 or w2 > 1490:
                if last_warp is not None:
                    rect[1][0] = last_warp[1][0]
                    rect[2][0] = last_warp[2][0]
                else:
                    w = min(w1, w2)
                    rect[1][0] = rect[2][0] = w
                    logging.warning("korrigiere w auf {}".format(w))
            if abs(y1 - y2) > 40 or y1 < 15 or y2 < 15:
                if last_warp is not None:
                    rect[0][1] = last_warp[0][1]
                    rect[1][1] = last_warp[1][1]
                else:
                    y = max(y1, y2)
                    rect[0][1] = rect[1][1] = y
                    logging.warning("korrigiere y auf {}".format(y))
            if abs(h1 - h2) > 40 or h1 > 1490 or h2 > 1490:
                if last_warp is not None:
                    rect[2][1] = last_warp[2][1]
                    rect[3][1] = last_warp[3][1]
                else:
                    h = min(h1, h2)
                    rect[2][1] = rect[3][1] = h
                    logging.warning("korrigiere h auf {}".format(h))

            # if abs(x1 - x2) > 40 or abs(w1 - w2) > 40 or abs(y1 - y2) > 40 or abs(h1 - h2) > 40:
            #     # or x1 < 15 or y1 < 15 \
            #     #     or w1 > 1485 or y2 < 15 or w2 > 1485 or h1 > 1485 or x2 < 15 or h2 > 1485:
            #     if last_warp is not None:
            #         rect = last_warp
            #     else:
            #         logging.error("es kann keine sinnvolle Transformation ermittelt werden")
            #     logging.warning("korrigiere rest auf {}".format(rect))
            # else:
            last_warp = rect

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [800, 0],
            [800, 800],
            [0, 800]], dtype="float32")

        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        m = cv2.getPerspectiveTransform(rect, dst)
        result = cv2.warpPerspective(__image, m, (800, 800))
        visualLogger.debug(VisualRecord("warp_custom", [result], fmt="png"))
        return result

    @staticmethod
    def _prepare_grid_image(_image):
        # Farbmodell LAB, 100px
        tmp_img = cv2.GaussianBlur(_image, (7, 7), 0)
        tmp_img = cv2.resize(tmp_img, (200, 200), interpolation=cv2.INTER_AREA)
        lab = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2LAB)
        _, a, b = cv2.split(lab)
        image = cv2.merge((a, b))
        image = image.reshape((200 * 200, 2))
        image = np.float32(image)

        # Color Quantization
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 8, 2.0)
        k = 4
        _, labels_, _ = cv2.kmeans(image, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        clustering = np.reshape(np.array(labels_, dtype=np.uint8), (200, 200))
        # Sort the cluster labels in order of the frequency with which they occur.
        sorted_labels = sorted([n for n in range(k)], key=lambda _x: -np.sum(clustering == _x))
        # Initialize K-means grayscale image; set pixel colors based on clustering.
        kmeans_image = np.zeros((200, 200), dtype=np.uint8)
        for i, label in enumerate(sorted_labels):
            kmeans_image[clustering == label] = int(255 / (k - 1)) * i * 50

        # Farbe des Mittelsteines
        y = 94  # 47  # (3,125 + (7*6,25)
        x = 94  # 47  # (3,125 + (7*6,25)
        field = kmeans_image[y:y + 12, x:x + 12]
        a, cnts = np.unique(field, return_counts=True)
        high_freq_element = a[cnts.argmax()]
        kmeans_image[kmeans_image != high_freq_element] = 0

        # auf gesamte Fläche ausdehnen
        set_of_tiles = set()
        for row in range(0, 15):
            for col in range(0, 15):
                y = int(6.25 + (row * 12.5))
                x = int(6.25 + (col * 12.5))
                field = kmeans_image[y:y + 12, x:x + 12]
                a, cnts = np.unique(field, return_counts=True)
                if a[cnts.argmax()] != 0:
                    logging.debug("{}{:2}: {} ".format(chr(ord('A') + row), col + 1, cnts))
                    set_of_tiles.add((col, row))

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug("{}".format(sorted_labels))
            logging.debug("tiles: {}".format(set_of_tiles))
            out = "\n {:2} ".format(' ')
            for col in range(0, 15):
                out += " {:2} ".format(col + 1)
            out += '\n'
            for row in range(0, 15):
                out += " {:2} ".format(chr(ord('A') + row))
                for col in range(0, 15):
                    if (col, row) in set_of_tiles:
                        out += "  X "
                    else:
                        out += "  . "
                out += '\n'
            logging.debug(out)
            visualLogger.debug(VisualRecord("kmeans", [kmeans_image], fmt="jpg"))

        # kein Wort gelegt
        if (6, 7) not in set_of_tiles and \
                (7, 6) not in set_of_tiles and \
                (8, 7) not in set_of_tiles and \
                (7, 8) not in set_of_tiles:
            return {}
        return set_of_tiles

    def _mark_grid(self, _queue, _coord, _candidat, _ignore):
        (_c, _r) = _coord
        if _coord not in _candidat:
            return
        _candidat.remove(_coord)
        if _coord not in _ignore:
            _y = get_y_position(_r)
            _x = get_x_position(_c)
            _gray = self.gray[_y - 10:_y + GRID_H + 10, _x - 10:_x + GRID_W + 10]
            _queue.put((_coord, _gray, self.board), block=False)
        self._mark_grid(_queue, (_c + 1, _r), _candidat, _ignore)
        self._mark_grid(_queue, (_c - 1, _r), _candidat, _ignore)
        self._mark_grid(_queue, (_c, _r + 1), _candidat, _ignore)
        self._mark_grid(_queue, (_c, _r - 1), _candidat, _ignore)

    def analyze(self, image=None, must_warp=True, last_board=None, ignore_board=None):
        _start = datetime.datetime.now()
        self.img = image
        if self.img is None:
            raise ValueError("img darf nicht None sein")
        self.board = last_board if last_board is not None else {}
        if ignore_board is None:
            ignore_board = {}
        if len(self.board) < 1:
            global last_warp
            last_warp = None

        self.warped = self._warp(self.img) if must_warp else self.img
        self.gray = cv2.cvtColor(self.warped, cv2.COLOR_BGR2GRAY)

        set_of_tiles = self._prepare_grid_image(self.warped)

        q = queue.Queue(0)
        for _ in range(WORKERS):
            WorkerCustom(q).start()  # start a worker

        self._mark_grid(q, (7, 7), set_of_tiles.copy(), ignore_board)
        for _ in range(WORKERS):
            q.put(None)  # add end-of-queue markers

        q.join()

        if logging.DEBUG >= visualLogger.level:
            _mark = overlay_grid(self.warped)
            _mark = overlay_tiles(_mark, board=self.board)
            visualLogger.debug(VisualRecord("marked", [_mark], fmt="jpg"))
        logging.info("timer analyze: {} sec".format(datetime.datetime.now() - _start))
        return self.board, self.warped
