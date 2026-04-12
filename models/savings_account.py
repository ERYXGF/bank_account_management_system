from decimal import Decimal
from models.account import BankAccount
from exceptions import MinimumBalanceError


class SavingsAccount(BankAccount):
    """
    Contains the SavingsAccount class inheriting from the 
    BankAccount class.
    """
    def __init__(self, owner_name, pin, interest_rate=0.03, minimum_balance=100.0):
        super().__init__(owner_name, pin)
        self.interest_rate = Decimal(str(interest_rate))
        self.minimum_balance = Decimal(str(minimum_balance))

    def withdraw(self, amount, pin, description=""):
        """
        Withdraws from the account.
        """
        self._verify_pin(pin)

        balance = self.get_balance(pin)
        amount = Decimal(str(amount))

        if balance - amount < self.minimum_balance:
            raise MinimumBalanceError(self.minimum_balance, balance)

        return super().withdraw(amount, pin, description)

    def apply_interest(self, pin):
        """
        Applies interest.
        """
        self._verify_pin(pin)

        balance = self.get_balance(pin)
        interest = balance * self.interest_rate

        return self.deposit(interest, pin, "Monthly interest")

    def calculate_projected_balance(self, months, pin):
        """
        Calculates the accounts projected balance.
        """
        self._verify_pin(pin)

        balance = self.get_balance(pin)
        return balance * (Decimal("1") + self.interest_rate) ** months

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Interest rate: {self.interest_rate} | "
            f"Min balance: {self.minimum_balance}"
        )
