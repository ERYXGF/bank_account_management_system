from decimal import Decimal
from models.account import BankAccount
from exceptions import OverdraftLimitError

class CurrentAccount(BankAccount):
    """
    CurrentAccount class that inherits from the BankAccount class.
    """
    def __init__(self, owner_name, pin, overdraft_limit=500.0, overdraft_fee=15.0):
        super().__init__(owner_name, pin)
        self.overdraft_limit = Decimal(str(overdraft_limit))
        self.overdraft_fee = Decimal(str(overdraft_fee))

    def withdraw(self, amount, pin, description=""):
        self._verify_pin(pin)

        balance = self.get_balance(pin)
        amount = Decimal(str(amount))

        if balance - amount < -self.overdraft_limit:
            raise OverdraftLimitError(self.overdraft_limit, amount)

        new_balance = super().withdraw(amount, pin, description)

        if new_balance < 0:
            super().withdraw(self.overdraft_fee, pin, "Overdraft fee")
            return self.get_balance(pin)

        return new_balance

    def direct_debit(self, amount, payee, pin):
        """
        Creates a direct debit.
        """
        self._verify_pin(pin)
        return self.withdraw(amount, pin, f"Direct debit to {payee}")

    def __str__(self):
        return (
            f"{super().__str__()} | "
            f"Overdraft limit: {self.overdraft_limit} | "
            f"Fee: {self.overdraft_fee}"
        )
