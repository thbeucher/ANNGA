#-------------------------------------------------------------------------------
# Name:        Crossover
# Purpose:
#
# Author:      tbeucher
#
# Created:     01/02/2016
# Copyright:   (c) tbeucher 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import numpy as np


def crossover(dad, mom, pop, SF):
    '''
    Creates the offspring from parents

    Inputs:
    dad: numpy ndarray,
    mom: numpy ndarray,
    pop: class object, corresponding to the population
    SF: selection function

    Outputs:
    baby1: numpy ndarray,
    baby2: numpy ndarray,

    '''
    shape1Dad, shape2Dad = dad.shape
    shape1Mom, shape2Mom = mom.shape
    #return dad and mom as offsprings dependent of the rate or if parents are the same
    if(np.array_equal(dad, mom)):
        while np.array_equal(dad, mom):
            dad = SF(pop.population)
            dad = dad.adn
    #determine a crossover point
    cp = np.random.randint(0, dad.size-1)
    #create the offspring
    part1Dad = (dad.reshape(dad.size))[0:cp:1]
    part2Dad = (dad.reshape(dad.size))[cp:dad.size:1]
    part1Mom = (mom.reshape(mom.size))[0:cp:1]
    part2Mom = (mom.reshape(mom.size))[cp:mom.size:1]
    baby1 = np.hstack((part1Dad, part2Mom)).reshape((shape1Dad, shape2Dad))
    baby2 = np.hstack((part1Mom, part2Dad)).reshape((shape1Mom, shape2Mom))
##    if(np.array_equal(baby1, baby2) or np.array_equal(baby1, dad) or np.array_equal(baby1, mom) or np.array_equal(baby2, dad) or np.array_equal(baby2, mom)):
##        baby1, baby2 = crossover(dad, mom, pop)
    return baby1, baby2

def twoPointCrossover(dad, mom, pop, SF):
    shape1Dad, shape2Dad = dad.shape
    shape1Mom, shape2Mom = mom.shape
    #return dad and mom as offsprings dependent of the rate or if parents are the same
    if(np.array_equal(dad, mom)):
        while np.array_equal(dad, mom):
            dad = SF(pop.population)
            dad = dad.adn
    #determine the two point for crossover
    cp1 = np.random.randint(0, dad.size-2)
    cp2 = np.random.randint(cp1+1, dad.size-1)
    #create the offspring
    part1Dad = (dad.reshape(dad.size))[0:cp1:1]
    part2Dad = (dad.reshape(dad.size))[cp1:cp2:1]
    part3Dad = (dad.reshape(dad.size))[cp2:dad.size:1]
    part1Mom = (mom.reshape(mom.size))[0:cp1:1]
    part2Mom = (mom.reshape(mom.size))[cp1:cp2:1]
    part3Mom = (mom.reshape(mom.size))[cp2:mom.size:1]
    baby1 = np.hstack((part1Dad, part2Mom, part3Dad)).reshape((shape1Dad, shape2Dad))
    baby2 = np.hstack((part1Mom, part2Dad, part3Mom)).reshape((shape1Mom, shape2Mom))
##    if(np.array_equal(baby1, baby2) or np.array_equal(baby1, dad) or np.array_equal(baby1, mom) or np.array_equal(baby2, dad) or np.array_equal(baby2, mom)):
##        baby1, baby2 = twoPointCrossover(dad, mom, pop)
    return baby1, baby2

def uniformCrossover(dad, mom, pop, SF):
    mixingRatio = 0.5
    shape1Dad, shape2Dad = dad.shape
    shape1Mom, shape2Mom = mom.shape
    if(np.array_equal(dad, mom)):
        while np.array_equal(dad, mom):
            dad = SF(pop.population)
            dad = dad.adn
    dad = dad.reshape(dad.size)
    mom = dad.reshape(mom.size)
    baby1 = np.ones(dad.size)
    baby2 = np.ones(mom.size)
    for i in range(dad.size):
        if np.random.rand() > mixingRatio:
            baby1[i] = dad[i]
        else:
            baby1[i] = mom[i]
        if np.random.rand() > mixingRatio:
            baby2[i] = dad[i]
        else:
            baby2[i] = mom[i]
    baby1 = baby1.reshape((shape1Dad, shape2Dad))
    baby2 = baby2.reshape((shape1Mom, shape2Mom))
    return baby1, baby2





##    def crossover(self, dad, mom, pop):
##        '''
##        Creates the offspring from parents
##
##        Inputs:
##            dad: numpy ndarray,
##            mom: numpy ndarray,
##
##        Outputs:
##            baby1: numpy ndarray,
##            baby2: numpy ndarray,
##
##        '''
##        shape1Dad, shape2Dad = dad.shape
##        shape1Mom, shape2Mom = mom.shape
##        #return dad and mom as offsprings dependent of the rate or if parents are the same
##        if(np.array_equal(dad, mom) or np.random.ranf(1) > self.crossoverRate):
##            #baby1 = dad
##            #baby2 = mom
##            #return baby1, baby2
##            while np.array_equal(dad, mom):
##                dad = rws2(pop.population)
##                dad = dad.adn
##        #determine a crossover point
##        cp = np.random.randint(0, dad.size-1)
##        #create the offspring
##        part1Dad = (dad.reshape(dad.size))[0:cp:1]
##        part2Dad = (dad.reshape(dad.size))[cp:dad.size:1]
##        part1Mom = (mom.reshape(mom.size))[0:cp:1]
##        part2Mom = (mom.reshape(mom.size))[cp:mom.size:1]
##        baby1 = np.hstack((part1Dad, part2Mom)).reshape((shape1Dad, shape2Dad))
##        baby2 = np.hstack((part2Dad, part1Mom)).reshape((shape1Mom, shape2Mom))
##        return baby1, baby2
