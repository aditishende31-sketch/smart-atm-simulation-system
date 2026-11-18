
from database.operations import create_customer, create_account, get_account

# Details for a test customer
name = "ATM Test User"
email = "atmtest@example.com"
phone = "9999999999"

# Create customer
customer_id = create_customer(name, email, phone)

# Create a separate test account
account_number = "200001"

from getpass import getpass

pin = getpass("Enter a test PIN: ")

initial_balance = 5000

existing_account = get_account(account_number)

if existing_account:
    print("Test account already exists.")
    print("Account Number:", account_number)
else:
    account_id = create_account(
        customer_id=customer_id,
        account_number=account_number,
        pin=pin,
        initial_balance=initial_balance
    )

    print("Test account created successfully!")
    print("Account Number:", account_number)
    print("Test PIN:", pin)
    print("Initial Balance: ₹", initial_balance)
