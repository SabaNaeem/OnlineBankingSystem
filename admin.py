import csv
import bcrypt
import sys
from datetime import datetime
from Transactions import Transactions

from User import User


class Admin:
    def __init__(self):
        self.users = self.__load_users()

    def create_user(self, username, pin, initial_balance=0):
        if self.__find_user(username):
            print(f"Username '{username}' already exists. Please choose a different username.")
            return False

        new_user = User(username, pin, False, initial_balance)

        with open('user_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([new_user.username, new_user.pin, new_user.freeze, new_user.balance, new_user.limit])

        print(f"Account for '{username}' created successfully with initial balance ${initial_balance}.")
        self.users.append(username)
        return True

    def show_details(self, username):
        user_details = self.__get_user_details(username)
        if user_details:
            print(f"Username: {user_details['username']}, Balance: ${user_details['balance']}, Freeze: {user_details['freeze']}, Limit: {user_details['limit']}")
        else:
            print(f"User '{username}' not found.")

    def show_transactions(self, username):
        t = Transactions()
        if username == 'A':
            all_transactions = t.get_transactions()
            if all_transactions:
                t.print_transactions(all_transactions)
            else:
                print(f"No transactions found")
        else:
            user_transactions = t.read_transactions_from_user(username)
            if user_transactions:
                t.print_transactions(user_transactions)
            else:
                print(f"No transactions found for user {username}")

    def delete_account(self, username):
        if not self.__find_user(username):
            print(f"User '{username}' not found.")
            return False

        users = []
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] != username:
                    users.append(row)

        with open('user_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(users)

        print(f"Account for '{username}' deleted successfully.")
        self.users.remove(username)
        return True

    def freeze_account(self, username):
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            accounts = list(reader)

        for account in accounts:
            if account['username'] == username:
                account['freeze'] = True
                print("Account freezed successfully.")

        with open('user_data.csv', mode='w', newline='') as file:
            fieldnames = ['username', 'pin', 'freeze', 'balance', 'limit']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)

    def set_transaction_limit(self, username, limit):
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            accounts = list(reader)

        for account in accounts:
            if account['username'] == username:
                account['limit'] = limit
                print("Account limit updated successfully.")

        with open('user_data.csv', mode='w', newline='') as file:
            fieldnames = ['username', 'pin', 'freeze', 'balance', 'limit']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)

    def generate_reports(self, period):
        transaction_manager = Transactions()
        transaction_manager.generate_time_period_reports(period)

    def __load_users(self):
        users = []
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                users.append(row[0])
        return users

    def __find_user(self, username):
        return username in self.users

    def __get_user_details(self, username):
        with open('user_data.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    return {'username': row['username'], 'balance': row['balance'], 'freeze': row['freeze'], 'limit': row['limit']}
        return None

    def __get_user_transactions(self, username):
        transactions = []
        with open('transactions.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username:
                    transactions.append(row)
        return transactions

