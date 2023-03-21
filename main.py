import sys
import csv


def load_bank():
    while True:
        try:
            with open("bank.txt") as file:
                bank = float(file.readline())
            print(f"\nMoney: {bank}")
            wager = float(input("Bet amount: "))
            if wager <= 5:
                print("Bet amount must be greater than $5.")
                continue
            if wager > bank:
                print("Bet amount must be lower than your total amount of money")
                continue
            else:
                bank -= wager
                save_bank(bank)
                break
        except ValueError:
            print("Please enter a valid number greater than 5.")
        except FileNotFoundError:
            print("File not found. Closing program.")
            sys.exit(1)
        except Exception as e:
            print("Unknown error occurred. Closing program.")
            print(type(e), e)
            sys.exit(1)
    return bank


def save_bank(bank):
    try:
        with open("bank.txt", "w") as file:
            file.write(f"{bank}")
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


def main():

    print("BLACKJACK!")
    print("Blackjack payout is 3:2")

    bank = load_bank()
    deck = load_deck()

    print(f"{bank}")
    print(f"{deck}")


if __name__ == '__main__':
    main()
