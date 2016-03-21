#-------------------------------------------------------------------------------
# Name:        Utils
# Purpose:
#
# Author:      tbeucher
#
# Created:     29/12/2015
# Copyright:   (c) tbeucher 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import numpy as np
import tkinter as tk
from itertools import  combinations


def savePop(pop, popName = 'pop_0'):
    directoryToSave = os.getcwd() + "/Brains/" + popName + "/"
    if not os.path.exists(directoryToSave):
        os.makedirs(directoryToSave)
    i = 0
    for ind in pop.population:
        fileName = directoryToSave + "brainFitness_" + str(i)
        arr, allSi, allSh = convertANNtoArray(ind.brain.ANN)
        np.savez(fileName, fitnessScore=ind.fitnessScore, brain=arr, allSizes=allSi, allShapes=allSh)
        i += 1


def loadOnePop(pop = "pop_0", totalPath = 'no'):
    if totalPath == 'no':
        path = os.getcwd() + "/Brains/" + pop + "/"
    else:
        path = totalPath + pop + "/"
    listOfObj = [np.load(path + el) for el in os.listdir(path)]
    listOrderedByfitnessScore = sorted(listOfObj, key=lambda x:x['fitnessScore'], reverse=True)
    newList = []
    for el in listOrderedByfitnessScore:
        a, b, c = el['brain'], el['allSizes'], el['allShapes']
        brainReconstructed = reconstructANN(a, b, c)
        newDic = {}
        newDic['brain'] = brainReconstructed
        newDic['fitnessScore'] = el['fitnessScore']
        newList.append(newDic)
    return newList


def convertANNtoArray(ann):
    arrayANN = np.asarray([])
    allSizes = [(el[0].size, el[1].size) for el in ann]
    allShapes = [(el[0].shape, el[1].shape) for el in ann]
    for el in ann:
        a = el[0].reshape(el[0].size)
        b = el[1].reshape(el[1].size)
        arrayANN = np.hstack((arrayANN, a, b))
    return arrayANN, allSizes, allShapes

def reconstructANN(arrayANN, allSizes, allShapes):
    ann = []
    old1 = 0
    for size, shape in zip(allSizes, allShapes):
        t1 = arrayANN[old1:old1+size[0]:1].reshape(shape[0])
        old1 += size[0]
        t2 = arrayANN[old1:old1+size[1]:1].reshape(shape[1])
        old1 += size[1]
        ann.append((t1, t2))
    return ann

def newFenTop():
    topFen = tk.Toplevel()
    canv = tk.Canvas(topFen)
    canv.pack()
    text = canv.create_text((25,10), text='chargement de la population')
    return topFen, canv, text

def addScoreOnTopWindows(topFen, sizePop):
    topFen[1].create_text((40,25), text = "fitnessScore: ")
    i = 40
    texts = []
    for j in range(sizePop):
        text = "Individu " + str(j) + " : "
        texts.append(topFen[1].create_text((40, i), text=text))
        i += 15
    return texts

def refreshScores(topFen, texts, pop):
    scores = [el.fitnessScore for el in pop.population]
    for el, j, t in zip(scores, range(len(scores)), texts):
        text = "Individu " + str(j) + " : " + str(el)
        topFen[1].itemconfig(t, text=text)


def compareBrain(pop):
    temp = [el.adn for el in pop.population]
    i, j = 0, 0
    for el in combinations(temp, 2):
        if np.array_equal(el[0], el[1]):
            i += 1
        else:
            j += 1
    print(i, j)


def startWithChoosenPop(choosenPop):
    pop = input("Nom de la population de depart(0 sinon): ")
    if not "pop" in pop:
        if int(pop) == 0:
            return 0
    else:
        numPop = int(pop.split("_")[1])
        pop = loadOnePop(pop = pop)
        for ind, newInd in zip(choosenPop.population, pop):
            ind.brain.ANN = newInd['brain']
            ind.weightOfTheANN()
        return numPop

def countIdentiqueArrayElement(b):
    c = {}
    for i, el1 in enumerate(b):
        c[i] = []
        for j, el2 in enumerate(b):
            if np.array_equal(el1, el2):
                if j not in c.keys():
                    k = 0
                    for val in c.values():
                        if j in val:
                            k += 1
                    if k == 0:
                        c[i].append(j)
    d = []
    for key, val in c.items():
        if len(val) == 0:
            d.append(key)
    [c.pop(el) for el in d]
    return c

##pop = loadOnePop("pop_90")
##a = [el['brain'] for el in pop]
##b = [convertANNtoArray(el)[0] for el in a]
##c = countIdentiqueArrayElement(b)
##print(c)



##def bidule():
##    c.create_text((25,25), text="non!")
##
##f = tk.Tk()
##c = tk.Canvas(f)
##c.pack()
##f.protocol('WM_DELETE_WINDOW', bidule)
##f.mainloop()
