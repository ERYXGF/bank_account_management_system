"""
Main CLI interface for the Bank Account System
"""

from models import Bank
from exceptions import (
    AuthenticationError,
    InsufficientFundsError,
    MinimumBalanceError,
    OverdraftLimitError
)
import os

DATA_FILE = "data/bank.json"


def load_bank():
    """
    Loads bank info from the json file.
    """
    bank = Bank("MyBank")

    if os.path.exists(DATA_FILE):
        bank.load_from_json(DATA_FILE)

    return bank


def save_bank(bank):
    """
    Saves bank info to the json file.
    """
    bank.save_to_json(DATA_FILE)


def main():
    """
    Main function that serves as the user interface.
    """
    bank = load_bank()

    while True:
        print("\n=== BANK MENU ===")
        print("1. Create savings account")
        print("2. Create current account")
        print("3. Deposit")
        print("4. Withdraw")
        print("5. Transfer")
        print("6. Check balance")
        print("7. View statement")
        print("8. Apply monthly interest")
        print("9. View total assets")
        print("0. Quit")

        choice = input("Choose an option: ")

        try:
            # CREATE SAVINGS ACCOUNT
            if choice == "1":
                name = input("Owner name: ")
                pin = input("PIN (4 digits): ")

                acc = bank.create_savings_account(name, pin)
                print(f"Account created: {acc}")

                save_bank(bank)

            # CREATE CURRENT ACCOUNT
            elif choice == "2":
                name = input("Owner name: ")
                pin = input("PIN (4 digits): ")

                acc = bank.create_current_account(name, pin)
                print(f"Account created: {acc}")

                save_bank(bank)

            # DEPOSIT
            elif choice == "3":
                acc_num = int(input("Account number: "))
                amount = float(input("Amount: "))
                pin = input("PIN: ")

                balance = bank.deposit(acc_num, amount, pin)
                print(f"New balance: {balance}")

                save_bank(bank)

            # WITHDRAW
            elif choice == "4":
                acc_num = int(input("Account number: "))
                amount = float(input("Amount: "))
                pin = input("PIN: ")

                balance = bank.withdraw(acc_num, amount, pin)
                print(f"New balance: {balance}")

                save_bank(bank)

            # TRANSFER
            elif choice == "5":
                from_acc = int(input("From account: "))
                to_acc = int(input("To account: "))
                amount = float(input("Amount: "))
                pin = input("PIN: ")

                balances = bank.transfer(from_acc, to_acc, amount, pin)
                print(f"Transfer complete. New balances: {balances}")

                save_bank(bank)

            # CHECK BALANCE
            elif choice == "6":
                acc_num = int(input("Account number: "))
                pin = input("PIN: ")

                balance = bank.get_balance(acc_num, pin)
                print(f"Balance: {balance}")

            # VIEW STATEMENT
            elif choice == "7":
                acc_num = int(input("Account number: "))
                pin = input("PIN: ")

                statement = bank.get_statement(acc_num, pin)
                print(statement)

            # APPLY INTEREST
            elif choice == "8":
                pin = input("PIN (for savings accounts): ")

                results = bank.apply_monthly_interest(pin)
                print("Interest applied:", results)

                save_bank(bank)

            # TOTAL ASSETS
            elif choice == "9":
                print(f"Total bank assets: {bank.total_assets()}")

            # QUIT
            elif choice == "0":
                save_bank(bank)
                print("Goodbye!")
                break

            else:
                print("Invalid option. Try again.")

        # 🔴 EXCEPTION HANDLING (VERY IMPORTANT)
        except AuthenticationError as e:
            print(f"Authentication error: {e}")

        except InsufficientFundsError as e:
            print(f"Insufficient funds: {e}")

        except MinimumBalanceError as e:
            print(f"Minimum balance error: {e}")

        except OverdraftLimitError as e:
            print(f"Overdraft limit error: {e}")

        except ValueError as e:
            print(f"Value error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
