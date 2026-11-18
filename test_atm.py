from banking.atm import ATM


def main():

    atm = ATM({
        500: 10,
        200: 10,
        100: 10
    })

    print("ATM Cash:")
    print(atm.cash_inventory)

    print("\nTotal cash:")
    print(f"₹{atm.total_cash():,.2f}")

    print("\nRequesting ₹2,700...")

    notes = atm.dispense_cash(250)
    print("\nCash dispensed:")

    for denomination, quantity in notes.items():

        print(
            f"₹{denomination} × {quantity}"
        )

    print("\nRemaining cash:")

    for denomination, quantity in atm.cash_inventory.items():

        print(
            f"₹{denomination}: {quantity} notes"
        )


if __name__ == "__main__":
    main()