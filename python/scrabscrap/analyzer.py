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

import analyzer_classic
import analyzer_custom
from config import WARP, BOARD_LAYOUT


def analyze_picture(image, must_warp=WARP, last_board=None, ignore_board=None, layout=BOARD_LAYOUT):
    """
    Analysiere das Bild. Hierzu wird die Spielfeldfläche in ein Gitter unterteilt. Jedes Gitterelement
    wird dann auf die mittlere Farbe geprüft und falls damit ein Spielstein erkannt wurde, wird hier ein
    Matching durchgeführt. Diese werden dann in dem aktuellen Board eingefügt.
    :param image: zu analysierendes Bild
    :param must_warp: falls ein warp des Bildes durchgeführt werden muss - ohne Angabe wird in der Wert aus
    scrabble.ini genommen
    :param last_board: Der Inhalt des letzten Boards - alle Steine mit einem Score > 90 werden vorrangig behalten
    :param ignore_board: Der Inhalt des drittletzten Boards - die Steine werden bei dem Matching ignoriert
    :param layout: Welches Layout soll verwendet werden (custom, classic) - Default per ini-Datei
    :return: dict(board)
    """

    if layout == 'custom':
        analyzer = analyzer_custom.AnalyzerCustom()
        board, warped = analyzer.analyze(image=image, must_warp=must_warp, last_board=last_board,
                                         ignore_board=ignore_board)
    else:
        analyzer = analyzer_classic.AnalyzerClassic()
        board, warped = analyzer.analyze(image=image, must_warp=must_warp, last_board=last_board)

    return board, warped
