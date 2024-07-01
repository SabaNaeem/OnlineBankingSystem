import csv
import sys
import bcrypt
from datetime import datetime
from Transactions import Transactions

class User:
    def __init__(self, username, pin, freeze=False, balance=0, limit=sys.maxsize):
        self.username = username
        self.pin = pin
        self.freeze = freeze
        self.balance = balance
        self.limit = limit

    def deposit(self, amount):
        if not self.check_Freeze():
            if amount <= 0:
                print("Deposit amount must be greater than zero.")
                return False
            if self.check_Limit() <= amount:
                print("Transaction Limit exceeded")
                return False

            self.balance = float(self.check_balance())
            self.balance += amount
            self.__add_transaction(self.username, "deposit", amount)
            self.__update_account_data()
            print(f"Successfully deposited ${amount}. Current balance: ${self.balance}")
            return True
        else:
            print("Account is freezed.")

    def withdraw(self, amount):
        if self.check_Freeze() == False:
            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
                return False

            self.balance = float(self.check_balance())
            if amount > self.balance:
                print("Insufficient funds.")
                return False

            if self.check_Limit() <= amount:
                print("Transaction Limit exceeded")
                return False

            self.balance -= amount
            self.__add_transaction(self.username, "withdraw", amount)
            self.__update_account_data()
            print(f"Withdrawal of ${amount} successful. Current balance: ${self.balance}")
            return True
        else:
            print("Account is freezed.")

    def transfer(self, recipient_user, amount):
        if not self.check_Freeze():
            if amount <= 0:
                print("Transfer amount must be greater than zero.")
                return False

            self.balance = float(self.check_balance())
            if amount > self.balance:
                print("Insufficient funds.")
                return False

            if self.check_Limit() <= amount:
                print("Transaction Limit exceeded")
                return False

            recipient = self.__get_user(recipient_user)
            if not recipient:
                print(f"Recipient '{recipient_user}' not found.")
                return False

            if recipient.check_Freeze() == False:
                if recipient.check_Limit() <= amount:
                    print("Transaction Limit of recipient exceeded")
                    return False
                self.balance -= amount
                self.__add_transaction(self.username, f"transfer to {recipient_user}", amount)
                recipient.balance += amount
                recipient.__add_transaction(recipient_user, f"transfer from {self.username}", amount)
                self.__update_account_data()
                recipient.__update_account_data()

                print(f"Transfer of ${amount} to {recipient_user} successful. Current balance: ${self.balance}")
                return True
            else:
                print("Recipient account is freeze.")
        else:
            print("Account is freeze.")

    def check_balance(self):
        try:
            with open('user_data.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == self.username:
                        self.balance = float(row['balance'])
                        return self.balance
            return self.balance
        except FileNotFoundError:
            print("User data file not found.")
            return False

    def check_Freeze(self):
        try:
            with open('user_data.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == self.username:
                        status = str(row['freeze'])
                        if status == "True":
                            self.freeze = True
                        break
            return self.freeze
        except FileNotFoundError:
            print("User data file not found.")
            return False

    def check_Limit(self):
        try:
            with open('user_data.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == self.username:
                        self.limit = float(row['limit'])
                        return self.limit
            return self.limit
        except FileNotFoundError:
            print("User data file not found.")
            return False

    def __add_transaction(self, user, transaction_type, amount):
        with open('transactions.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), transaction_type, amount])

        return True

    def __update_account_data(self):
        # Update account data in CSV file
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            accounts = list(reader)

        for account in accounts:
            if account['username'] == self.username:
                account['balance'] = str(self.balance)

        with open('user_data.csv', mode='w', newline='') as file:
            fieldnames = ['username', 'pin', 'freeze', 'balance', 'limit']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)

    def is_authenticated(self, username, pin):
        found = False
        try:
            with open('user_data.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        found = True
                        stored_pin = row['pin']
                        if bcrypt.checkpw(pin.encode('utf-8'), stored_pin.encode('utf-8')):
                            return True
                        else:
                            print("Incorrect pin")
                if not found:
                    print("User not found")
            return False
        except FileNotFoundError:
            print("User data file not found.")
            return False

    def set_pin(self, new_pin):
        self.pin = bcrypt.hashpw(new_pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            accounts = list(reader)

        for account in accounts:
            if account['username'] == self.username:
                account['pin'] = str(self.pin)
                print("Successfully updated pin.")

        with open('user_data.csv', mode='w', newline='') as file:
            fieldnames = ['username', 'pin', 'freeze', 'balance', 'limit']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)

    def __get_user(self, username):
        try:
            with open('user_data.csv', mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        user = User(row['username'], row['pin'], float(row['balance']))
                        return user
        except FileNotFoundError:
            print("User data file not found.")
        return None

    def print_statement(self):
        t = Transactions()
        user_transactions = t.read_transactions_from_user(self.username)
        if user_transactions:
            t.write_user_transactions_to_file(self.username, user_transactions)
            print(f"Transactions for {self.username} have been written to {self.username}_transactions.csv")
        else:
            print(f"No transactions found for user {self.username}")

    def transaction_history(self):
        t = Transactions()
        user_transactions = t.read_transactions_from_user(self.username)
        if user_transactions:
            t.print_transactions(user_transactions)
        else:
            print(f"No transactions found for user {self.username}")



