"""
Contains pin hashing and verification using hashlib (built-in module). Account.py depends on it.
"""
#Imports the hashlib module:
import hashlib

def hash_pin(pin):
    """
    Takes a PIN as a string or integer, converts to string, encodes to bytes and returns a SHA-256 hash as a hex string. 
    This is what gets stored in JSON instead of the raw PIN.
    """
    #Converts the pin to a string:
    pin = str(pin)
    #Encodes pin to a bytes format:
    pin_bytes = pin.encode()
    #Converts to a 256 hash and returns hex string:
    hashed_pin = hashlib.sha256(pin_bytes).hexdigest()
    #Returns the hashed pin:
    return hashed_pin

def verify_pin(entered_pin, stored_hash):
    """
    Takes the PIN the user just typed and the hash stored on the account. 
    Hashes the entered PIN using the same method and compares the two hashes. 
    Returns True if they match, False otherwise. 
    Never compare raw PINs — always compare hashes.
    """
    #Converts the entered pin to a hash:
    entered_hash = hashlib.sha256(str(entered_pin).encode()).hexdigest()
    #Compares the entered_hash to the stored one:
    return entered_hash == stored_hash

def validate_pin_format(pin):
    """
    takes a raw PIN input and validates it is exactly 4 digits, all numeric. 
    Returns True or False. Used in account creation before hashing.
    """
    #Converts the pin to a string:
    pin = str(pin)
    #Checks that it contains exacly 4 digits:
    return pin.isdigit() and len(pin) == 4
