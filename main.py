#-------------------------------------------------------------------------------
# Name:        main
# Purpose:
#
# Author:      tbeucher
#
# Created:     10/11/2015
# Copyright:   (c) tbeucher 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
from Windows import fenetre
from Individu import Ant
from Food import Food
import time
from MoveRule import computeNextPos
from Population import Population
import os
from Utils import savePop, newFenTop, addScoreOnTopWindows, refreshScores, startWithChoosenPop, zipData
import Params
from GeneticAlgorithm import Genetic
from Crossover import crossover, twoPointCrossover, uniformCrossover
from RouletteWheelSelection import rws2, srwrs2


def test():
    fen = fenetre()
    food = Food(fen)
    ant = Ant(fen)
    fen.setObj(ant.id)
    fen.setFoodObj(food)
    fen.fen.mainloop()

def routine():
    #create the windows
    fen = fenetre()
    #create the food
    food = Food(fen)
    #create the population
    pop = Population(fen, food)

    t = time.time()
    while time.time() - t < Params.p['lifeTime']:
        #time.sleep(0.01)
        pop.routineForPopulation()
        fen.refreshScreen()
    fen.fen.destroy()
    savePop(pop)

def routine2():
    for i in range(int(Params.p['nbEvol'])):
        popName = "pop_" + str(i)
        fen = fenetre()
        food = Food(fen)
        pop = Population(fen, food)
        t = time.time()
        while time.time() - t < Params.p['lifeTime']:
            pop.routineForPopulation()
            fen.refreshScreen()
        fen.fen.destroy()
        savePop(pop, popName = popName)

def routine3():
    gen = Genetic()
    fen = fenetre()
    food = Food(fen)
    newFen = newFenTop()
    texts = addScoreOnTopWindows(newFen, int(Params.p['sizePop']))
    for i in range(int(Params.p['nbEvol'])):
        popName = "pop_" + str(i)
        if i == 0:
            pop = Population(fen, food)
        else:
            gen.createNewPopulation(pop)
            food = Food(fen)
            pop.setFood(food)
            pop.setInitialPositions()
        newFen[1].itemconfig(newFen[2], text=popName)
        t = time.time()
        while time.time() - t < Params.p['lifeTime']:
            refreshScores(newFen, texts, pop)
            pop.routineForPopulation()
            fen.refreshScreen()
        savePop(pop, popName = popName)
    fen.fen.destroy()

def routine4(sf, cf):
    gen = Genetic(sf, cf)
    fen = fenetre()
    food = Food(fen)
    newFen = newFenTop()
    texts = addScoreOnTopWindows(newFen, int(Params.p['sizePop']))
    pop = Population(fen, food)
    numPop = startWithChoosenPop(pop)
    pop.setInitialPositions()
    for i in range(numPop, numPop+int(Params.p['nbEvol']), 1):
        popName = "pop_" + str(i)
        if i > numPop:
            gen.createNewPopulation(pop)
            food = Food(fen)
            pop.setFood(food)
            pop.setInitialPositions()
        newFen[1].itemconfig(newFen[2], text=popName)
        t = time.time()
        while time.time() - t < Params.p['lifeTime']:
            refreshScores(newFen, texts, pop)
            pop.routineForPopulation()
            fen.refreshScreen()
        savePop(pop, popName = popName)
    fen.fen.destroy()

def routineTo(sf, cf):
    gen = Genetic(sf, cf)
    fen = fenetre()
    food = Food(fen)
    #newFen = newFenTop()
    #texts = addScoreOnTopWindows(newFen, int(Params.p['sizePop']))
    pop = Population(fen, food)
    pop.setInitialPositions()
    for i in range(int(Params.p['nbEvol'])):
        popName = "pop_" + str(i)
        if i > 0:
            gen.createNewPopulation(pop)
            food = Food(fen)
            pop.setFood(food)
            pop.setInitialPositions()
        #newFen[1].itemconfig(newFen[2], text=popName)
        t = time.time()
        #while time.time() - t < Params.p['lifeTime']:
        j = 0
        while j < Params.p['lifeTime']:
            #refreshScores(newFen, texts, pop)
            pop.routineForPopulation()
            fen.refreshScreen()
            j += 1
        timeGen = time.time() - t
        print("Execution time: ", timeGen)
        savePop(pop, popName = popName)
    fen.fen.destroy()

def runAll():
    routineTo(rws2, crossover)
    zipData("rws2crossover", os.getcwd() + "/Brains")
    routineTo(rws2, twoPointCrossover)
    zipData("rws2twoPointCrossover", os.getcwd() + "/Brains")
    routineTo(rws2, uniformCrossover)
    zipData("rws2uniformCrossover", os.getcwd() + "/Brains")

    routineTo(srwrs2, crossover)
    zipData("srwrs2crossover", os.getcwd() + "/Brains")
    routineTo(srwrs2, twoPointCrossover)
    zipData("srwrs2twoPointCrossover", os.getcwd() + "/Brains")
    routineTo(srwrs2, uniformCrossover)
    zipData("srwrs2uniformCrossover", os.getcwd() + "/Brains")


def main():
    print("This is the main!")
    #routine4(rws2, crossover)
    runAll()


if __name__ == '__main__':
    main()
