import random
import time
import sys
from itertools import permutations
import copy
from collections import Counter
from typing import List

computerScore = 0
playerScore = 0
playersTurn = False

class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit


def computerGivesGo():

    global playerScore
    print("The computer gives a go, giving a point to the player.\n")
    playerScore += 1 

def displayPlayCount(pegCount):

    print("\nCount: " + str(pegCount))



def playerGivesGo():

    global computerScore
    print("The player gives a go, giving a point to the computer.\n")
    computerScore += 1

def playRoundStartComputer(hand1, hand2):

    count = 0
    while(count <= 31):

        #computers turn:

        if(len(hand1) == 0 or len(hand2) == 0):
            compareHandLengths(hand1, hand2)
            break


        displayPlayCount(count)
    #players turn
        oldCount = count
        

        try:
            hand2, count = getAndPlayCardComputer(hand2, count)
        except TypeError:
            #this runs if the player has no more cards left to play.
            break

        if(count == oldCount):
            computerGivesGo()
            playRoundStartComputer(hand1, hand2)
            #break
        if(count >= 31):
            break
            
        displayPlayCount(count)
    #Then take the computers turn
        oldCount = count

        try:
            hand1, count = getAndPlayCardPlayer(hand1, count)
        except TypeError:
            #this runs if the computer has no more cards left.  
            break

        if(count == oldCount):
            playerGivesGo()
            #if the computer gives a go, then start a new round of play with the computer starting the play. 
            playRoundStartPlayer(hand1, hand2)
            
        if(count >= 31):
            break
        

    return hand1, hand2

def getAndPlayCardComputer(hand2, count):

    random.shuffle(hand2)

    try:
        CPUcardOfChoice = hand2[0]
    except IndexError:
        return hand2, count
    #hand2.remove(CPUcardOfChoice)

    #turn the chosen value into an int (face cards will get turned into 10.)

    try:
        intCPUValOfChoice = int(CPUcardOfChoice.value)
    except ValueError:
        intCPUValOfChoice = 10

    #check to see if the card can be added to the count without making it greater than 31. And if the hand still has another card in it, take it and use that instead.

    if(count + intCPUValOfChoice > 31 and len(hand2) > 1):
        #take a new card
        
        CPUcardOfChoice = hand2[1]
        try:
            intCPUValOfChoice = int(CPUcardOfChoice.value)
        except:
            pass
        
        if(intCPUValOfChoice + count > 31):
            return hand2, count

        else:
            count += intCPUValOfChoice
            hand2.remove(CPUcardOfChoice)
            displayPlayMove("computer",CPUcardOfChoice.value,count)
            computerPegEval(count)
            return hand2, count
    
    #if not, and the added card just makes the count go over 31, break out of the loop and start again. 

    elif(count + intCPUValOfChoice > 31):
        return hand2, count
    
    else:
        count += intCPUValOfChoice
        hand2.remove(CPUcardOfChoice)
        displayPlayMove("computer",CPUcardOfChoice.value,count)
        computerPegEval(count)
        return hand2, count

    #takes the computer count and evaluates for points.

def computerPegEval(pegCount):

    global computerScore

    if(pegCount == 15):
        print("The computer made 15, giving 2 points to the computer.\n")
        computerScore += 2
    if(pegCount == 31):
        print("The computer scored exactly 31, giving 2 point to the computer.\n")
        computerScore += 2
        
def displayPlayMove(player, value, totalCount):

    if(value == 8):
        print("\nThe " + player + " played an " + str(value) + ". Making the total count " + str(totalCount))
    else:
        print("\nThe " + player + " played a " + str(value) + ". Making the total count " + str(totalCount))
    

def getAndPlayCardPlayer(hand1, count):

     #prompt for card
    if(len(hand1) == 0):
        return
    displayHand(hand1)
    numberChoice = int(input("What card would you like to play? "))
    cardOfChoice = hand1[numberChoice - 1]
    
    try:
        intValueOfChoice = int(cardOfChoice.value)
    except ValueError:
        intValueOfChoice = 10 


    if(intValueOfChoice + count > 31):
        return hand1, count
    else:
        count += intValueOfChoice
    #add value of card to count, eval 15s, and remove chosen card from players hand. 

    #try statement for if the player plays a face card. 

    

    #evaluation takes place here.

    displayPlayMove("player",cardOfChoice.value,count)

    playerPegEval(count)
    hand1.remove(cardOfChoice)

    #display the move.

    

    return hand1, count#, is31

def playerPegEval(pegCount):

    global playerScore
    


    if(pegCount == 15):
        print("The player made 15, giving 2 points to the player.\n")
        playerScore += 2
    if(pegCount == 31):
        print("The player scored exactly 31, giving 2 point to the player.\n")
        playerScore += 2
    

    return

def playRoundStartPlayer(hand1, hand2):

    count = 0
    while(count <= 31):

        if(len(hand1) == 0 or len(hand2) == 0):
            compareHandLengths(hand1, hand2)
            break


        displayPlayCount(count)
    #players turn
        oldCount = count
        

        try:
            hand1, count = getAndPlayCardPlayer(hand1, count)
        except TypeError:
            #this runs if the player has no more cards left to play.
            break

        if(count == oldCount):
            playerGivesGo()
            playRoundStartPlayer(hand1, hand2)
            #break
        if(count >= 31):
            break
            
        displayPlayCount(count)
    #Then take the computers turn
        oldCount = count

        try:
            hand2, count = getAndPlayCardComputer(hand2, count)
        except TypeError:
            #this runs if the computer has no more cards left.  
            break

        if(count == oldCount):
            computerGivesGo()
            #if the computer gives a go, then start a new round of play with the computer starting the play. 
            playRoundStartComputer(hand1, hand2)
            
        if(count >= 31):
            break


    return hand1, hand2



def compareHandLengths(hand1, hand2):

    global playerScore
    global computerScore

    if(len(hand1) > len(hand2)):
        print("The player has the last card, so the player gets a point.")
        playerScore += 1
    elif(len(hand2) > len(hand1)):
        print("The computer has the last card, so the computer gets a point.")
        computerScore += 1

def initiatePlay(hand1, hand2):

    global playersTurn
    global playerScore
    global computerScore

    #print welcome message

    

    #put each hand into separate list of only values.

    hand1Vals = []
    hand2Vals = []
    

    #make original copies of the hands, becasue they all cards will eventually be removed from them.

    hand1Copy = copy.deepcopy(hand1)

    hand2Copy = copy.deepcopy(hand2)

    #if the players turn is true, then the player will start the play, else, the computer will play. 

    for value in hand1Copy:
        hand1Vals.append(value.value)
    for value in hand2Copy:
        hand2Vals.append(value.value)

    # check to see if the players turn is true, and if so, then continue with the play.


    if(playersTurn == True):

        print("It is the player's turn, so the player will begin the play.")

        while(len(hand1) > 0 and len(hand2) > 0):

            #player plays first:
            playRoundStartPlayer(hand1, hand2)

        compareHandLengths(hand1,hand2)

    elif(playersTurn == False):

        print("It is the computers turn, so the computer will begin the play.")

        #do evertthing in the if statement backwards, so that the computer starts.
        while(len(hand1) > 0 and len(hand2) > 0):

            playRoundStartComputer(hand1, hand2)

        compareHandLengths(hand1,hand2)


    return hand1Copy, hand2Copy

def displayHand(hand1):
    print("\nPlayer hand: \n=====================================")

    for card in hand1:
        print(str(hand1.index(card)+1) + ": " + str(card.value) + " of " + str(card.suit))

    print("=====================================")

def main():
    suits = ["spades","clubs","hearts","diamonds"]
    deck = [Card(value, suit) for value in range(1, 14) for suit in suits]

    hand1 = []
    hand2 = []

    random.shuffle(deck)
    
    for i in range(6):
        hand1.append(deck[i])
        del deck[i]
    for i in range(6):
        hand2.append(deck[i])
        del deck[i]
    

#convert numbers to face cards

    for card in range(len(hand1)):
        if(hand1[card].value == 11):
            hand1[card].value = "Jack"
        if(hand1[card].value == 12):
            hand1[card].value = "Queen"
        if(hand1[card].value == 13):
            hand1[card].value = "King"


    for card in range(len(hand2)):
        if(hand2[card].value == 11):
            hand2[card].value = "Jack"
        if(hand2[card].value == 12):
            hand2[card].value = "Queen"
        if(hand2[card].value == 13):
            hand2[card].value = "King"


    initiatePlay(hand1, hand2)

main()