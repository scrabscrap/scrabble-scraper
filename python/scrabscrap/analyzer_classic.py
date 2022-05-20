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
import logging.config
import queue
import time

import cv2
import imutils
import numpy as np
from vlogging import VisualRecord

from board.board import overlay_grid, overlay_tiles, get_y_position, get_x_position, GRID_H, GRID_W
from worker.classic import WorkerClassic

WORKERS = 4
visualLogger = logging.getLogger("visualLogger")


class AnalyzerClassic:
    def __init__(self, _img=None, _board=None):
        self.img = _img
        if _board is None:
            self.board = dict()
        else:
            self.board = _board
        self.bgr = None
        self.gray = None
        self.warped = None

    @staticmethod
    def warp(__image):
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
        # will have the minumum difference and the bottom-left will
        # have the maximum difference
        diff = np.diff(pts, axis=1)
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]
        # now that we have our rectangle of points, let's compute
        # the width of our new image
        (tl, tr, br, bl) = rect
        width_a = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        width_b = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))

        # ...and now for the height of our new image
        height_a = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        height_b = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))

        # take the maximum of the width and height values to reach
        # our final dimensions
        max_width = max(int(width_a), int(width_b))
        max_height = max(int(height_a), int(height_b))

        # construct our destination points which will be used to
        # map the screen to a top-down, "birds eye" view
        dst = np.array([
            [0, 0],
            [max_width, 0],
            [max_width, max_height],
            [0, max_height]], dtype="float32")

        # calculate the perspective transform matrix and warp
        # the perspective to grab the screen
        m = cv2.getPerspectiveTransform(rect, dst)
        result = cv2.warpPerspective(__image, m, (max_width, max_height))
        # crop bild auf 10mm Rand
        # größe = 360mm x 360mm
        # abschneiden: oben: 7mm links: 15mm rechts 15mm unten 23mm
        # ergibt: 330mm x 330mm
        # img[y:y + h, x:x + w]
        ct = int((max_height / 360) * 7)
        cw = int((max_width / 360) * 15)
        cb = int((max_height / 360) * 23)
        crop = result[ct:max_height - cb, cw:max_width - cw]
        resized = cv2.resize(crop, (800, 800))
        visualLogger.debug(VisualRecord("warp_classic", [resized, result, crop], fmt="png"))
        return resized

    def _prepare_image_classic(self, _img):
        _gray = cv2.cvtColor(_img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        blank_grid = 255 - thresh.astype('uint8')
        blank_grid = cv2.erode(blank_grid, None, iterations=4)
        blank_grid = cv2.dilate(blank_grid, None, iterations=2)
        blank_grid = cv2.erode(blank_grid, None, iterations=4)
        blank_grid = cv2.dilate(blank_grid, None, iterations=2)

        mark_grid = cv2.GaussianBlur(thresh, (5, 5), 0)
        mark_grid = cv2.erode(mark_grid, None, iterations=4)
        mark_grid = cv2.dilate(mark_grid, None, iterations=4)
        _, mark_grid = cv2.threshold(mark_grid, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        _tiles_candidates = set()
        _blank_candidates = {}
        self._mark_grid((7, 7), mark_grid, blank_grid, _tiles_candidates, _blank_candidates)  # starte in der Mitte

        if logging.DEBUG >= visualLogger.level:
            height, width, _ = _img.shape
            mask = np.zeros((height, width), np.uint8)
            for (_col, _row) in _tiles_candidates:
                y = get_y_position(_row)
                x = get_x_position(_col)
                cv2.rectangle(mask, (x - 10, y - 10), (x + GRID_W + 15, y + GRID_H + 15),
                              (255, 255, 255), -1)
            masked = cv2.bitwise_and(_gray, _gray, mask=mask)
            visualLogger.debug(VisualRecord("prepare image: overlay, gray, masked, thresh, mark_grid, blank_search",
                                            [overlay_grid(_img), _gray, masked, thresh, mark_grid, blank_grid],
                                            fmt="jpg"))
        return _gray, _blank_candidates, _tiles_candidates

    def _mark_grid(self, coord, _grid, _blank_grid, _board, _blank_candidates):
        (_c, _r) = coord
        if _c < 0 or _c > 14:
            return
        if _r < 0 or _r > 14:
            return
        if (_c, _r) in _board:
            return
        _y = get_y_position(_r)
        _x = get_x_position(_c)
        # schneide Gitterelement aus
        _image = _grid[_y + 12:_y + GRID_H - 12, _x + 12:_x + GRID_W - 12]
        percentage = np.count_nonzero(_image) * 100 // _image.size
        if percentage > 60:
            _board.add((_c, _r))
            _img_blank = _blank_grid[_y + 15:_y + GRID_H - 15, _x + 15:_x + GRID_W - 15]
            percentage = np.count_nonzero(_img_blank) * 100 // _img_blank.size
            if percentage > 85:
                _blank_candidates[(_c, _r)] = ('_', 76 + (percentage - 90) * 2)
            self._mark_grid((_c + 1, _r), _grid, _blank_grid, _board, _blank_candidates)
            self._mark_grid((_c - 1, _r), _grid, _blank_grid, _board, _blank_candidates)
            self._mark_grid((_c, _r + 1), _grid, _blank_grid, _board, _blank_candidates)
            self._mark_grid((_c, _r - 1), _grid, _blank_grid, _board, _blank_candidates)

    def analyze(self, image=None, must_warp=True, last_board=None):
        _start = time.time()
        self.img = image
        if self.img is None:
            raise ValueError("img darf nicht None sein")
        self.board = last_board if last_board is not None else {}
        self.warped = self.warp(self.img) if must_warp else self.img

        if last_board is not None:
            self.board = {i: last_board[i] for i in last_board if last_board[i][1] >= 90 and last_board[i][0] != '_'}
        gray, blank_candidates, tile_candidates = self._prepare_image_classic(self.warped)
        tile_candidates -= set([i for i in self.board if self.board[i][1] >= 90])

        q = queue.Queue(0)
        for e in tile_candidates:
            q.put((e, gray, self.board, blank_candidates), block=False)
        for _ in range(WORKERS):
            q.put(None)  # add end-of-queue markers

        for _ in range(WORKERS):
            WorkerClassic(q).start()  # start a worker
        q.join()

        if logging.DEBUG >= visualLogger.level:
            _mark = overlay_grid(self.warped)
            _mark = overlay_tiles(_mark, board=self.board)
            visualLogger.debug(VisualRecord("marked", [_mark], fmt="jpg"))
        logging.info(f"timer analyze: {(time.time() - _start):.2f} sec")
        logging.debug(f"visited: #{len(tile_candidates)} {tile_candidates}")
        return self.board, self.warped
