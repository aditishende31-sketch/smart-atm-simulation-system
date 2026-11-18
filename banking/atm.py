class ATM:

    def __init__(self, cash_inventory=None):

        if cash_inventory is None:
            cash_inventory = {
                500: 0,
                200: 0,
                100: 0
            }

        self.cash_inventory = cash_inventory

    def load_cash(self, denomination, quantity):

        if denomination not in self.cash_inventory:
            raise ValueError(
                "Unsupported denomination."
            )

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        self.cash_inventory[denomination] += quantity

    def total_cash(self):

        return sum(
            denomination * quantity
            for denomination, quantity
            in self.cash_inventory.items()
        )

    def calculate_notes(self, amount):

        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )

        remaining = amount
        notes = {}

        for denomination in sorted(
            self.cash_inventory.keys(),
            reverse=True
        ):

            available = self.cash_inventory[denomination]

            required = remaining // denomination

            use = min(required, available)

            if use > 0:

                notes[denomination] = use

                remaining -= (
                    denomination * use
                )

        if remaining != 0:

            raise ValueError(
                "ATM cannot dispense the requested amount "
                "with available denominations."
            )

        return notes

    def dispense_cash(self, amount):

        notes = self.calculate_notes(amount)

        for denomination, quantity in notes.items():

            self.cash_inventory[denomination] -= quantity

        return notes