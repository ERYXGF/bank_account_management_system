from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from models.transaction import Transaction
from exceptions import AuthenticationError, InsufficientFundsError
from security import hash_pin, verify_pin, validate_pin_format
from utils import format_account_number, format_date


class BankAccount:

    _account_counter = 10000000

    def __init__(self, owner_name, pin):

        # Validate owner name
        if not isinstance(owner_name, str) or not owner_name.strip():
            raise ValueError("Owner name must be a non-empty string.")

        # Validate PIN
        if not validate_pin_format(pin):
            raise ValueError("Invalid PIN format.")

        self.__pin_hash = hash_pin(pin)
        self.__balance = Decimal("0.00")
        self.__account_number = BankAccount._account_counter

        self.owner_name = owner_name.strip()
        self.transaction_history = []
        self.created_date = date.today()

        BankAccount._account_counter += 1

    def _verify_pin(self, pin):
        """
        Verifies the pin.
        """
        if not verify_pin(pin, self.__pin_hash):
            raise AuthenticationError("Incorrect PIN.")

    def get_balance(self, pin):
        """
        Gets the accounts balance.
        """
        self._verify_pin(pin)
        return self.__balance

    def get_account_number(self):
        """
        Gets the accounts number.
        """
        return format_account_number(str(self.__account_number))

    def _normalize_amount(self, amount):
        """
        Internal helper to safely convert and round money values.
        """
        if not isinstance(amount, (int, float, Decimal)):
            raise TypeError("Amount must be a number.")

        return Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def deposit(self, amount, pin, description=""):
        """
        Deposits into the account.
        """

        self._verify_pin(pin)

        amount = self._normalize_amount(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        self.__balance += amount
        self.__balance = self.__balance.quantize(Decimal("0.01"))

        transaction = Transaction("deposit", amount, description, self.__balance)
        self.transaction_history.append(transaction)

        return self.__balance

    def withdraw(self, amount, pin, description=""):
        """
        Withdraws from the account.
        """
        self._verify_pin(pin)

        amount = self._normalize_amount(amount)

        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        if self.__balance - amount < 0:
            raise InsufficientFundsError(self.__balance, amount)

        self.__balance -= amount
        self.__balance = self.__balance.quantize(Decimal("0.01"))

        transaction = Transaction("withdrawal", amount, description, self.__balance)
        self.transaction_history.append(transaction)

        return self.__balance

    def get_statement(self, last_n=10):
        """
        Creates a classic Bank Statement.
        """
        lines = [
            f"Statement for {self.owner_name}",
            f"Account: {self.get_account_number()}",
            f"Created: {format_date(self.created_date)}"
        ]

        for t in self.transaction_history[-last_n:]:
            lines.append(str(t))

        return "\n".join(lines)

    def __str__(self):
        return f"{self.owner_name} - {self.get_account_number()}"

    def __repr__(self):
        return f"<BankAccount {self.get_account_number()} owner={self.owner_name}>"

    def __len__(self):
        return len(self.transaction_history)

    def to_dict(self, pin):
        """
        Converts key information to a dictionary to be able to save to json file.
        """
        self._verify_pin(pin)

        return {
            "account_number": self.__account_number,
            "owner_name": self.owner_name,
            "pin_hash": self.__pin_hash,
            "balance": str(self.__balance),
            "created_date": self.created_date.isoformat(),
            "transactions": [t.to_dict() for t in self.transaction_history]
        }

    def _to_dict_internal(self):
        return {
            "account_number": self.__account_number,
            "owner_name": self.owner_name,
            "pin_hash": self.__pin_hash,
            "balance": str(self.__balance),
            "created_date": self.created_date.isoformat(),
            "transactions": [t.to_dict() for t in self.transaction_history]
        }

    @classmethod
    def from_dict(cls, data):
        """
        Loads the info from a dict (to be able to load the json format.)
        """
        obj = cls.__new__(cls)

        obj.__account_number = data["account_number"]
        obj.__pin_hash = data["pin_hash"]
        obj.__balance = Decimal(str(data["balance"])).quantize(Decimal("0.01"))
        obj.owner_name = data["owner_name"]
        obj.created_date = date.fromisoformat(data["created_date"])

        obj.transaction_history = [
            Transaction.from_dict(t) for t in data["transactions"]
        ]

        cls._account_counter = max(cls._account_counter, obj.__account_number + 1)

        return obj
