class Account:

    def __init__(
        self,
        account_id,
        customer_id,
        account_number,
        balance=0.0,
        status="ACTIVE"
    ):
        self.account_id = account_id
        self.customer_id = customer_id
        self.account_number = account_number
        self.balance = float(balance)
        self.status = status

    def check_balance(self):
        return self.balance

    def deposit(self, amount):

        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")

        self.balance += amount

        return self.balance

    def withdraw(self, amount):

        if amount <= 0:
            raise ValueError(
                "Withdrawal amount must be greater than zero."
            )

        if amount > self.balance:
            raise ValueError("Insufficient account balance.")

        self.balance -= amount

        return self.balance