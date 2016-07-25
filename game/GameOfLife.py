#-------------------------------------------------------------------------------
# Name:        lifeGame
# Purpose:
#
# Author:      tbeucher
#
# Created:     28/10/2015
# Copyright:   (c) tbeucher 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
import tkinter as tk
import time

class LifeGame:

    def __init__(self, size_fen, nb_cell_alive, size_cell):
        self.size_fen = size_fen
        self.nb_cell_alive = nb_cell_alive
        self.size_cell = size_cell
        self.create_win_and_initiate()
        self.exit_condition = False
        self.event()

    def runGame(self):
        time.sleep(1)
        while self.exit_condition == False:
            self.rule_of_game()
            self.apply_new_gen()
            self.canv.update()
            time.sleep(0.1)

    def apply_new_gen(self):
        for el1 in range(self.nb_case_line):
            for el2 in range(self.nb_case_line):
                if self.tabGame[el1][el2][1] == 0:
                    self.canv.itemconfig(self.tabGame[el1][el2][0], fill="white")
                else:
                    self.canv.itemconfig(self.tabGame[el1][el2][0], fill="blue")

    def check_neighbors(self, c1, c2):
        nb_neighbors_alive = 0
        for i in range(-1,2,1):
            for j in range(-1,2,1):
                #check if case exist
                if c1+i >= 0 and c1+i < self.nb_case_line\
                   and c2+j >= 0 and c2+j < self.nb_case_line:
                    if c1+i == c1 and c2+j == c2:
                        a = 1
                    else:
                        if self.tabGame[c1+i][c2+j][1] == 1:
                            nb_neighbors_alive += 1
        return nb_neighbors_alive

    def rule_of_game(self):
        for c1 in range(self.nb_case_line):
            for c2 in range(self.nb_case_line):
                neighbors = self.check_neighbors(c1, c2)
                if self.tabGame[c1][c2][1] == 0:
                    if neighbors == 3:
                        self.tabGame[c1][c2][1] = 1
                else:
                    if neighbors < 2 or neighbors > 3:
                        self.tabGame[c1][c2][1] = 0

    def create_win_and_initiate(self):
        self.win = tk.Tk()
        self.canv = tk.Canvas(self.win, width = self.size_fen,\
                              height = self.size_fen)
        self.canv.pack()
        self.create_pavement()
        #white for dead cell and blue for alive one
        self.init_cell_alive()
        self.canv.update()

    def init_cell_alive(self):
        r1, r2 = np.random.randint(0, self.nb_case_line, self.nb_cell_alive),\
                 np.random.randint(0, self.nb_case_line, self.nb_cell_alive)
        for i, j in zip(r1, r2):
            self.tabGame[i][j][1] = 1
            self.canv.itemconfig(self.tabGame[i][j][0], fill="blue")

    def create_pavement(self):
        self.tabGame = []
        self.nb_case_line = int(self.size_fen/self.size_cell)
        x, y = 0, 0
        for line in range(self.nb_case_line):
            y = line*self.size_cell
            self.tabGame.append([])
            for col in range(self.nb_case_line):
                x = col*self.size_cell
                #(obj, state, nb_neighbour) 0=dead 1=alive
                self.tabGame[line].append(\
                    [self.canv.create_rectangle(x, y,\
                                                x+self.size_cell,\
                                                y+self.size_cell), 0, 0])

    def exit(self, bla):
        self.exit_condition = True

    def event(self):
        self.win.bind("<Escape>", self.exit)


a = LifeGame(300,300,10)
a.runGame()
    
