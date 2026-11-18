from auth.authentication import AuthenticationService


auth = AuthenticationService()


account_number = input(
    "Enter account number: "
)

current_pin = input(
    "Enter current PIN: "
)

success, result = auth.login(
    account_number,
    current_pin
)

if not success:

    print(result)

else:

    account_id = result["account_id"]

    new_pin = input(
        "Enter new 4-digit PIN: "
    )

    confirm_pin = input(
        "Confirm new PIN: "
    )

    success, message = auth.change_pin(
        account_id,
        current_pin,
        new_pin,
        confirm_pin
    )

    print(message)