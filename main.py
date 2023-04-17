import sys
import random
import db


def loadDeck():
    deck = []
    suits = ["\u2665", "\u2660", "\u2666", "\u2663"]  # Unicode for suits in a deck of cards

    # Adding cards 2 to 10 to the deck
    for i in range(2, 11):
        heartCard = [i, suits[0], i]
        deck.append(heartCard)
        spadeCard = [i, suits[1], i]
        deck.append(spadeCard)
        diamondCard = [i, suits[2], i]
        deck.append(diamondCard)
        clubCard = [i, suits[3], i]
        deck.append(clubCard)

    # Adding Jacks, Queens, Kings and Aces to the deck
    for i in range(len(suits)):
        jackCard = ["J", suits[i], 10]
        deck.append(jackCard)
        queenCard = ["Q", suits[i], 10]
        deck.append(queenCard)
        kingCard = ["K", suits[i], 10]
        deck.append(kingCard)
        aceCard = ["A", suits[i], 11]
        deck.append(aceCard)

    return deck


def dealPlayer(playerHand, deck):
    try:
        card = deck.pop(0)
        playerTotal = calculatePlayerTotal(playerHand)
        if card[0] == "A" and playerTotal + 11 < 21:
            choice = input("\nYou drew an Ace, do you want it to be high or low? ")
            if choice.lower() == "low":
                card = [card[0], card[1], 1]
        elif card[0] == "A" and playerTotal + 11 > 21:
            card = [card[0], card[1], 1]
        playerHand.append(card)
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def dealDealer(dealerHand, deck):
    try:
        card = deck.pop(0)
        dealerHand.append(card)
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def printHand(hand):
    for card in hand:
        print(f"{card[0]}{card[1]}  ", end="")


def calculatePlayerTotal(hand):
    total = 0

    for card in hand:
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

    # Ensuring aces are calculated properly for the dealer
    if total > 21:
        for card in hand:
            if card[0] == 'A' and total - 10 <= 21:
                total -= 10

    # Printing outcomes
    if total == 21 and (len(hand) == 2):
        print("Blackjack!!!")
    elif total > 21:
        print("Bust!")
    elif total == 21:
        print("21!")

    return total


def roundEnd(playerTotal, dealerTotal, bank, wager):
    print(f"\n\nYOUR POINTS:     {playerTotal}")
    print(f"DEALER'S POINTS: {dealerTotal}")

    # Calculating who wins and what happens with the bet
    if (playerTotal <= 21) and (dealerTotal > 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.saveBank(bank)
        return round(bank, 2)
    elif (playerTotal > dealerTotal) and (playerTotal <= 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.saveBank(bank)
        return round(bank, 2)
    else:
        print("\nSorry. You lose.")
        bank -= wager
        db.saveBank(bank)
        return round(bank, 2)


def main():
    print("BLACKJACK!")
    print("Blackjack payout is 3:2")

    choice = "y"
    deck = loadDeck()

    print("\nDealer is shuffling ...")
    random.shuffle(deck)

    bank = db.loadBank()
    print(f"\nMoney: ${round(bank, 2)}")

    while choice.lower() == "y":

        dealerHand = []
        playerHand = []

        if bank < 5:
            db.depositMoney(bank)

        # Check to see if the deck needs to be reshuffled
        if len(deck) < 10:
            print("\nDeck is low on cards, reshuffling...")
            deck = loadDeck()
            random.shuffle(deck)

        wager = db.getWager(bank)

        print("\nDEALER'S SHOW CARD:")
        dealDealer(dealerHand, deck)
        printHand(dealerHand)

        # Player gets two cards face up and dealer gets a face down card
        print("\n\nYOUR FIRST CARD:")
        dealPlayer(playerHand, deck)
        printHand(playerHand)

        print("\n\nDEALER GETS SECOND CARD AND ITS FACE DOWN..")
        dealDealer(dealerHand, deck)

        print("\nYOUR CARDS:")
        dealPlayer(playerHand, deck)
        printHand(playerHand)
        playerTotal = calculatePlayerTotal(playerHand)

        # Player's turn
        while playerTotal < 21:
            choice = input("\n\nHit or stand? (hit/stand): ")
            if choice.lower() == "hit":
                dealPlayer(playerHand, deck)
                print("\nYOUR CARDS:")
                printHand(playerHand)
                playerTotal = calculatePlayerTotal(playerHand)
            if choice.lower() == "stand":
                break

        # Dealer's turn
        print("\nDEALER REVEALS SECOND CARD:")
        printHand(dealerHand)
        dealerTotal = calculateDealerTotal(dealerHand)

        if playerTotal <= 21:
            while dealerTotal < 17 and dealerTotal < playerTotal:
                print("\n\nDEALER'S CARDS:")
                dealDealer(dealerHand, deck)
                printHand(dealerHand)
                dealerTotal = calculateDealerTotal(dealerHand)

        # End of round
        bank = roundEnd(playerTotal, dealerTotal, bank, wager)
        print(f"Money: ${bank}")

        choice = input("\nPlay again? (y/n) ")

    print("\nCome back soon!")
    print("Bye!")


if __name__ == '__main__':
    main()
