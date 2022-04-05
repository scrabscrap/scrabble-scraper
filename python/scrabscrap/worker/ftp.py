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
            logging.exception("can not read ftp-secret.ini {}".format(str(e)))

    def __store_move(self, move):
        if self.ftp_server is None:
            logging.warning("ftp server not configured")
            return
        try:
            session = ftplib.FTP(self.ftp_server, self.ftp_user, self.ftp_pass)
            file = open(WEB_PATH + "data-" + str(move) + ".json", 'rb')  # file to send
            session.storbinary("STOR data-" + str(move) + ".json", file)  # send the file
            file.close()  # close file and FTP
            file = open(WEB_PATH + "image-" + str(move) + ".jpg", 'rb')  # file to send
            session.storbinary("STOR image-" + str(move) + ".jpg", file)  # send the file
            file.close()  # close file and FTP
            file = open(WEB_PATH + "data-" + str(move) + ".json", 'rb')  # file to send
            session.storbinary("STOR status.json", file)  # send the file
            file.close()  # close file and FTP
            session.quit()
            logging.info("upload to ftp-server:" + self.ftp_server)
        except Exception as e:
            logging.warning("ftp upload failure" + str(e))

    def __store_zip(self, filename):
        if self.ftp_server is None:
            logging.warning("ftp server not configured")
            return
        logging.info("transfer zip file to ftp server {}".format(self.ftp_server))
        try:
            session = ftplib.FTP(self.ftp_server, self.ftp_user, self.ftp_pass)
            file = open(WEB_PATH + filename + ".zip", 'rb')  # file to send
            session.storbinary("STOR " + filename + ".zip", file)  # send the file
            file.close()  # close file and FTP
            logging.info("delete data files from ftp server")
            files = session.nlst()
            for i in files:
                if i.startswith("data-"):
                    session.delete(i)  # delete (not status.json, *.zip)
            session.quit()
        except Exception as e:
            logging.warning("ftp upload failure" + str(e))

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
            logging.info("{} ftp finished".format(op))
