import sys


def load_bank():
    try:
        with open("money.txt") as file:
            bank = float(file.readline())
        print(f"\nMoney: ${bank}")
        while bank < 5:
            print("\nYou don't have enough money in your account to play.")
            bank = deposit_money(bank)
        return bank
    except FileNotFoundError:
        print("File not found. Closing program.")
        sys.exit(1)
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def save_bank(bank):
    try:
        with open("money.txt", "w") as file:
            file.write(f"{bank}")
    except Exception as e:
        print("Unknown error occurred. Closing program.")
        print(type(e), e)
        sys.exit(1)


def deposit_money(bank):
    while True:
        try:
            choice = input("\nWould you like to add more money to your account? (y/n) ")
            if choice.lower() == "y":
                deposit = float(input("\nHow much would you like to deposit? "))
                if deposit <= 0:
                    print("Deposit amount must be greater than 0.")
                    continue
                bank += deposit
                save_bank(bank)
                print(f"\nMoney: ${bank}")
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


def main():
    print("")


if __name__ == '__main__':
    main()
