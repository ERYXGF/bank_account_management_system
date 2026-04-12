from datetime import date
import json
from models.savings_account import SavingsAccount
from models.current_account import CurrentAccount


class Bank:
    """
    Bank class, contains all the bank's info.
    """

    def __init__(self, name):
        self.name = name
        self._accounts = {}
        self.created_date = date.today()

    def create_savings_account(self, owner_name, pin):
        account = SavingsAccount(owner_name, pin)

        # Extract account number safely
        acc_number = account.to_dict(pin)["account_number"]

        self._accounts[acc_number] = account
        return account

    def create_current_account(self, owner_name, pin):
        account = CurrentAccount(owner_name, pin)

        acc_number = account.to_dict(pin)["account_number"]

        self._accounts[acc_number] = account
        return account

    def _find_account(self, account_number):
        if account_number not in self._accounts:
            raise ValueError("Account not found.")
        return self._accounts[account_number]

    def deposit(self, account_number, amount, pin):
        account = self._find_account(account_number)
        return account.deposit(amount, pin)

    def withdraw(self, account_number, amount, pin):
        account = self._find_account(account_number)
        return account.withdraw(amount, pin)

    def transfer(self, from_number, to_number, amount, pin):
        from_acc = self._find_account(from_number)
        to_acc = self._find_account(to_number)

        # Step 1: withdraw
        from_acc.withdraw(amount, pin, f"Transfer to {to_number}")

        try:
            # Step 2: deposit into destination
            # ⚠️ must pass SAME pin (design limitation)
            to_acc.deposit(amount, pin, f"Transfer from {from_number}")

        except Exception:
            # rollback
            from_acc.deposit(amount, pin, "Rollback transfer")
            raise

        return (
            from_acc.get_balance(pin),
            to_acc.get_balance(pin)
        )

    def get_balance(self, account_number, pin):
        account = self._find_account(account_number)
        return account.get_balance(pin)

    def get_statement(self, account_number, pin):
        account = self._find_account(account_number)
        return account.get_statement()

    def apply_monthly_interest(self, pin):
        results = {}

        for acc_num, account in self._accounts.items():
            if isinstance(account, SavingsAccount):
                interest = account.apply_interest(pin)
                results[acc_num] = interest

        return results

    def total_assets(self):
        total = 0

        for account in self._accounts.values():
            # We must use to_dict → only safe way without private access
            data = account._to_dict_internal()
            total += float(data["balance"])

        return total

    def __len__(self):
        return len(self._accounts)

    def save_to_json(self, filepath="data/bank.json"):
        data = {
            "name": self.name,
            "created_date": self.created_date.isoformat(),
            "accounts": [
                acc._to_dict_internal() for acc in self._accounts.values()
            ]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self, filepath="data/bank.json"):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.name = data["name"]
            self.created_date = date.fromisoformat(data["created_date"])
            self._accounts = {}

            for acc_data in data["accounts"]:
                if "interest_rate" in acc_data:
                    acc = SavingsAccount.from_dict(acc_data)
                else:
                    acc = CurrentAccount.from_dict(acc_data)

                acc_number = acc_data["account_number"]
                self._accounts[acc_number] = acc

        except FileNotFoundError:
            pass