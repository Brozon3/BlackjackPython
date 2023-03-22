import sys
import csv
import random
import db


def get_wager(bank):
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
        except Exception as e:
            print("Unknown error occurred. Closing program.")
            print(type(e), e)
            sys.exit(1)


def load_deck():
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
        number = random.randint(0, len(deck) - 1)
        card = deck.pop(number)
        hand.append(card)
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def print_hand(hand):
    for card in hand:
        print(f"{card[0]} of {card[1]}")


def calculate_total(hand):
    total = 0
    for card in hand:
        total += card[2]
    if total == 21:
        print("Blackjack!")
    if total > 21:
        print("Bust!")
    return total


def end_of_round(player_total, dealer_total, bank, wager):
    print(f"\nYOUR POINTS:     {player_total}")
    print(f"DEALER'S POINTS: {dealer_total}")

    if (player_total <= 21) and (dealer_total > 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.save_bank(bank)
        print(f"Money: {bank}")
    elif (player_total > dealer_total) and (player_total < 21) and (dealer_total < 21):
        print("\nYou win!")
        bank += round(1.5 * wager, 2)
        db.save_bank(bank)
        print(f"Money: {bank}")
    else:
        print("\nYou lose!")
        bank -= wager
        db.save_bank(bank)
        print(f"Money: {bank}")


def main():

    print("BLACKJACK!")
    print("Blackjack payout is 3:2")

    choice = "y"

    while choice.lower() == "y":

        bank = db.load_bank()
        wager = get_wager(bank)
        deck = load_deck()
        dealer_hand = []
        dealer_total = 0
        player_hand = []

        print("\nDealer is shuffling ...")
        random.shuffle(deck)

        print("\nDEALER'S SHOW CARD")
        deal(dealer_hand, deck)
        print_hand(dealer_hand)

        print("\nYOUR CARDS:")
        deal(player_hand, deck)
        deal(player_hand, deck)
        print_hand(player_hand)
        player_total = calculate_total(player_hand)

        while player_total < 21:
            choice = input("\nHit or stand? ")
            if choice.lower() == "hit":
                deal(player_hand, deck)
                print("\nYOUR CARDS:")
                print_hand(player_hand)
                player_total = calculate_total(player_hand)
            if choice.lower() == "stand":
                break

        while dealer_total < 17:
            print("\nDEALER'S CARDS:")
            deal(dealer_hand, deck)
            print_hand(dealer_hand)
            dealer_total = calculate_total(dealer_hand)

        end_of_round(player_total, dealer_total, bank, wager)

        choice = input("\nPlay again? (y/n) ")

    print("\nBye!")


if __name__ == '__main__':
    main()
