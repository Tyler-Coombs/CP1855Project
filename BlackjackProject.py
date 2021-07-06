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

def playerBet():
    money = db.readMoney()
    print("Money: " + money)
    betAmount = input("Bet Amount: ")
    if betAmount < 5 or betAmount > 1000:
        print("Invalid bet amount. Please bet between 5 and 1000.")
    elif betAmount > money:
        print("Invalid bet amount. You cannot bet more money than you have.")
    else:
        money = money - betAmount
        db.writeMoney()
        return betAmount

def winnings():
    betAmount = playerBet()
    winAmount = betAmount * 1.5
    money = db.readMoney()
    money = money + winAmount
    db.writeMoney(money)

def playGame(deck):
    playerHand = []
    dealerHand = []
    playerScore = 0
    dealerScore = 0


    print("DEALER'S SHOW CARD")
    dealerCard = random.choice(deck)
    dealerHand.append(dealerCard)
    deck.remove(dealerCard)
    card = dealerCard
    dealerScore += pointValue(card)
    print(dealerHand)
    if len(dealerHand) == 2:
        if pointValue(dealerHand[0]) == 11 and pointValue(dealerHand[1]) == 11:
            pointValue(dealerHand[1]) = 1
            dealerScore -= 10
    
    while len(playerHand) < 2:
        playerCard = random.choice(deck)
        playerHand.append(playerCard)
        deck.remove(playerCard)
        card = playerCard
        playerScore += pointValue(card)

        if len(playerHand) == 2:
            if pointValue(playerHand[0]) == 11 and pointValue(playerHand[1]) == 11:
                pointValue(playerHand[0]) = 1
                playerScore -= 10
        
        print("YOUR CARDS: ")
        print(playerHand)
        
    if playerScore == 21:
        print("YOU HAVE A BLACKJACK!")
        print("YOU WIN!")

    while playerScore < 21:
        choice = input("Hit or stand? (hit/stand): ")
        if choice.lower() == "hit"

            playerCard = random.choice(deck)
            playerHand.append(playerCard)
            deck.remove(playerCard)
            card = playerCard

            playerScore += pointValue(card)
            print(playerHand)
            continue

        elif choice.lower() == "stand"
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
        money = db.readMoney()
        print("Money: " + str(money)
        
    elif dealerScore > playerScore:
        print("Sorry. You lose.")
    elif dealerScore == 21 and playerScore < 21:
        print("Sorry. You lose.")
    elif playerScore == 21 and dealerScore == 21:
        print("Draw. No winners. You get your money back.")
    elif playerScore > 21:
        print("BUST. Sorry. You lose.")
        

def main():
    playAgain = "y"
    deck = deckOfCards()
    while playAgain.lower() == "y":

        playerBet()
        playGame()


        playAgain = input("Play again? (y/n): ")
        print()
    print("Come back soon! \nBye!")


if __name__ == "__main__":
    main()
