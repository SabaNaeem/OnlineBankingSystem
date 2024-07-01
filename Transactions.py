import csv
from collections import defaultdict
from datetime import datetime, timedelta


class Transactions:
    def __init__(self):
        self.transactions = []

    def read_transactions_from_file(self):
        self.transactions = []
        with open('transactions.csv', mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                transaction = [
                    row['username'],
                    datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'),
                    row['type'],
                    row['amount']
                ]
                self.transactions.append(transaction)

    def filter_user_transactions(self, username):
        user_transactions = [t for t in self.transactions if t[0] == username]
        return user_transactions

    def write_user_transactions_to_file(self, username, user_transactions):
        filename = f"{username}_transactions.csv"
        with open(filename, mode='w', newline='') as file:
            fieldnames = ['username', 'Date', 'transaction_type', 'amount']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for transaction in user_transactions:
                writer.writerow({
                    'username': transaction[0],
                    'date': transaction[1].strftime('%Y-%m-%d %H:%M:%S'),
                    'transaction_type': transaction[2],
                    'amount': transaction[3]
                })

    def print_transactions(self, user_transactions):
        for transaction in user_transactions:
            print(f"Name: {transaction[0]}, Date: {transaction[1]}, Type: {transaction[2]}, Amount: {transaction[3]}")

    def read_transactions_from_user(self, username):
        print(f"Transaction history for {username}:")
        self.read_transactions_from_file()
        user_transactions = self.filter_user_transactions(username)
        return user_transactions

    def get_transactions(self):
        self.read_transactions_from_file()
        if not self.transactions:
            print("No transactions found.")
            return False

        return self.transactions

    def filter_transactions_by_time(self, start_date, end_date):
        filtered_transactions = [
            t for t in self.transactions if start_date <= t[1] <= end_date
        ]
        return filtered_transactions

    def generate_report(self, transactions):
        report = defaultdict(lambda: {'cash_in': 0, 'cash_out': 0})
        for t in transactions:
            date_key = t[1].strftime('%Y-%m-%d')
            if t[2] in ['deposit', 'transfer from']:
                report[date_key]['cash_in'] += float(t[3])
            elif t[2] in ['withdraw', 'transfer to']:
                report[date_key]['cash_out'] += float(t[3])
        return report

    def print_report(self, report, period):
        print(f"\n{period.capitalize()} Report:")
        for date, amounts in sorted(report.items()):
            print(f"Date: {date}, Cash-In: {amounts['cash_in']}, Cash-Out: {amounts['cash_out']}")

    def generate_time_period_reports(self, period):
        self.read_transactions_from_file()
        today = datetime.now()

        # Monthly report
        if period == 'M':
            start_of_month = today.replace(day=1)
            print(f"From: {start_of_month}, To: {today}")
            transaction_list = self.filter_transactions_by_time(start_of_month, today)
            self.print_report(
                self.generate_report(transaction_list),
                "monthly"
            )
        elif period == 'W':
            # Weekly report
            start_of_week = today - timedelta(days=today.weekday())  # Monday
            print(f"From: {start_of_week}, To: {today}")
            transaction_list = self.filter_transactions_by_time(start_of_week, today)
            self.print_report(
                self.generate_report(transaction_list),
                "weekly"
            )
        # Yearly report
        elif period == 'Y':
            start_of_year = today.replace(month=1, day=1)
            print(f"From: {start_of_year}, To: {today}")
            transaction_list = self.filter_transactions_by_time(start_of_year, today)
            self.print_report(
                self.generate_report(transaction_list),
                "yearly"
            )
        else:
            print("Invalid time period.")

