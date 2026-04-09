"""
Formatting helpers for currency, dates and bank statement output. 
No dependencies on other project files.
"""

def format_currency(amount):
    """
    Takes a float and returns a string formatted as currency with two decimal places and a € symbol. 
    Handles negative amounts correctly for overdraft display.
    """
    return f"{amount:.2f}€"


def format_date(dt):
    """
    Takes a datetime object and returns a clean readable string like "20 March 2025 at 14:32".
    """
    return dt.strftime("%d %B %Y at %H:%M")


def format_account_number(account_number):
    """
    Takes the full account number string and returns a masked version showing only the last 4 digits 
    for security display, like "****7842".
    """
    account_number = str(account_number)
    return "*" * (len(account_number) - 4) + account_number[-4:]


def format_statement_line(transaction):
    """
    Takes a Transaction object and returns a single formatted line suitable for printing in a bank 
    statement. Fixed-width columns for date, type, amount and balance.
    """

    # Format individual components
    date_str = format_date(transaction.timestamp)
    type_str = transaction.transaction_type

    # Determine sign for amount
    if transaction.transaction_type in ["deposit", "transfer_in", "interest"]:
        sign = "+"
    else:
        sign = "-"

    amount_str = f"{sign}{format_currency(transaction.amount)}"
    balance_str = format_currency(transaction.balance_after)

    # Fixed-width formatting
    return f"{date_str:<25} | {type_str:<12} | {amount_str:>12} | {balance_str:>12}"
