#Cribbage Game
import random
import time
import sys
from itertools import permutations
import copy
from collections import Counter
from typing import List


playersTurn = True
playerScore = 0
computerScore = 0

roundNumber = 0


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

def displayComputerHand(hand1):
    print("Computer Hand: \n=====================================")

    for card in hand1:
        print(str(hand1.index(card)+1) + ": " + str(card.value) + " of " + str(card.suit))

def displayHand(hand1):
    print("\nPlayer hand: \n=====================================")

    for card in hand1:
        print(str(hand1.index(card)+1) + ": " + str(card.value) + " of " + str(card.suit))

    print("=====================================")

def placeCardInCrib(hand1, hand2):



    cribList = []
    randomNumber = random.randrange(0, len(hand2) - 1)
    cribChoice = input("\nChoose one card that you would like to discard, type the number next to the card: ")
    try:
        cribList.append(hand1[int(cribChoice) - 1])
        del hand1[int(cribChoice) - 1]
    except IndexError:
        print("Please select a number associated with a card.")
        placeCardInCrib(hand1,hand2)

    cribList.append(hand2[randomNumber])
    del hand2[randomNumber]
    
    return cribList, hand1, hand2

def displayPlayCount(pegCount):

    print("\nCount: " + str(pegCount))

def getPegChoice(hand1):

    pegChoice = int(input("What card would you like to play? "))


                # Add chosen card to the pegCount and complete logical operations deciding to award points to the player.

    try:
        cardValue = int(hand1[pegChoice - 1].value)
    except ValueError:
        cardValue = 10
    except IndexError:
        pass

    #remove chosen card from hand1

    del hand1[pegChoice - 1]

    return cardValue, hand1

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
    
def computerPegEval(pegCount):

    global computerScore
    


    if(pegCount == 15):
        print("The computer made 15, giving 2 points to the computer.\n")
        computerScore += 2
    if(pegCount == 31):
        print("The computer scored exactly 31, giving 2 point to the computer.\n")
        computerScore += 2
        
def computerGivesGo():

    global playerScore
    print("The computer gives a go, giving a point to the player.\n")
    playerScore += 1 

def playerGivesGo():

    global computerScore
    print("The player gives a go, giving a point to the computer.\n")
    computerScore += 1

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

def playRoundStartComputer(hand1, hand2):

    count = 0
    while(count <= 31):

        #computers turn:

        displayPlayCount(count)

        hand2, count = getAndPlayCardComputer(hand2, count)
            
        displayPlayCount(count)

        #take players turn next:
        try:
            hand1, count = getAndPlayCardPlayer(hand1, count)
        except TypeError:
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

def displayPlayMove(player, value, totalCount):

    if(value == 8):
        print("\nThe " + player + " played an " + str(value) + ". Making the total count " + str(totalCount))
    else:
        print("\nThe " + player + " played a " + str(value) + ". Making the total count " + str(totalCount))
    
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

            count = 0
            while(count <= 31):

                #get computer card and remove from hand, add to count and evaluate for points. 

                random.shuffle(hand2)
                CPUcardOfChoice = hand2[0]
                hand2.remove(CPUcardOfChoice)

                try:
                    count += int(CPUcardOfChoice.value)
                except ValueError:
                    count += 10

                displayPlayMove("computer",CPUcardOfChoice.value,count)

                computerPegEval(count)

                #get players card, remove from total hand, and eval points.

                displayPlayCount(count)
                displayHand(hand1)
                numberChoice = int(input("What card would you like to play? "))
                cardOfChoice = hand1[numberChoice - 1]

                #add value of card to count, eval 15s, and remove chosen card from players hand. 

                try:
                    count += int(cardOfChoice.value)
                except ValueError:
                    count += 10

                playerPegEval(count)
                hand1.remove(cardOfChoice)
                displayPlayMove("player",cardOfChoice.value,count)


    return hand1Copy, hand2Copy
        # as soon as the outside while loop exits, check to see who has the remaining cards

def flipCoinForFirstTurn():

    thisNumber = random.random()
    global playersTurn
    if(thisNumber > .5):
        playersTurn = True
    else:
        playersTurn = False

def revealCard(deck):



    topCard = deck[0]
    topCardVal = topCard.value

    if(topCardVal == 11):
        topCardVal = "Jack"
    elif(topCardVal == 12):
        topCardVal == "Queen"
    elif(topCardVal == 13):
        topCardVal = "King"


    for remaining in range(3, 0, -1):
        sys.stdout.write("\r")
        sys.stdout.write("Card will be revealed in:{:2d}".format(remaining)) 
        sys.stdout.flush()
        time.sleep(1)

    print("\n=====================================")
    sys.stdout.write("\r" + str(topCardVal) + " of " + str(topCard.suit) + " was drawn from the deck!\n" + "=====================================\n")
    
    if(topCard.value == "Jack" and playersTurn == True):
        print("\nThe player cut a jack, giving them a point.\n")
    elif(topCard.value == "Jack" and playersTurn == False):
        print("\nThe computer cut a jack, giving it a point.\n")

    return topCard
    
def countFifteens(hand1, hand2):


    global playerScore
    global computerScore

    hand1Vals = []
    hand2Vals = []

    # collect values for 15s calculation

    for card in hand1:
        try:
            hand1Vals.append(int(card.value))
        except ValueError:
            hand1Vals.append(10)

   

    # perform 15s calculation with list of exclusive values.


    hand1ValsPerm = permutations(hand1Vals)
    calculationList = []
    fifteens = 0
    
 
        
    for perm in hand1ValsPerm:
        for value in perm:
            calculationList.append(value)

            if(sum(calculationList) == 15 and len(calculationList) == 3 and calculationList[0] == 5):
                fifteens += 1
            elif(sum(calculationList) == 15 and len(calculationList) == 3):
                fifteens += 1
            elif(sum(calculationList) == 15):
                fifteens += 1
                continue
        calculationList.clear()
        
    
                
    totalPointsFromFifteens = 2*(int(fifteens/12))
    playerScore += totalPointsFromFifteens
    
    #and now for hand2

    calculationList = []

    for card in hand2:
        try:
            hand2Vals.append(int(card.value))
        except ValueError:
            hand2Vals.append(10)

 

    hand2ValsPerm = permutations(hand2Vals)

    # set 15 count back at 0

    fifteens = 0

    for perm in hand2ValsPerm:
        for value in perm:
            calculationList.append(value)

            if(sum(calculationList) == 15 and len(calculationList) == 3 and calculationList[0] == 5):
                fifteens += 1
            elif(sum(calculationList) == 15 and len(calculationList) == 3):
                fifteens += 1
            elif(sum(calculationList) == 15):
                fifteens += 1
                continue
        calculationList.clear()
   
    totalPointsFifteensComputer = 2*(int(fifteens/12))
    computerScore += totalPointsFifteensComputer


    # take original hand and use it to collect pairs/trios/runs 
    # assign face cards a value of 11 12 13 and compare them that way to make run calculation much easier. 


    return totalPointsFromFifteens, totalPointsFifteensComputer  

def countPairsRuns(hand1):



    global playerScore
    global computerScore


    # take original hand and use it to collect pairs/trios/runs 
    # assign face cards a value of 11 12 13 and compare them that way to make run calculation much easier. 
    hand1Vals = []


    for card in hand1:
        try:
            hand1Vals.append(int(card.value))
        except ValueError:
            if(card.value == "Jack"):
                hand1Vals.append(11)
            elif(card.value == "Queen"):
                hand1Vals.append(12)
            elif(card.value == "King"):
                hand1Vals.append(13)

        
    print(hand1Vals)
    


    

    #run evaluation
    '''
    In cribbage, a player has a hand of 5 cards when counting points. 
    
    If a player has a hand with 3 sequential cards in a row, they are awarded 3 points. 
    Same goes for a run of 4 and a run of 5, each awarding 4 and 5 points, respectively. 
    
    For example if I have a hand: [1,2,3,6,8] (usually in the form of playing cards), 
    I would earn 3 points, for the run of three in the first three elements of the list.
    '''
    # sort hand ascending order
    hand = sorted(hand1Vals)
    
    # get longest sequence
    totalpoints = 1

    ### WORKS, BUT DOES NOT FACTOR IN MORE THAN A DUPLICATE OF 2.: 

    # check to see if list has duplicates.

    if(len(hand) != len(set(hand))):

        # create deep copy of list

        duplicateList = copy.deepcopy(hand)

        # create two list, each with the one of the duplicates in them.

        for i in range(len(hand)):
            try:
                if(hand[i] == hand[i + 1]):
                    del duplicateList[i+1]
                    del hand[i+1]
            except IndexError:
                continue

        # run both lists through the run calculator. 

        for i in range(3):
            if(hand[i+1] == hand[i] + 1):
                totalpoints += 1
            elif totalpoints < 3:
                totalpoints = 1

        if totalpoints < 3:
            totalpoints = 0

        totalpoints2 = 1

        for i in range(3):
            if(duplicateList[i+1] == duplicateList[i] + 1):
                totalpoints2 += 1
            elif totalpoints2 < 3:
                totalpoints2 = 1

        if totalpoints2 < 3:
            totalpoints2 = 0

        return totalpoints + totalpoints2

    else:
        
        for i in range(4):
            if hand[i+1] == hand[i] + 1:
                totalpoints += 1
            elif totalpoints < 3:
                totalpoints = 1

    # score if continuous sequence is greater or equal than 3
        if totalpoints < 3:
            totalpoints = 0

        return totalpoints
    

    return totalpoints


    # for i in range(len(hand1Vals)):
    #     try:
    #         if(hand1Vals[i] == (hand1Vals[i + 1] - 1) and hand1Vals[i] == (hand1Vals[i + 2] - 2) 
    #         and hand1Vals[i] == (hand1Vals[i + 3] - 3) and hand1Vals[i] == (hand1Vals[i + 4] - 4)):
    #             playerScore += 5
    #             break
    #         else: 
    #             pass
    #     except IndexError:
    #         pass
    #     try:
    #         if(hand1Vals[i] == (hand1Vals[i + 1] - 1) and hand1Vals[i] == (hand1Vals[i + 2] - 2) 
    #         and hand1Vals[i] == (hand1Vals[i + 3] - 3)):
    #             playerScore += 4
    #         else:
    #             pass
    #     except IndexError:
    #         pass
    #     try:
    #         if(hand1Vals[i] == (hand1Vals[i + 1] - 1) and hand1Vals[i] == (hand1Vals[i + 2] - 2) 
    #         and hand1Vals[i] == (hand1Vals[i + 3] - 3)):
    #             playerScore += 3
    #             break
    #         else:
    #             pass
    #     except IndexError:
    #         pass

    #run evaluation


    # for i in range(len(hand1Vals)):
    #     if(i == 0):
    #         if(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2 and hand1Vals[i] == hand1Vals[i+3] - 3 and hand1Vals[i] == hand1Vals[i+4] - 4):
    #             totalPoints += 5
    #             break
    #         elif(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2 and hand1Vals[i] == hand1Vals[i+3] - 3):
    #             totalPoints += 4
    #         elif(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2):
    #             totalPoints += 3
    #     elif(i == 1):
    #         if(totalPoints == 4):
    #             pass
    #         elif(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2 and hand1Vals[i] == hand1Vals[i+3] - 3):
    #                 totalPoints += 4
    #         if(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2):
    #             totalPoints  += 3
    #     elif(i == 2):
    #         if(hand1Vals[i] == hand1Vals[i+1] - 1 and hand1Vals[i] == hand1Vals[i+2] - 2):
    #             totalPoints += 3

        
    
         

    # https://old.reddit.com/r/learnpython/comments/k3l53j/cribbage_run_evaluator_in_python/

def multipleDuplicates(hand) -> bool:

    counts = Counter(hand)
    listOfCounts = counts.values()
    

    numOfDuplicates = 0

    for each in listOfCounts:
        if(each > 1):
            numOfDuplicates += 1


    if numOfDuplicates > 1:
        return True
    else:
        return False

def evalDuplicateOfThree(handOfThree):

    totalScore = 0

    for i in range(2):
        if(handOfThree[i] == handOfThree[i + 1] - 1 and handOfThree[i] == handOfThree[i+2] - 2):
            totalScore += 3

    return totalScore

def evaluateRunPoints(hand):

    totalpoints = 1

    for i in range(4):
        if hand[i+1] == hand[i] + 1:
            totalpoints += 1
        elif totalpoints < 3:
            totalpoints = 1

    # score if continuous sequence is greater or equal than 3
    if totalpoints < 3:
        totalpoints = 0


    return totalpoints

def evaluatePairs(hand1):

    totalpoints = 0

    hand = []

    for i in hand1:
        hand.append(i.value)

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
    
def score_runs(hand1):
    '''
    In cribbage, a player has a hand of 5 cards when counting points. 
    
    If a player has a hand with 3 sequential cards in a row, they are awarded 3 points. 
    Same goes for a run of 4 and a run of 5, each awarding 4 and 5 points, respectively. 
    
    For example if I have a hand: [1,2,3,6,8] (usually in the form of playing cards), 
    I would earn 3 points, for the run of three in the first three elements of the list.
    '''
    hand1Vals = []

    for card in hand1:
        try:
            hand1Vals.append(int(card.value))
        except ValueError:
            if(card.value == "Jack"):
                hand1Vals.append(11)
            elif(card.value == "Queen"):
                hand1Vals.append(12)
            elif(card.value == "King"):
                hand1Vals.append(13)


    hand = []
    # sort hand ascending order
    for value in hand1Vals:
        hand.append(value)

  

    hand = sorted(hand)
    setHand = set(hand)
    
    
    # get longest sequence
    totalpoints = 0

    ### WORKS, BUT DOES NOT FACTOR IN MORE THAN A DUPLICATE OF 2.: 

    #Checks for multiple duplicats in the list, and if present, assigns the list to a set list and iterates through evaluation 4 times.

    if(multipleDuplicates(hand) == True):

        coolList = list(set(hand))

        # make length of the list 5

        coolList.append(0)
        coolList.append(0)

        #evaluations

        for i in range(4):
            totalpoints += evaluateRunPoints(coolList)

        return totalpoints

    else:
        pass



    # check to see if list has a dhuplicate of 3:

    if(len(hand) != len(set(hand)) and len(set(hand)) == 3):

        #create four lists that will be filled with many valees pertaining to the iterations.

        list1 = []
        list2 = []
        list3 = []

        # in a sorted list, check to see if there is a duplicate of three at the start, middle, and end of the list.

        #START:

        for val in set(hand):
            for i in range(3):
                if(val == hand[i] and val == hand[i+1] and val == hand[i+2]):
                    for val in set(hand):
                        list1.append(val)
                else:
                    continue

        

       

        #MIDDLE: 

        for val in set(hand):
            for i in range(3):
                if(val == hand[i + 1] and val == hand[i + 2] and val == hand[i + 3]):
                    for val in setHand:
                        list1.append(val)
                        list2.append(val)
                        list3.append(val)
                        
                else:
                    continue

        #END:
        
        for val in set(hand):
            for i in range(2, 0, -1):
                if(val == hand[i] and val == hand[i+1] and val == hand[i+2]):
                    for val in setHand:
                        list1.append(val)
                        list2.append(val)
                        list3.append(val)
                        
                else:
                    continue

        #adding extra elements to the list so that no index error occurs.

        for i in range(2):
            list1.append(0)

        

        # evaluate the new list containing the set values an appropriate number of times.  

        if(len(list1) > 2):
            for i in range(3):
                totalpoints += evaluateRunPoints(list1)


        
    elif(len(hand) != len(set(hand))):

        # create deep copy of list

        duplicateList = copy.deepcopy(hand)

        # create two list, each with the one of the duplicates in them.

        for i in range(len(hand)):
            try:
                if(hand[i] == hand[i + 1]):
                    del duplicateList[i+1]
                    del hand[i+1]
            except IndexError:
                continue

        # run both lists through the run calculator. 

        duplicateList.append(0)
        hand.append(0)

        totalpoints += evaluateRunPoints(duplicateList)
        totalpoints += evaluateRunPoints(hand)

        return totalpoints

    else:
        
        totalpoints += evaluateRunPoints(hand)
    

    return totalpoints

def countFifteensSingular(hand):

    handVals = []
    calculationList = []
    fifteens = 0

    #take all values from the hand and add them to a separate list of values.

    for card in hand:
        try:
            handVals.append(int(card.value))
        except ValueError:
            handVals.append(10)

    #make permutations out of the list of values. 

    handValsPerm = permutations(handVals)

    #evaluate each permutation for combinations equaling 15.
    
    
    for perm in handValsPerm:
       
        for value in perm:

            calculationList.append(value)

            if(sum(calculationList) == 15 and len(calculationList) == 5):
                fifteens += .1
            elif(sum(calculationList) == 15 and len(calculationList) == 3):
                fifteens += 1
            elif(sum(calculationList) == 15):
                fifteens += 1
                continue
        calculationList.clear()
        
    #for some reason, the total fifteens counted is always divisible by 12.. . not sure why, but working around it to get the desuired answer.
                
    totalPointsFromFifteens = 2*(int(round(fifteens)/12))

    if(totalPointsFromFifteens % 2 == 1):
        totalPointsFromFifteens += 1 

    return totalPointsFromFifteens

def cribCount(hand, turn):

    global playerScore
    global computerScore

    if(turn == True):
        #players crib
        #evaluate all cards:
        playerScore += score_runs(hand)
        playerScore += evaluatePairs(hand)
        playerScore += countFifteensSingular(hand)
    elif(turn == False):
        #computers crib
        #evaluate all cards:
        computerScore += score_runs(hand)
        computerScore += evaluatePairs(hand)
        computerScore += countFifteensSingular(hand)
    
def displayCrib(hand, turn):

    if(turn == True):
        print("\nIt is the player's turn, so the player gets the crib this turn\n")
        print("\nThe Crib: \n=====================================")

        for card in hand:
            print(str(hand.index(card)+1) + ": " + str(card.value) + " of " + str(card.suit))

        print("=====================================")

    elif(turn == False):
        print("\nIt is the computer's turn, so the computer gets the crib this turn.\n")
        print("\nThe Crib: \n=====================================")

        for card in hand:
            print(str(hand.index(card)+1) + ": " + str(card.value) + " of " + str(card.suit))

        print("=====================================")



def main():

#initialize global variables 

    global computerScore
    global playerScore
    global roundNumber
    global playersTurn

    #print welcome message on the first round

    if(roundNumber == 0):
        print("=====================================\n")
        print("Welcome to Cribbage.py!  Score 121 Points to Win the Game.  Good Luck!")

        suits = ["spades","clubs","hearts","diamonds"]
        deck = [Card(value, suit) for value in range(1, 14) for suit in suits]

        #flip a coin for the first turn.

       # flipCoinForFirstTurn()
        playerTurn = True
    else: 
        suits = ["spades","clubs","hearts","diamonds"]
        deck = [Card(value, suit) for value in range(1, 14) for suit in suits]
        random.shuffle(deck)
        #negate players turn bool:
        playersTurn = not(playersTurn)



#takes note of players current score so that the points made this round can be calculated and displayed after the point addition. 

    lastPlayerScore = playerScore
    lastComputerScore = computerScore

#shuffle deck and give cards to two different players.

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


    

# let user select which cards to put into the crib.


    #take first two cards.
    displayHand(hand1)
    cribCards, hand1, hand2 = placeCardInCrib(hand1, hand2)
    #take second two cards.
    displayHand(hand1)
    secondCribCards, hand1, hand2 = placeCardInCrib(hand1, hand2)

    #add cards from second call into the cribCards list.
    for card in secondCribCards:
        cribCards.append(card)

# reveal card drawn from top of deck

    topCard = revealCard(deck)
    
    
# initiate the play process.
# 
# 

    print("The play is about to begin.\n")

    #hand1, hand2 = initiatePlay(hand1, hand2)


# count up the points in each hand

    #append topcard to list of both hands so that counting may include the drawn card. 

    hand1.append(topCard)
    hand2.append(topCard)

    #create two variables used to count the points made by both the player and the computer this round.

    lastPlayerScore = playerScore
    lastComputerScore = computerScore

    playerScore += countFifteensSingular(hand1)
    computerScore += countFifteensSingular(hand2)

    playerScore += score_runs(hand1)
    computerScore += score_runs(hand2)
    playerScore += evaluatePairs(hand1)
    computerScore += evaluatePairs(hand2)

    #add this rounds points to total player/computer score.

    #calculate points earned this round.

    playerPointsEarnedThisRound = playerScore - lastPlayerScore
    computerPointsEarnedThisRound = computerScore - lastComputerScore

    
    displayHand(hand1)
    print("\nThe player's hand scores " + str(playerPointsEarnedThisRound) + " making the player's total score: " + str(playerScore) + "\n")
    displayComputerHand(hand2)
    print("\nThe computer's hand scores " + str(computerPointsEarnedThisRound) + " making the computer's total score: " + str(computerScore) + "\n") 

    #count the points in the crib and add them to each players score depending on who's turn it is. 

    #now count the crib. 

    #display crib and who has it
    displayCrib(cribCards, playersTurn)
    #add top card to the crib
    cribCards.append(topCard)
    #count the crib
    cribCount(cribCards, playersTurn)

    
    
    

    #display the hand as well as the points earned this round.


    displayHand(hand1)
    print("\nThe player's hand scores " + str(playerPointsEarnedThisRound) + " making the player's total score: " + str(playerScore) + "\n")
    displayComputerHand(hand2)
    print("\nThe computer's hand scores " + str(computerPointsEarnedThisRound) + " making the computer's total score: " + str(computerScore) + "\n") 

    
    

    while(playerScore < 121 and computerScore < 121):

        #increase round number and repeat the process.

        roundNumber += 1
        main()
    
    if(playerScore >= 121):
        print("The player has won the game, congratulations!")
    elif(computerScore >= 121):
        print("The computer has beaten you, get better.")

    

main()



