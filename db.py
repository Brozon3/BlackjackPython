import sys


def loadBank():
    bank = 10.00
    try:
        with open("money.txt") as file:
            bank = float(file.readline())
        while bank < 5:
            print("\nYou don't have enough money in your account to play.")
            bank = depositMoney(bank)
        return round(bank, 2)
    except FileNotFoundError:
        print(f"Couldn't find {file}. Your account will start with a balance of ${bank}.")
        return bank
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def saveBank(bank):
    try:
        with open("money.txt", "w") as file:
            file.write(f"{round(bank, 2)}")
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def depositMoney(bank):
    while True:
        try:
            choice = input("\nWould you like to add more money to your account? (y/n) ")
            if choice.lower() == "y":
                deposit = float(input("\nHow much would you like to deposit? "))
                if deposit <= 0:
                    print("Deposit amount must be greater than 0.")
                    continue
                bank += deposit
                saveBank(bank)
                print(f"\nMoney: ${round(bank, 2)}")
                return bank
            else:
                print("Once you had added more funds to your account you can come back and play.")
                sys.exit(1)
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print("Unknown error occurred. Closing program.")
            print(type(e), e)
            sys.exit(1)


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


def main():
    print("")


if __name__ == '__main__':
    main()
