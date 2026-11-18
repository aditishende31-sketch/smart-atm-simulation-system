from database.operations import unlock_account


account_number = input(
    "Enter account number to unlock: "
)

if unlock_account(account_number):

    print("Account unlocked successfully.")

else:

    print("Account not found.")