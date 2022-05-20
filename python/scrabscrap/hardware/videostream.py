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

# siehe auch:
# https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/
# https://www.pyimagesearch.com/2015/12/21/increasing-webcam-fps-with-python-and-opencv/
import logging
import time
from threading import Thread

import cv2

from config import IM_HEIGHT, IM_WIDTH, FPS, ROTATE, SIMULATE, SIMULATE_PATH

try:
    # noinspection PyUnresolvedReferences
    from picamera import PiCamera
    # noinspection PyUnresolvedReferences
    from picamera.array import PiRGBArray
except ImportError:
    SIMULATE = True


class PiVideoStream:

    def __init__(self, src=0, name="PIVideoStream", width=IM_WIDTH, height=IM_HEIGHT, fps=FPS):

        resolution = (width, height)
        self.name = name
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = fps
        if ROTATE:
            self.camera.rotation = 180
        self.rawCapture = PiRGBArray(self.camera, (384, 384))
        self.stream = self.camera.capture_continuous(self.rawCapture, format="bgr",
                                                     use_video_port=True, resize=(384, 384), splitter_port=1)
        time.sleep(2)  # wait for awb
        self.frame = []
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        thread = Thread(target=self.update, name=self.name, args=())
        thread.daemon = True
        thread.start()
        # warte auf das erste Bild
        for _ in range(0, 10):
            grabbed, _ = self.read()
            if grabbed:
                break
            time.sleep(0.3)
        return self

    def update(self):
        for file in self.stream:
            self.frame = file.array
            # self.rawCapture.seek(0)
            self.rawCapture.truncate(0)
            time.sleep(0.07)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()

    def picture(self):
        _capture = PiRGBArray(self.camera, size=(IM_WIDTH, IM_HEIGHT))
        self.camera.capture(_capture, format="bgr")
        return _capture.array

    def read(self):
        return self.frame is not None, self.frame

    def stop(self):
        self.stopped = True

    def close(self):
        time.sleep(1)
        self.camera.close()


class CvVideoStream:
    closed = False

    def __init__(self, src=0, name="VideoStream", width=IM_WIDTH, height=IM_HEIGHT, fps=FPS):
        # initialize the video camera stream and read the first frame
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.stream.set(cv2.CAP_PROP_FPS, fps)
        time.sleep(1)  # warte auf Kamera
        (self.grabbed, self.frame) = self.stream.read()
        while not self.grabbed:
            (self.grabbed, self.frame) = self.stream.read()
        self.name = name
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        thread = Thread(target=self.update, name=self.name, args=())
        thread.daemon = True
        thread.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            if self.stopped:
                self.stream.release()
                return
            (self.grabbed, self.frame) = self.stream.read()
            time.sleep(0.05)

    def picture(self):
        return self.frame

    def read(self):
        return self.grabbed, cv2.resize(self.frame, (384, 384))

    def stop(self):
        self.stopped = True

    def close(self):
        time.sleep(1)
        self.stream.release()


class SimulateVideo:
    closed = False

    def __init__(self, formatter):
        self.cnt = 0
        self.formatter = formatter
        self.img = cv2.imread(self.formatter.format(self.cnt))

    def picture(self):
        logging.debug(f"picture {self.formatter.format(self.cnt)}")
        return self.img

    def read(self):
        import os.path

        self.cnt += 1 if os.path.isfile(self.formatter.format(self.cnt + 1)) else 0
        self.img = cv2.imread(self.formatter.format(self.cnt))
        logging.debug(f"read {self.formatter.format(self.cnt)}")
        return True, cv2.resize(self.img, (384, 384))

    def start(self):
        pass

    def stop(self):
        pass


def get_video():
    if SIMULATE:
        logging.info("simuliere Video mit Bildern ...")
        cap = SimulateVideo(SIMULATE_PATH)
    else:
        logging.info("starte Kamera ...")
        # cap = CvVideoStream()
        cap = PiVideoStream()
    return cap
