#-------------------------------------------------------------------------------
# Name:        RouletteWheelSelection
# Purpose:
#
# Author:      tbeucher
#
# Created:     18/01/2016
# Copyright:   (c) tbeucher 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np
from collections import Counter

class Ind:

    def __init__(self, i, f):
        self.id = i
        self.fitnessScore = f

def rws1(pop):
    '''
    Roulette wheel selection classique
    '''
    fitnessOfThePop = [el.fitnessScore for el in pop]
    t = sum(fitnessOfThePop)
    x = np.random.randint(0, t)
    for el in pop:
        x -= el.fitnessScore
        if x <= 0:
            return el

def rws12(pop):
    fitnessList = sorted([ind.fitnessScore for ind in pop])
    totalFitness = float(sum(fitnessList))
    if totalFitness == 0:
        totalFitness = 1
    wheel = [f/totalFitness for f in fitnessList]
    # Generate probability intervals for each individual
    probs = [sum(wheel[:i+1]) for i in range(len(wheel))]
    while 1:
        r = np.random.rand()
        for (i, ind) in enumerate(pop):
            if r <= probs[i]:
                return ind


def rws2(pop):
    '''
    Roulette wheel selection via stochastic acceptance
    '''
    fl = [el.fitnessScore for el in pop]
    while 1:
        #select randomly one of the ind
        ind = pop[np.random.randint(0, len(pop), 1)]
        #the selection is accepted with probability fitness/fmax
        if np.random.rand() < ind.fitnessScore/max(fl):
            return ind


def srwrs(pop):
    '''
    Stochastic remainder without replacement selection

    '''
    newPop = []
    for el in pop:
        newPop.append(Ind(pop.index(el), el.fitnessScore))
    fl = [el.fitnessScore for el in pop]
    ri = [el/np.mean(fl) for el in fl]
    eri = [int(el) for el in ri]
    for el1, el2, el3 in zip(newPop, ri, eri):
        newF = el2 - el3
        el1.fitnessScore = newF
    for ind, rie, ir in zip(pop, eri, ri):
        newFitness = ir - rie
        newInd = Ind(pop.index(ind), newFitness)
        newPop.append(newInd)
        if rie > 0:
            for i in range(rie):
                newFitness = ir - rie
                newInd = Ind(pop.index(ind), newFitness)
                newPop.append(newInd)
    #choosenInd = rws1(pop)
    choosenInd = rws2(newPop)
    realChoosenInd = pop[choosenInd.id]
    return realChoosenInd

def srwrs2(pop):
    '''
    Stochastic remainder without replacement selection

    '''
    #creation de Tm de dim m (m<n)
    #on recupere les individu dont leur fitness est superieur a la moyenne
    #chacun de ces individu est represente ni fois
    fitness = [el.fitnessScore for el in pop]
    Ni = [el/np.mean(fitness) for el in fitness]
    partieEntiere = [int(el) for el in Ni]
    partieFractionnaire = [el1 - el2 for el1, el2 in zip(fitness, partieEntiere)]
    newPop = []
    for el1, el2 in zip(pop, partieEntiere):
        newPop.append(el1)
        for i in range(el2):
            newPop.append(el1)
    #On ajoute aleatoirement n-m individu pour laisser une chance de selectionner
    #de moins bon individu qui peuvent potentiellement permettre d'atteindre le maxima
    while len(newPop) < len(pop):
        for el1, el2 in zip(pop, partieFractionnaire):
            if np.random.rand() < el2:
                newPop.append(el1)
    choosenOne = rws2(newPop)
    return choosenOne


def createPop(nbInd):
    pop = []
    for i in range(nbInd):
        ind = Ind(i, np.random.randint(0, 15))
        pop.append(ind)
    return pop

def tirage(pop, nbTirage):
    locoRws1 = []
    locoRws2 = []
    locoRws12 = []
    locoSrwrs = []
    locoSrwrs2 = []
    for i in range(nbTirage):
        ciRws1 = rws1(pop)
        locoRws1.append(ciRws1.id)
        ciRws2 = rws2(pop)
        locoRws2.append(ciRws2.id)
        ciRws12 = rws12(pop)
        locoRws12.append(ciRws12.id)
        ciSrwrs = srwrs(pop)
        locoSrwrs.append(ciSrwrs.id)
        ciSrwrs2 = srwrs2(pop)
        locoSrwrs2.append(ciSrwrs2.id)
    occurRws1 = Counter(locoRws1)
    occurRws2 = Counter(locoRws2)
    occurRws12 = Counter(locoRws12)
    occurSrwrs = Counter(locoSrwrs)
    occurSrwrs2 = Counter(locoSrwrs2)
    return occurRws1, occurRws2, occurRws12, occurSrwrs, occurSrwrs2


# pop = createPop(10)
# popIdF = [(el.id, el.fitnessScore) for el in pop]
# print(popIdF)
# oc1, oc2, oc3, oc4, oc5 = tirage(pop, 15)
# popIdFS = sorted(popIdF, key=lambda x:x[1])
# print(popIdFS)
# print("rws1 : ", [oc1[el[0]] for el in popIdFS])
# print("rws2 : ", [oc2[el[0]] for el in popIdFS])
# print("rws12 : ", [oc3[el[0]] for el in popIdFS])
# print("srwrs : ", [oc4[el[0]] for el in popIdFS])
# print("srwrs2 : ", [oc5[el[0]] for el in popIdFS])


#Old roulette selection in GeneticAlgorithm class
##    def rouletteSelection(self, pop):
##        '''
##        Chooses an individu among a population according to the roulette wheel selection
##
##        input:  -pop: class object, the population
##
##        output: -ind: class object, the individu selected
##
##        '''
##        fitnessList = sorted([ind.fitnessScore for ind in pop.population])
##        totalFitness = float(sum(fitnessList))
##        if totalFitness == 0:
##            totalFitness = 1
##        wheel = [f/totalFitness for f in fitnessList]
##        # Generate probability intervals for each individual
##        probs = [sum(wheel[:i+1]) for i in range(len(wheel))]
##        for n in range(int(pop.sizeOfPop)):
##            r = np.random.rand()
##            for (i, ind) in enumerate(pop.population):
##                if r <= probs[i]:
##                    return ind
##        print("Aucun individu n'a pu etre selectionne!")
##        return -1
##
##    def rouletteWheelSelection2(self, pop):
##        totalFitness = sum([ind.fitnessScore for ind in pop.population])
##        x = np.random.randint(0, totalFitness)
##        for ind in pop.population:
##            x -= ind.fitnessScore
##            if x <= 0:
##                return ind



##    def roulette_select(population, fitnesses, num):
##        total_fitness = float(sum(fitnesses))
##        rel_fitness = [f/total_fitness for f in fitnesses]
##        # Generate probability intervals for each individual
##        probs = [sum(rel_fitness[:i+1]) for i in range(len(rel_fitness))]
##        # Draw new population
##        new_population = []
##        for n in xrange(num):
##            r = rand()
##            for (i, individual) in enumerate(population):
##                if r <= probs[i]:
##                    new_population.append(individual)
##                    break
##        return new_population
