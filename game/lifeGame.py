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
        self.get_map_neighbour()

    def runGame(self):
        for i in range(50):
            print("generation: ", i)
            self.get_map_neighbour()
            self.rule_of_game()
            self.apply_new_gen()
            self.canv.update()
            print("nb cell alive: ", self.nb_alive)
            time.sleep(0.1)

    def apply_new_gen(self):
        nb_alive = 0
        for el1 in range(self.nb_case_line):
            for el2 in range(self.nb_case_line):
                if self.tabGame[el1][el2][1] == 0:
                    self.canv.itemconfig(self.tabGame[el1][el2][0], fill="white")
                else:
                    nb_alive += 1
                    self.canv.itemconfig(self.tabGame[el1][el2][0], fill="blue")
        self.nb_alive = nb_alive

    def rule_of_game(self):
        #si la cellule est seule, elle meurt
        #si la cellule a une voisine, elle survit
        #si la cellule a deux voisine, elle enfante
        for el1 in range(self.nb_case_line):
            for el2 in range(self.nb_case_line):
                if self.tabGame[el1][el2][1] == 1:
                    if self.tabGame[el1][el2][2] == 0:
                        self.tabGame[el1][el2][1] = 0
                    elif self.tabGame[el1][el2][2] > 1:
                        test = 0
                        for e1, e2 in zip(np.random.randint(0, self.nb_case_line, 100), np.random.randint(0, self.nb_case_line, 100)):
                            if test == 0 and self.tabGame[e1][e2][1] == 0:
                                self.tabGame[e1][e2][1] == 1
                                test += 1

    def get_map_neighbour(self):
        for el1 in range(self.nb_case_line):
            for el2 in range(self.nb_case_line):
                neighbour_list = [[el1-1, el2], [el1+1, el2], [el1, el2-1], [el1, el2+1]]
                nb = 0
                for el in neighbour_list:
                    if el[0] >= 0 and el[0] < self.nb_case_line and el[1] >= 0 and el[1] < self.nb_case_line:
                        if self.tabGame[el[0]][el[1]][1] == 1:
                            nb += 1
                self.tabGame[el1][el2][2] = nb

    def create_win_and_initiate(self):
        self.win = tk.Tk()
        self.canv = tk.Canvas(self.win, width = self.size_fen, height = self.size_fen)
        self.canv.pack()

        self.create_pavement()
        r1 = np.random.randint(0, self.nb_case_line, self.nb_cell_alive)
        r2 = np.random.randint(0, self.nb_case_line, self.nb_cell_alive)
        for el1, el2 in zip(r1,r2):
            #white for dead cell and blue for alive one
            self.canv.itemconfig(self.tabGame[el1][el2][0], fill="blue")
            self.tabGame[el1][el2][1] = 1

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


a = LifeGame(300,50,10)
a.runGame()
    
