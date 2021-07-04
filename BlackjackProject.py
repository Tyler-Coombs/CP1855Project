#!/usr/bin/env python3
import random
import db #import module created to write/read money file
#db.readMoney()
#db.writeMoney()

print("BLACKJACK!")
print("Blackjack payout is 3:2")

def deckOfCards():
    #sets the card types and values
    cardValue = ['Ace','2','3','4','5','6','7','8','9','10','J','Q','K']
    cardType = ['Hearts','Spades','Clubs','Diamonds']
    deck = []
    #This iterates all 52 cards into a deck
    for i in cardType:
        for j in cardValue:
            deck.append(j + ' of ' + i)
    return deck

def pointValue(card):
    #only reading first slice to determine value of the card
    if card[:1] in ('J','Q','K','10'):
        return int(10)
    elif card[:1] in ('2','3','4','5','6','7','8','9'):
        #card[:1] example '2' out of the full '2 of Hearts' string
        return int(card[:1])
    elif card[:1] == 'A':
        print ("\n"+ str(card))
        num = input("Do you want this to be 1 or 11?\n>")
        while num !='1' or num !='11':
            if num == '1':
                return int(1)
            elif num == '11':
                return int(11)
            else:
                num = input("Do you want this to be 1 or 11?\n>")

def dealerHand(deck):
    dealerHand = []
    card = random.choice(deck)
    dealerHand.append(card)
    print(dealerHand)
    return dealerHand

def playerHand(deck):
    playerHand = []
    card = random.choice(deck)
    playerHand.append(card)
    print(playerHand)
    return playerHand

def hitOrStand():
    playerChoice = "hit"
    pass

def dealerScore(dealerHand):
    points = 0
    for card in dealerHand:
        points += pointValue(card)
        return points

def playerScore(playerHand):
    points = 0
    for card in playerHand:
        points += pointValue(card)
        return points

def playerBet(money):
    pass

def winnings(money):
    pass

def readMoney():
    money = 0
    try:
        with open("money.txt") as file:
            money = file.read()
        return float(money)
    except FileNotFoundError:
        print("Could not find money file.")
        exit_program()
    except Exception as e:
        print(type(e), e)
        exit_program()

def writeMoney(money):
    with open("money.txt", "w") as file:
        file.write(money)

def playGame():
    pass

def main():
    deck = deckOfCards()
    #print(deck)
    dealerHand(deck)

if __name__ == "__main__":
    main()
