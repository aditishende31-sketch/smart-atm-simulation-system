from database.operations import (
    get_account,
    reset_failed_attempts,
    update_failed_attempts,
    lock_account,
    update_pin
)

from database.database import get_connection
from auth.security import verify_pin, hash_pin


MAX_ATTEMPTS = 3


class AuthenticationService:

    def login(self, account_number, pin):

        if not account_number:
            return False, "Account number is required."

        if not pin:
            return False, "PIN is required."

        account = get_account(account_number)

        if account is None:
            return False, "Account not found."

        (
            account_id,
            customer_id,
            account_number,
            pin_hash,
            balance,
            status,
            failed_attempts
        ) = account

        if status == "LOCKED":
            return False, "Account is locked."

        if status != "ACTIVE":
            return False, "Account is not active."

        if verify_pin(pin, pin_hash):

            reset_failed_attempts(account_id)

            return True, {
                "message": "Login successful.",
                "account_id": account_id,
                "customer_id": customer_id,
                "account_number": account_number
            }

        failed_attempts += 1

        if failed_attempts >= MAX_ATTEMPTS:

            lock_account(account_id)

            return False, (
                "Account locked after 3 failed attempts."
            )

        update_failed_attempts(
            account_id,
            failed_attempts
        )

        attempts_left = (
            MAX_ATTEMPTS - failed_attempts
        )

        return False, (
            f"Invalid PIN. "
            f"{attempts_left} attempt(s) remaining."
        )

    def change_pin(
        self,
        account_id,
        current_pin,
        new_pin,
        confirm_pin
    ):

        account = self.get_account_by_id(account_id)

        if account is None:
            return False, "Account not found."

        pin_hash = account[3]

        if not verify_pin(current_pin, pin_hash):
            return False, "Current PIN is incorrect."

        if new_pin != confirm_pin:
            return False, "New PINs do not match."

        if not new_pin.isdigit():
            return False, "PIN must contain only digits."

        if len(new_pin) != 4:
            return False, "PIN must be exactly 4 digits."

        if new_pin == current_pin:
            return False, (
                "New PIN must be different "
                "from current PIN."
            )

        new_hash = hash_pin(new_pin)

        update_pin(
            account_id,
            new_hash
        )

        return True, "PIN changed successfully."

    def get_account_by_id(self, account_id):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    account_id,
                    customer_id,
                    account_number,
                    pin_hash,
                    balance,
                    status,
                    failed_attempts
                FROM accounts
                WHERE account_id = ?
                """,
                (account_id,)
            )

            return cursor.fetchone()

        finally:
            connection.close()