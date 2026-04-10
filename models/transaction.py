"""
The Transaction class. No dependencies on other models. Built third.
"""
#Imports datetime:
from datetime import datetime

#Imports format_statement_line:
from utils import format_statement_line

class Transaction:
    """
    Represents a single bank transaction
    """
    _id_counter = 1

    def __init__(self, transaction_type, amount, description, balance_after):

        #Simple attributes:
        self.transaction_type = transaction_type
        self.amount = float(amount)
        self.description = description
        self.balance_after = float(balance_after)

        #Assigns the transaction_id:
        self.transaction_id = Transaction._id_counter
        Transaction._id_counter += 1

        #Assigns the timestamp:
        self.timestamp = datetime.now()

    def __str__(self):
        """
        Human readable expression
        """
        return format_statement_line(self)
    
    def __repr__(self):
        """
        Developer/debug representation
        """
        return f"<Transaction id={self.transaction_id} type={self.transaction_type}>"

    def to_dict(self):
        """
        Convert transaction to dictionary for JSON storage
        """
        return {
            "transaction_id": self.transaction_id,
            "transaction_type": self.transaction_type,
            "amount": self.amount,
            "description": self.description,
            "balance_after": self.balance_after,
            "timestamp": self.timestamp.isoformat()
        }
  
    @classmethod
    def from_dict(cls, data):
        """
        Reconstruct a Transaction object from dictionary
        """
        obj = cls(
            data["transaction_type"],
            data["amount"],
            data["description"],
            data["balance_after"]
        )

        obj.transaction_id = data["transaction_id"]
        obj.timestamp = datetime.fromisoformat(data["timestamp"])

        cls._id_counter = max(cls._id_counter, obj.transaction_id + 1)

        return obj
