# 🏦 Bank Account System (Python)

A fully object-oriented bank account simulation built in Python.
This project demonstrates secure PIN handling, transaction tracking, multiple account types, and persistent data storage using JSON.

---

## 🚀 Features

* 🔐 Secure PIN system using SHA-256 hashing
* 💰 Deposit, withdraw, and transfer money
* 🏦 Multiple account types:

  * Savings Account (with interest + minimum balance)
  * Current Account (with overdraft + fees)
* 📄 Transaction history with formatted statements
* 💾 Persistent storage using JSON
* ⚠️ Custom exception handling for realistic banking errors
* 🧠 Fully object-oriented design

---

## 📂 Project Structure

```
bank-account-system/
├── main.py
├── models/
│   ├── __init__.py
│   ├── transaction.py
│   ├── account.py
│   ├── savings_account.py
│   ├── current_account.py
│   └── bank.py
├── exceptions.py
├── security.py
├── utils.py
├── data/
│   └── bank.json
├── .gitignore
├── README.md
└── LICENSE
```

---

## 🧱 Architecture Overview

### 🔹 Core Components

| File                      | Role                         |
| ------------------------- | ---------------------------- |
| exceptions.py             | Custom banking errors        |
| security.py               | PIN hashing and verification |
| utils.py                  | Formatting helpers           |
| models/transaction.py     | Transaction model            |
| models/account.py         | Base account class           |
| models/savings_account.py | Savings account logic        |
| models/current_account.py | Current account logic        |
| models/bank.py            | Central bank manager         |
| main.py                   | CLI interface                |

---

## 🔐 Security

* PINs are never stored in plain text
* Uses hashlib.sha256 for hashing
* All sensitive actions require PIN verification

---

## 💡 Account Types

### 🟢 Savings Account

* Interest rate (default: 3%)
* Minimum balance requirement
* Monthly interest application

### 🔵 Current Account

* Overdraft limit (default: €500)
* Automatic overdraft fee
* Direct debit support

---

## ⚙️ How to Run

1. Clone the repo:

```
git clone https://github.com/yourusername/bank-account-system.git
cd bank-account-system
```

2. Run the program:

```
python main.py
```

---

## 🖥️ CLI Menu

```
1. Create savings account
2. Create current account
3. Deposit
4. Withdraw
5. Transfer
6. Check balance
7. View statement
8. Apply monthly interest
9. View total assets
0. Quit
```

---

## 💾 Data Persistence

* All data is stored in:

```
data/bank.json
```

* Automatically:

  * Loaded on startup
  * Saved after every operation

---

## ⚠️ Error Handling

The system includes custom exceptions:

* AuthenticationError
* InsufficientFundsError
* MinimumBalanceError
* OverdraftLimitError

All errors are handled gracefully — no crashes.

---

## 🧠 Concepts Demonstrated

* Object-Oriented Programming (OOP)
* Inheritance and polymorphism
* Encapsulation (private/protected attributes)
* Data serialization (JSON)
* Exception handling
* Secure programming practices

---

## 📈 Possible Improvements

* GUI interface (Tkinter / Web app)
* User login system
* Multi-user authentication
* Transaction search/filtering
* Currency conversion
* Database integration (SQLite/PostgreSQL)

---

## 👨‍💻 Author

Built as a learning project to master Python OOP and system design.

---

## 📜 License

This project is licensed under the MIT License.

