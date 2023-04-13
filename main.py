import sys
import csv
import random
import db


def getWager(bank):
    while True:
        try:
            wager = float(input("Bet amount: "))
            if wager < 5:
                print("Bet amount must be greater than $5.")
                continue
            elif wager > 1000:
                print("Bet amount must be lower than $1000.")
                continue
            elif wager > bank:
                print("Bet amount must be lower than your total amount of money.")
                continue
            else:
                return wager
        except ValueError:
            print("Please enter a valid number.")
            continue
        except Exception as e:
            print("Unknown error occurred. Closing program.")
            print(type(e), e)
            sys.exit(1)


def loadDeck():
    try:
        deck = []
        with open("deck.csv", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                card = [row[0], row[1], int(row[2])]
                deck.append(card)
        return deck
    except FileNotFoundError:
        print("File not found. Closing program.")
        sys.exit(1)
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def deal(hand, deck):
    try:
        card = deck.pop(0)
        hand.append(card)
        return hand
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def printHand(hand):
    for card in hand:
        print(f"{card[0]} of {card[1]}")


def calculateTotal(hand):
    total = 0

    for card in hand:
        if card[2] == 11 and total + 11 < 21:
            choice = input("Do you want your ace to be high or low? ")
            if choice.lower() == 'high':
                total += 11
            elif choice.lower() == 'low':
                total += 1
        elif card[2] == 11 and total + 11 > 21:
            total += 1
        else:
            total += card[2]

    if total == 21 and (len(hand) == 2):
        print("Blackjack!!!")
    elif total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")

    return total


def calculateDealerTotal(hand):
    total = 0

    for card in hand:
        total += card[2]

    if total > 21:
        for card in hand:
            if card[2] == 11 and total - 10 <= 21:
                total -= 10

    if total == 21 and (len(hand) == 2):
        print("Blackjack!!!")
    elif total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")

    return total


def endOfRound(player_total, dealer_total, bank, wager):
    print(f"\nYOUR POINTS:     {player_total}")
    print(f"DEALER'S POINTS: {dealer_total}")

    if (player_total <= 21) and (dealer_total > 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.save_bank(bank)
        print(f"Money: {bank}")
    elif (player_total > dealer_total) and (player_total <= 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.save_bank(bank)
        print(f"Money: {bank}")
    else:
        print("\nSorry. You lose.")
        bank -= wager
        db.save_bank(bank)
        print(f"Money: {bank}")


def main():

    print("BLACKJACK!")
    print("Blackjack payout is 3:2")

    choice = "y"
    deck = loadDeck()

    print("\nDealer is shuffling ...")
    random.shuffle(deck)

    while choice.lower() == "y":

        bank = db.load_bank()
        wager = getWager(bank)

        dealer_hand = []
        player_hand = []

        if len(deck) < 10:
            print("Deck is low on cards, reshuffling...")
            deck = loadDeck()
            random.shuffle(deck)

        print("\nDEALER'S SHOW CARD")
        deal(dealer_hand, deck)
        printHand(dealer_hand)

        print("\nYOUR CARDS:")
        deal(player_hand, deck)
        deal(dealer_hand, deck)
        deal(player_hand, deck)
        printHand(player_hand)
        player_total = calculateTotal(player_hand)

        while player_total < 21:
            choice = input("\nHit or stand? (hit/stand): ")
            if choice.lower() == "hit":
                deal(player_hand, deck)
                print("\nYOUR CARDS:")
                printHand(player_hand)
                player_total = calculateTotal(player_hand)
            if choice.lower() == "stand":
                break

        print("\nDealer flips second card:")
        printHand(dealer_hand)
        dealer_total = calculateDealerTotal(dealer_hand)

        if player_total <= 21:
            while dealer_total < 17 and dealer_total < player_total:
                print("\nDEALER'S CARDS:")
                deal(dealer_hand, deck)
                printHand(dealer_hand)
                dealer_total = calculateDealerTotal(dealer_hand)

        endOfRound(player_total, dealer_total, bank, wager)

        choice = input("\nPlay again? (y/n) ")

    print("\nBye!")


if __name__ == '__main__':
    main()
