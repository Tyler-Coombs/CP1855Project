#!/usr/bin/env python3
import sys
import random
import db #import module created to write/read money file

#function to exit from the program 
def exit_program():
    print("Exiting program. Bye!")
    sys.exit()

#function to generate deck of cards as list of lists
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

#function to get value of each card
def pointValue(card):
    #only reading first slice to determine value of the card
    if card[:1] in ('J','Q','K'):
        return int(10)
    #checks for the card beginning with a 1
    elif card[:1] == '1':
        return int(10)
    elif card[:1] in ('2','3','4','5','6','7','8','9'):
        #card[:1] example '2' out of the full '2 of Hearts' string
        return int(card[:1])
    elif card[:1] == 'A':
        return int(11)

#function to deal a random card
def dealCard(deck):
    card = random.choice(deck)
    return card

#function to get player bet
def playerBet(money):
    while True:
        try:
            betAmount = float(input("Bet Amount: "))
            if betAmount < 5 or betAmount > 1000:
                print("Invalid bet amount. Please bet between 5 and 1000.")
                continue
            elif betAmount > float(money[0]):
                print("Invalid bet amount. You cannot bet more money than you have.")
                continue
            else:
                newMoney = float(money[0]) - round(betAmount, 2)
                money.clear()
                money.append(newMoney)
                db.writeMoney(money)
                return betAmount
                break
        except ValueError:
            print("Please enter a valid amount between 5 and 1000.")
            continue
        except Exception as e:
            print(type(e), e)
            continue

#gameplay function
def playGame(deck):
    playerHand = []
    dealerHand = []
    playerScore = 0
    dealerScore = 0
    winnings = 0
    money = db.readMoney()

    #prompt player to buy more chips if they have less than minimum bet in wallet
    if float(money[0]) < 5:
        print("Money: " + str(money[0]))
        print("You need more money to play.")
        print()
        buyChips = input("Would you like to add money to the wallet? (y/n) >>")
        while buyChips.lower() == "y":
            try:
                buyAmount = float(input("\nHow much money will you add? >>"))
                if buyAmount >= 5:
                    newMoney = float(money[0]) + buyAmount
                    money.clear()
                    money.append(newMoney)
                    db.writeMoney(money)
                    buyChips = "n"
                    print()
                else:
                    print("Minimum bet is 5. Please add a greater amount than minimum bet.")
                    continue
            except ValueError:
                print("Please enter a valid amount of money to add.")
                continue
            except Exception as e:
                print(type(e), e)
                continue
        
    if float(money[0]) >= 5:
        print("Money: " + str(money[0]))
        #get player bet
        betAmount = playerBet(money)

        #deal player a card
        card = dealCard(deck)
        playerHand.append(card)
        deck.remove(card)
        points = pointValue(card)
        playerScore += int(points)
        #allow player to choose the value of A
        if pointValue(card) == 11:
            while True:
                num = input("\nDo you want this Ace to be 1 or 11?\n>")
                if num == '1':
                    playerScore -= 10
                    break
                elif num == '11':
                    playerScore = playerScore
                    break
                else:
                    print("You must choose 1 or 11")
                    continue

        #deal dealer a card
        card = dealCard(deck)
        dealerHand.append(card)
        deck.remove(card)
        points = pointValue(card)
        dealerScore += points

        #deal player second card
        card = dealCard(deck)
        playerHand.append(card)
        deck.remove(card)
        points = pointValue(card)
        playerScore += points
        #allow user to choose value of A
        if pointValue(card) == 11:
            while True:
                num = input("\nDo you want this Ace to be 1 or 11?\n>")
                if num == '1':
                    playerScore -= 10
                    break
                elif num == '11':
                    playerScore = playerScore
                    break
                else:
                    print("You must choose 1 or 11")
                    continue

        #deal dealer second card
        card = dealCard(deck)
        dealerHand.append(card)
        deck.remove(card)
        points = pointValue(card)
        dealerScore += points
        #if the user has more than one ace, one will only count as 1 point
        if len(dealerHand) == 2:
            if pointValue(dealerHand[0]) == 11 and pointValue(dealerHand[1]) == 11:
                dealerScore -= 10

        #show one of dealer's cards and players cards
        print("\nDEALER'S SHOW CARD:")
        print(dealerHand[0])
        print("Hidden Card")
        print()
        print("YOUR CARDS:")
        print("\n".join(playerHand))
        print()

        #give player option to get dealt another card (hit) or to stick with what they have (stand)
        while playerScore < 21:
            choice = input("Hit or stand? (hit/stand): ")
            print()
            if choice.lower() == "hit":
                card = dealCard(deck)
                playerHand.append(card)
                deck.remove(card)
                points = pointValue(card)
                playerScore += points
                #allow player to choose the value of A
                if pointValue(card) == 11:
                    while True:
                        num = input("\nDo you want this Ace to be 1 or 11?\n>")
                        if num == '1':
                            playerScore -= 10
                            break
                        elif num == '11':
                            playerScore = playerScore
                            break
                        else:
                            print("You must choose 1 or 11")
                            continue
                print("YOUR CARDS")
                print("\n".join(playerHand))
                print()
                if dealerScore < 17: #when player hits, dealer should also get another card if their score is <17
                    card = dealCard(deck)
                    dealerHand.append(card)
                    deck.remove(card)
                    points = pointValue(card)
                    dealerScore += points
                    #in the presence of another A, set the value of A to 1 for the dealer
                    if len(dealerHand) >= 2 and pointValue(card) == 11:
                        if pointValue(dealerHand[0]) == 11 or pointValue(dealerHand[1]) == 11:
                            dealerScore -= 10
                continue
            elif choice.lower() == "stand":
                if dealerScore < 17: #when player stands, dealer should get cards until their score is >17
                    card = dealCard(deck)
                    dealerHand.append(card)
                    deck.remove(card)
                    points = pointValue(card)
                    dealerScore += points
                    #in the presence of another A, set the value of an A to 1 for the dealer
                    if len(dealerHand) >= 2 and pointValue(card) == 11:
                        if pointValue(dealerHand[0]) == 11 or pointValue(dealerHand[1]) == 11:
                            dealerScore -= 10
                break
            else:
                print("Invalid response. Please enter hit or stand.")
                continue

        #display points and dealer's cards
        print("DEALER'S CARDS")
        print("\n".join(dealerHand))
        print()
        print("YOUR POINTS:          " + str(playerScore))
        print("DEALER'S POINTS:   " + str(dealerScore))
        print()

        #code to decide winner/loser and payout
        if playerScore == 21 and dealerScore < 21:
            print("YOU HAVE A BLACKJACK!")
            print("YOU WIN!")
            winnings = round(betAmount * 1.5, 2)
            print("Winnings: " + str(winnings))
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif playerScore == 21 and dealerScore > 21:
            print("YOU HAVE A BLACKJACK!")
            print("YOU WIN!")
            winnings = round(betAmount * 1.5, 2)
            print("Winnings: " + str(winnings))
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif playerScore > dealerScore and playerScore < 21:
            print("YOU WIN!")
            winnings = round(betAmount * 1.5, 2)
            print("Winnings: " + str(winnings))
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif (playerScore < dealerScore and playerScore != 21) and dealerScore > 21:
            print("DEALER BUSTS!")
            print("YOU WIN!")
            winnings = round(betAmount * 1.5, 2)
            print("Winnings: " + str(winnings))
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif dealerScore > playerScore and dealerScore < 21:
            print("Sorry. You lose.")
            money = db.readMoney()
            print("Money: " + str(money[0]))
        elif dealerScore == 21 and playerScore < 21:
            print("Dealer has BLACKJACK.")
            print("Sorry. You lose.")
            money = db.readMoney()
            print("Money: " + str(money[0]))
        elif playerScore == 21 and dealerScore == 21:
            print("Draw. No winners.")
            winnings = betAmount
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif playerScore == dealerScore:
            print("Draw. No winners.")
            winnings = betAmount
            money = db.readMoney()
            newMoney = float(money[0]) + winnings
            money.clear()
            money.append(newMoney)
            db.writeMoney(money)
            print("Money: " + str(money[0]))
        elif playerScore > 21:
            print("BUST. Sorry. You lose.")
            money = db.readMoney()
            print("Money: " + str(money[0]))

def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")
    print()
    playAgain = "y"
    deck = deckOfCards()
    while playAgain.lower() == "y":
        playGame(deck)
        playAgain = input("\nPlay again? (y/n): ")
        print()
    print("Come back soon! \nBye!")


if __name__ == "__main__":
    main()
