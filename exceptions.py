"""
Contains all four custom exception classes all inheriting from Exception. Each one should have a custom __init__ that stores a message and passes it to super().__init__(), and a __str__ that returns that message clearly..
"""
class AuthenticationError(Exception):
    """
    Raised when a PIN is wrong. Message should include how many attempts remain if you implement attempt limiting.
    """
    def __init__(self, attempts_remaining = None):
        #Checks if the user has any attempts remaining:
        if attempts_remaining is not None:
            self.message = f"Incorrect PIN. Attempts left: {attempts_remaining}"
        #If the user has no attempts remaining:
        else:
            self.message = "Incorrect PIN"
        #Passes it to super init:
        super().__init__(self.message)

    def __str__(self):
        return self.message

class InsufficientFundsError(Exception):
    """
    Raised when a withdrawal would take balance below zero (or below minimum for savings). Message should include the current balance and the amount attempted.
    """
    def __init__(self, balance, amount):
        #Defines the balance and amount:
        self.balance = balance
        self.amount = amount
        #Defines the message:
        self.message = (
            f"Insufficient funds. Current balance is: {balance:.2f}€\n"
            f"Attempted withdrawal: {amount:.2f}€"
        )
        #Passes it to super init:
        super().__init__(self.message)

    def __str__(self):
        return self.message

class MinimumBalanceError(Exception):
    """
    Raised specifically for savings accounts when a withdrawal would breach the minimum balance threshold. Message should include the minimum balance required and the current balance.
    """
    def __init__(self, minimum_balance, current_balance):
        #Defines min_balance and balance:
        self.min_balance = minimum_balance
        self.balance = current_balance
        #Defines the message:
        self.message = (
            f"Not enough money sent. Minimum balance required: {minimum_balance:.2f}€\n"
            f"Current balance: {current_balance:.2f}€"
        )
        #Passes it to super init:
        super().__init__(self.message)
    
    def __str__(self):
        return self.message

class OverdraftLimitError(Exception):
    """
    Raised when a current account withdrawal would exceed the overdraft limit. Message should include the limit and how much was attempted.
    """
    def __init__(self, limit, attempted_amount):
        #Defines limit and attempted_amount:
        self.limit = limit
        self.attempted_amount = attempted_amount
        #Defines the message:
        self.message = (
            f"Overdraft limit exceeded: limit: {limit:.2f}€\n"
            f"Attempted withdrawal: {attempted_amount:.2f}€"
        )
        #Passes it to super init
        super().__init__(self.message)

    def __str__(self):
        return self.message
