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
import json
import logging
import queue
import threading

import cv2

from analyzer import analyze_picture
from board import tiles
from config import WEB_PATH, WRITE_WEB, FTP
from worker.ftp import WorkerFtp


class ScrabbleOp:

    def __init__(self, _op, _img, _active, _scrabble, _time):
        self.op = _op  # move, --, challenge, time
        self.img = _img
        self.active = _active  # 0/1
        self.scrabble = _scrabble
        self.time = _time


class WorkerScrabble(threading.Thread):

    def __init__(self, q):
        self.__queue = q
        if FTP:
            self.ftp_queue = queue.Queue(0)
            WorkerFtp(self.ftp_queue).start()
        else:
            self.ftp_queue = None
        threading.Thread.__init__(self)
        self.setDaemon(True)

    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                self.__queue.task_done()
                break  # reached end of queue
            if item.op == "start":
                try:
                    self.__clear_game(item)
                except Exception:
                    logging.exception("Fehler bei clear game")
            elif item.op == "move":
                try:
                    _last_board = dict(item.scrabble.game[-1][item.scrabble.DICT_BOARD]) if len(
                        item.scrabble.game) > 0 else None
                    _ignore_board = dict(item.scrabble.game[-3][item.scrabble.DICT_BOARD]) if len(
                        item.scrabble.game) > 2 else None
                    _board, warped = analyze_picture(item.img, last_board=_last_board, ignore_board=_ignore_board)
                    item.img = warped
                    item.scrabble.move(_board, item.scrabble.player[item.active])
                    self.__write_move(item)
                except Exception:
                    logging.exception("Analyse des Scrabble Boards nicht erfolgreich - ? inkorrekte Punktestände")
            elif item.op == "--":
                item.scrabble.valid_challenge()
                zug = len(item.scrabble.game)
                item.img = cv2.imread(WEB_PATH + "image-" + str(zug-2) + ".jpg")
                self.__write_move(item)
            elif item.op == "challenge":
                try:
                    item.scrabble.invalid_challenge(item.scrabble.player[item.active])
                    zug = len(item.scrabble.game)
                    item.img = cv2.imread(WEB_PATH + "image-" + str(zug-1) + ".jpg")
                    self.__write_move(item)
                except Exception:
                    logging.exception("Analyse des Scrabble Boards nicht erfolgreich - ? inkorrekte Punktestände")
            elif item.op == "time":
                pass
            elif item.op == "quit" or item.op == "reset":
                self.__store_game(item)
                item.scrabble.reset()
            logging.debug("gcg-data:" + str(item.scrabble))
            logging.info(f'Score {item.scrabble.player[0]}={item.scrabble.get_score(item.scrabble.player[0]):d}'
                         f' {item.scrabble.player[1]}={item.scrabble.get_score(item.scrabble.player[1]):d}')
            self.__queue.task_done()
            logging.debug("scrabble task finished")

    def __clear_game(self, item):
        if WRITE_WEB or FTP:
            try:
                to_json = json.dumps(
                    {
                        'time': str(datetime.datetime.now()),
                        'move': 0,
                        'score1': 0,
                        'score2': 0,
                        'time1': int(item.time[0]),
                        'time2': int(item.time[1]),
                        'name1': item.scrabble.player[0],
                        'name2': item.scrabble.player[1],
                        'onmove': item.scrabble.player[item.active],
                        'moves': [],
                        'board': [],
                        'bag': []
                    })
                # überschreibe den aktuellen Zustand
                f = open(WEB_PATH + "data-0.json", "w")
                f.write(to_json)
                f.close()
                f = open(WEB_PATH + "status.json", "w")
                f.write(to_json)
                f.close()
                open(WEB_PATH + "image-0.jpg", 'a').close()
                if FTP and self.ftp_queue is not None:
                    self.ftp_queue.put(('move', 0, None))
            except Exception as e:
                logging.exception(f"Fehler beim Clean des Spielstandes {e}")

    def __write_move(self, item):
        if WRITE_WEB or FTP:
            try:
                zug = len(item.scrabble.game)
                k = item.scrabble.game[-1][item.scrabble.DICT_BOARD].keys()
                v = item.scrabble.game[-1][item.scrabble.DICT_BOARD].values()
                k1 = [chr(ord('a') + y) + str(x + 1) for (x, y) in k]
                v1 = [t for (t, p) in v]
                bag = tiles.bag_as_list.copy()
                # noinspection PyStatementEffect
                [i for i in v1 if i not in bag or bag.remove(i)]  # alle aus v1 entfernen, falls in bag
                movelist = [str(g[item.scrabble.DICT_MOVE]) for g in item.scrabble.game]

                to_json = json.dumps(
                    {
                        'time': str(datetime.datetime.now()),
                        'move': zug,
                        'score1': item.scrabble.get_score(item.scrabble.player[0]),
                        'score2': item.scrabble.get_score(item.scrabble.player[1]),
                        'time1': int(item.time[0]),
                        'time2': int(item.time[1]),
                        'name1': item.scrabble.player[0],
                        'name2': item.scrabble.player[1],
                        'onmove': item.scrabble.player[item.active],
                        'moves': movelist,
                        'board': dict(zip(*[k1, v1])),
                        'bag': bag
                    })
                f = open(WEB_PATH + "data-" + str(zug) + ".json", "w")
                f.write(to_json)
                f.close()
                # überschreibe den aktuellen Zustand
                f = open(WEB_PATH + "status.json", "w")
                f.write(to_json)
                f.close()
                cv2.imwrite(WEB_PATH + "image-" + str(zug) + ".jpg", item.img)
                if FTP and self.ftp_queue is not None:
                    self.ftp_queue.put(('move', zug, None))
            except Exception as e:
                logging.exception(f"Fehler beim Speichern des Spielstandes {e}")

    def __store_game(self, item):
        import uuid
        import os
        from zipfile import ZipFile

        if not WRITE_WEB and not FTP:
            return
        if len(item.scrabble.game) < 1:
            return
        uuid = str(uuid.uuid4())
        filename = item.scrabble.player[0] + "-" + item.scrabble.player[1] + "-" + uuid
        prefix = WEB_PATH + filename

        try:
            f = open(prefix + ".gcg", "w")
            f.write(str(item.scrabble))
            f.close()
            with ZipFile(prefix + '.zip', 'w') as _zip:
                _zip.write(prefix + ".gcg")
                logging.info(f"create zip with {len(item.scrabble.game):d} files")
                for i in range(1, len(item.scrabble.game) + 1):
                    _zip.write(WEB_PATH + "image-" + str(i) + ".jpg")
                    _zip.write(WEB_PATH + "data-" + str(i) + ".json")
                if os.path.exists(WEB_PATH+"../log/messages.log"):
                    _zip.write(WEB_PATH+"../log/messages.log")
            if FTP and self.ftp_queue is not None:
                self.ftp_queue.put(('zip', None, filename))
                self.ftp_queue.put(None)
                self.ftp_queue.join()
            logging.info("delete image/data files")
            os.system('rm ' + WEB_PATH + "image*")
            os.system('rm ' + WEB_PATH + "data*")
            os.system('rm ' + WEB_PATH + "*.gcg")
        except Exception as e:
            logging.exception(f"Fehler beim Speichern des Spieles {e}")
