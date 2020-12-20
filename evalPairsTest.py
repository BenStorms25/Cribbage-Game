import random
import time
import sys
from itertools import permutations
import copy
from collections import Counter
from typing import List


def evaluatePairs(hand1):

    totalpoints = 0

    hand = []

    for i in hand1:
        hand.append(i)

    counts = Counter(hand)
    listOfCounts = counts.values()

    for i in listOfCounts:
        if(i == 2):
            try:
                for i in range(len(hand)):
                    if(hand[i] == hand[i+1]):
                        totalpoints += 2
            except:
                pass

        elif(i == 3):
            try:
                for i in range(len(hand)):
                    if(hand[i] == hand[i + 1] and hand[i] == hand[i + 2]):
                        totalpoints += 3
            except:
                pass
            
        elif(i == 4):
            try:
                for i in range(len(hand)):
                    if(hand[i] == hand[i + 1] and hand[i] == hand[i+2] and hand[i] == hand[i+3]):
                        totalpoints += 4
            except:
                pass
        
        elif(i == 5):
            try:
                for i in range(len(hand)):
                    if(hand[i] == hand[i+1] and hand[i] == hand[i+2] and hand[i] == hand[i+3] and hand[i] == hand[i+4]):
                        totalpoints += 5
            except:
                pass
    if(totalpoints == 8):
        return 4
    if(totalpoints == 9):
        return 5

    return totalpoints

def main():

    hand = [1,1,2,3,4]
    points = evaluatePairs(hand)
    print(points)
main()