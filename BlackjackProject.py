#!/usr/bin/env python3
import sys
import random
import db #import module created to write/read money file
#db.readMoney()
#db.writeMoney()

print("BLACKJACK!")
print("Blackjack payout is 3:2")

def exit_program():
    print("Exiting program. Bye!")
    sys.exit()

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

def playerPointValue(playerCard):
    #only reading first slice to determine value of the card
    if playerCard[:1] in ('J','Q','K','10'):
        return int(10)
    elif playerCard[:1] in ('2','3','4','5','6','7','8','9'):
        #card[:1] example '2' out of the full '2 of Hearts' string
        return int(playerCard[:1])
    elif playerCard[:1] == 'A':
        print ("\n"+ str(playerCard))
        num = input("Do you want this to be 1 or 11?\n>")
        while num !='1' or num !='11':
            if num == '1':
                return int(1)
            elif num == '11':
                return int(11)
            else:
                num = input("Do you want this to be 1 or 11?\n>")

def dealerPointValue(dealerCard):
    #only reading first slice to determine value of the card
    if dealerCard[:1] in ('J','Q','K','10'):
        return int(10)
    elif dealerCard[:1] in ('2','3','4','5','6','7','8','9'):
        #card[:1] example '2' out of the full '2 of Hearts' string
        return int(dealerCard[:1])
    elif dealerCard[:1] == 'A':
        print ("\n"+ str(dealerCard))
        num = input("Do you want this to be 1 or 11?\n>")
        while num !='1' or num !='11':
            if num == '1':
                return int(1)
            elif num == '11':
                return int(11)
            else:
                num = input("Do you want this to be 1 or 11?\n>")

#def dealerHand(deck):
  #  dealerHand = []
    #card = random.choice(deck)
    #dealerHand.append(card)
    #print(dealerHand)
    #return dealerHand

#def playerHand(deck):
  #  playerHand = []
   # card = random.choice(deck)
   # playerHand.append(card)
   # print(playerHand)
   # return playerHand

def hitOrStand():
    playerChoice = "hit"
    pass

def dealerScore(dealerHand):
    points = 0
    for dealerCard in dealerHand:
        points += dealerPointValue(dealerCard)
        return points

def playerScore(playerHand):
    points = 0
    for playerCard in playerHand:
        points += playerPointValue(playerCard)
        return points

def playerBet():
    money = db.readMoney()
    print("Money: " + str(money[0]))
    if float(money[0]) < 5:
        buyChips = str(input("Not enough chips. Buy more? (y/n)"))
        if buyChips.lower == "y":
            buyAmount = float(input("How many chips would you like to buy? "))
            money[0] = float(money[0]) + buyAmount
            db.writeMoney(money)
            return money
        else:
            print("You do not have enough chips to play.")
            exit_program()
    else:
        betAmount = float(input("Bet Amount: "))
        if betAmount < 5 or betAmount > 1000:
            print("Invalid bet amount. Please bet between 5 and 1000.")
        elif betAmount > float(money[0]):
            print("Invalid bet amount. You cannot bet more money than you have.")
        else:
            money[0] = float(money[0]) - betAmount
            #money.append(money[0])
            db.writeMoney(money)
            return betAmount

def winnings():
    betAmount = playerBet()
    winAmount = betAmount * 1.5
    money = db.readMoney()
    money = money + winAmount
    db.writeMoney(money)
    print("Money: " + str(money))


def playGame(deck):
    playerHand = []
    dealerHand = []
    playerScore = 0
    dealerScore = 0

    print("DEALER'S SHOW CARD")
    dealerCard = random.choice(deck)
    dealerHand.append(dealerCard)
    deck.remove(dealerCard)
    #card = dealerCard
    dealerScore += dealerPointValue(dealerCard)
    print(dealerHand)
    dealerCard = random.choice(deck)
    dealerHand.append(dealerCard)
    deck.remove(dealerCard)
    #card = dealerCard
    dealerScore += dealerPointValue(dealerCard)
    if len(dealerHand) == 2:
        if dealerPointValue(dealerHand[0]) == 11 and dealerPointValue(dealerHand[1]) == 11:
            dealerScore -= 10
    
    while len(playerHand) < 2:
        playerCard = random.choice(deck)
        playerHand.append(playerCard)
        deck.remove(playerCard)
        #card = playerCard
        playerScore += playerPointValue(playerCard)
        #playerScore = playerScore(playerHand)

        if len(playerHand) == 2:
            if playerPointValue(playerHand[0]) == 11 and playerPointValue(playerHand[1]) == 11:
                playerScore -= 10
        
        print("YOUR CARDS: ")
        print(playerHand)

    while playerScore < 21:
        choice = input("Hit or stand? (hit/stand): ")
        if choice.lower() == "hit":

            playerCard = random.choice(deck)
            playerHand.append(playerCard)
            deck.remove(playerCard)
            #card = playerCard

            playerScore += playerPointValue(playerCard)
            print(playerHand)
            continue

        elif choice.lower() == "stand":
            break

        else:
            print("Please enter hit or stand.")
            continue

    print("DEALER'S CARDS: ")
    print(dealerHand)

    print("YOUR POINTS:\t" + str(playerScore))
    print("DEALER'S POINTS:\t" + str(dealerScore))

    if playerScore == 21 and dealerScore < 21:
        print("YOU HAVE A BLACKJACK!")
        print("YOU WIN!")
        winnings()
    elif playerScore > dealerScore and playerScore < 21:
        print("YOU WIN!")
        winnings()
    elif dealerScore > playerScore and dealerScore < 21:
        print("Sorry. You lose.")
        money = db.readMoney()
        print("Money: " + str(money))
    elif dealerScore == 21 and playerScore < 21:
        print("Sorry. You lose.")
        money = db.readMoney()
        print("Money: " + str(money))
    elif playerScore == 21 and dealerScore == 21:
        print("Draw. No winners. You get your money back.")
        
    elif playerScore > 21:
        print("BUST. Sorry. You lose.")
        money = db.readMoney()
        print("Money: " + str(money))
        

def main():
    playAgain = "y"
    deck = deckOfCards()
    while playAgain.lower() == "y":

        playerBet()
        playGame(deck)


        playAgain = input("Play again? (y/n): ")
        print()
    print("Come back soon! \nBye!")


if __name__ == "__main__":
    main()
