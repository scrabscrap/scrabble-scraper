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


class Action:
    def __init__(self, action):
        self.action = action

    def __str__(self): return self.action

    def __cmp__(self, other):
        if str(self.action) == str(other.action):
            return 0
        return str(self.action) < str(other.action)

    def __hash__(self): return hash(self.action)


# Static fields; an enumeration of instances:
PLAYER1 = Action("player 1 ready")
PLAYER2 = Action("player 2 ready")
PAUSE = Action("pause")
DOUBT = Action("doubt")
RESET = Action("reset")
QUIT = Action("quit")
CONFIG = Action("config")
