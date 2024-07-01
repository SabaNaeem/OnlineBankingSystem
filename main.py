import getpass
import bcrypt
import warnings
from User import User
from admin import Admin

# from admin import Admin
1
def main():
    print("Welcome to the Account Management System")

    while True:
        role = input("Are you a (1) User or (2) Admin? (3 to Quit): ")

        if role == '1':
            username = input("Enter username: ")
            pin = input("Enter password: ")
            user = User(username, pin)
            if user.is_authenticated(username, pin):
                print(f"Welcome {username}")
                while True:
                    action = input(
                        "1. Deposit\n2. Check Balance\n3. Print Statement\n4. Withdraw\n5. Transfer\n"
                        "6. Set/Change PIN\n7. View Transaction History\n8. Logout\nChoose an action: ")

                    if action == '1':
                        amount = float(input("Enter amount to deposit: "))
                        user.deposit(amount)
                    elif action == '2':
                        print(f"Balance: {user.check_balance()}")
                    elif action == '3':
                        user.print_statement()
                        print("Statement is printed to the new file")
                    elif action == '4':
                        amount = float(input("Enter amount to withdraw: "))
                        user.withdraw(amount)
                    elif action == '5':
                        to_username = input("Enter recipient username: ")
                        amount = float(input("Enter amount to transfer: "))
                        user.transfer(to_username, amount)
                    elif action == '6':
                        new_pin = input("Enter new PIN: ")
                        user.set_pin(new_pin)
                    elif action == '7':
                        user.transaction_history()
                    elif action == '8':
                        break
                    else:
                        print("Invalid action.")
            else:
                print("Authentication failed.")

        elif role == '2':
            admin = Admin()
            print("Admin Mode")
            while True:
                action = input(
                    "1. Create Account\n2. Show Details\n3. Show Transactions\n4. Delete Account\n"
                    "5. Freeze Account\n6. Set Transaction Limit\n7. Generate Daily/monthly/weekly report\n8. Logout\nChoose an action: ")

                if action == '1':
                    username = input("Enter username: ")
                    warnings.filterwarnings("ignore", category=getpass.GetPassWarning)
                    pin = input("Enter password: ")
                    if admin.create_user(username, bcrypt.hashpw(pin.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')):
                        print("Account created.")
                    else:
                        print("Account creation failed. Username may already exist.")
                elif action == '2':
                    username = input("Enter username: ")
                    admin.show_details(username)
                elif action == '3':
                    username = input("Enter username (Press A for all transactions): ")
                    admin.show_transactions(username)
                elif action == '4':
                    username = input("Enter username: ")
                    if admin.delete_account(username):
                        print("Account deleted.")
                    else:
                        print("Account deletion failed.")
                elif action == '5':
                    username = input("Enter username: ")
                    admin.freeze_account(username)
                elif action == '6':
                    username = input("Enter username: ")
                    limit = float(input("Enter new transaction limit: "))
                    admin.set_transaction_limit(username, limit)
                elif action == '7':
                    period = input("Enter period - W/M/Y: ")
                    admin.generate_reports(period)
                elif action == '8':
                    break
                else:
                    print("Invalid action.")

        elif role == '3':
            print("Thank you for using the system built by SABA NAEEM")
            break


if __name__ == '__main__':
    main()
