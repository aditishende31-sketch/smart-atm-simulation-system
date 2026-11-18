from auth.session import Session


def main():

    session = Session(
        account_id=1,
        account_number="100001",
        timeout_minutes=5
    )

    print("Session active:")
    print(session.is_active())

    print("\nUpdating activity...")

    session.update_activity()

    print(
        "Session active:",
        session.is_active()
    )

    print("\nLogging out...")

    session.logout()

    print(
        "Session active:",
        session.is_active()
    )


if __name__ == "__main__":
    main()