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
import ftplib
import logging
import os
import threading

from config import WEB_PATH

WORK_DIR = os.path.abspath(os.path.dirname(os.path.abspath(__file__))+"/../../../work")


class WorkerFtp(threading.Thread):

    def __init__(self, q):
        self.__queue = q
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.ftp_server = None
        self.ftp_user = None
        self.ftp_pass = None
        try:
            ftp = configparser.ConfigParser()
            with open(WORK_DIR + '/ftp-secret.ini', "r") as config_file:
                ftp.read_file(config_file)
                self.ftp_server = ftp['ftp']['ftp-server']
                self.ftp_user = ftp['ftp']['ftp-user']
                self.ftp_pass = ftp['ftp']['ftp-password']
        except Exception as e:
            logging.exception(f"can not read ftp-secret.ini {e}")

    def __store_move(self, move):
        if self.ftp_server is None:
            logging.warning("ftp: server not configured")
            return
        try:
            _start = datetime.datetime.now()
            logging.info("ftp: start upload to ftp-server")
            session = ftplib.FTP(self.ftp_server, self.ftp_user, self.ftp_pass)
            with open(WEB_PATH + "data-" + str(move) + ".json", 'rb') as file:
                session.storbinary("STOR data-" + str(move) + ".json", file)   # send the file
            with open(WEB_PATH + "image-" + str(move) + ".jpg", 'rb') as file:
                session.storbinary("STOR image-" + str(move) + ".jpg", file)   # send the file
            with open(WEB_PATH + "data-" + str(move) + ".json", 'rb') as file:
                session.storbinary("STOR status.json", file)  # send the file
            session.quit()
            logging.info(f"ftp: end upload to ftp-server: {self.ftp_server} {datetime.datetime.now() - _start}")
        except Exception as e:
            logging.warning(f"ftp: upload failure {e}")

    def __store_zip(self, filename):
        if self.ftp_server is None:
            logging.warning("ftp: server not configured")
            return
        try:
            _start = datetime.datetime.now()
            logging.info("ftp: start transfer zip file to ftp server")
            session = ftplib.FTP(self.ftp_server, self.ftp_user, self.ftp_pass)
            with open(WEB_PATH + filename + ".zip", 'rb') as file:
                session.storbinary("STOR " + filename + ".zip", file)  # send the file
            logging.info("ftp: delete data files from ftp server")
            files = session.nlst()
            for i in files:
                if i.startswith("data-"):
                    session.delete(i)  # delete (not status.json, *.zip)
            session.quit()
            logging.info(f"ftp: end upload to ftp-server: {self.ftp_server} {datetime.datetime.now() - _start}")
        except Exception as e:
            logging.warning(f"ftp: upload failure {e}")

    def run(self):
        while 1:
            item = self.__queue.get()
            if item is None:
                self.__queue.task_done()
                break  # reached end of queue
            op = item[0]
            move = item[1]
            filename = item[2]

            if op == 'move':
                self.__store_move(move)
            elif op == 'zip':
                self.__store_zip(filename)

            self.__queue.task_done()
            logging.info(f"ftp: {op} tasks done")
