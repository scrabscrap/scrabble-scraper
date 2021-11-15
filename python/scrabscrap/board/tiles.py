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

import os.path

import cv2

scores = dict(A=1, B=3, C=4, D=1, E=1, F=4, G=2, H=2, I=1, J=6, K=4, L=2, M=3, N=1, O=2, P=4, Q=10, R=1, S=1, T=1,
              U=1, V=6, W=3, X=8, Y=10, Z=3, Ä=6, Ö=8, Ü=6, _=0)

bag = dict(A=5, B=2, C=2, D=4, E=15, F=2, G=3, H=4, I=6, J=1, K=2, L=3, M=4, N=9, O=3, P=1, Q=1, R=6, S=7, T=6,
           U=6, V=1, W=1, X=1, Y=1, Z=1, Ä=1, Ö=1, Ü=1, _=2)

bag_as_list = sum([[k] * bag[k] for k in bag], [])

tiles = []


class OneTile:

    def __init__(self):
        self.name = "Placeholder"
        self.img = []
        self.w = 0
        self.h = 0


def load_tiles(filepath=None):
    tiles.clear()
    if filepath is None:
        filepath = (os.path.dirname(__file__) or '.') + '/img/'

    for Tile in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                 'Ä', 'Ö', 'Ü']:
        image = cv2.imread(filepath + Tile + '.png')
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        new_tile = OneTile()
        new_tile.name = Tile
        new_tile.img = gray
        new_tile.w, new_tile.h = new_tile.img.shape[::-1]
        tiles.append(new_tile)
    return tiles


load_tiles()
