from auth.authentication import AuthenticationService
from auth.session import Session


def main():

    auth = AuthenticationService()

    print("=" * 45)
    print("       AUTHENTICATION TEST")
    print("=" * 45)

    account_number = input(
        "\nEnter account number: "
    )

    pin = input(
        "Enter PIN: "
    )

    success, result = auth.login(
        account_number,
        pin
    )

    if not success:
        print(result)
        return

    print(result["message"])

    session = Session(
        result["account_id"],
        result["account_number"]
    )

    print("\nSession created.")

    print(
        "Account:",
        session.account_number
    )

    print(
        "Session active:",
        session.is_active()
    )


if __name__ == "__main__":
    main()