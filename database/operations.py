from database.database import get_connection
from auth.security import hash_pin, verify_pin


def create_customer(name, email, phone=None):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO customers (name, email, phone)
            VALUES (?, ?, ?)
            """,
            (name, email, phone)
        )

        cursor.execute(
            "SELECT customer_id FROM customers WHERE email = ?",
            (email,)
        )
        customer_id = cursor.fetchone()[0]

        connection.commit()

        return customer_id

    finally:
        connection.close()


def create_account(
    customer_id,
    account_number,
    pin,
    initial_balance=0.0
):
    pin_hash = hash_pin(pin)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO accounts (
                customer_id,
                account_number,
                pin_hash,
                balance
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                customer_id,
                account_number,
                pin_hash,
                initial_balance
            )
        )

        cursor.execute(
            "SELECT account_id FROM accounts WHERE account_number = ?",
            (account_number,)
        )
        account_id = cursor.fetchone()[0]

        connection.commit()

        return account_id

    finally:
        connection.close()


def get_account(account_number):

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
            WHERE account_number = ?
            """,
            (account_number,)
        )

        return cursor.fetchone()

    finally:
        connection.close()


def authenticate(account_number, pin):

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

    if verify_pin(pin, pin_hash):

        reset_failed_attempts(account_id)

        return True, "Login successful."

    failed_attempts += 1

    if failed_attempts >= 3:

        lock_account(account_id)

        return False, "Account locked after 3 failed attempts."

    update_failed_attempts(
        account_id,
        failed_attempts
    )

    attempts_left = 3 - failed_attempts

    return False, (
        f"Invalid PIN. "
        f"{attempts_left} attempt(s) remaining."
    )


def update_failed_attempts(account_id, attempts):

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE accounts
            SET failed_attempts = ?
            WHERE account_id = ?
            """,
            (attempts, account_id)
        )

        connection.commit()

    finally:
        connection.close()


def reset_failed_attempts(account_id):

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE accounts
            SET failed_attempts = 0
            WHERE account_id = ?
            """,
            (account_id,)
        )

        connection.commit()

    finally:
        connection.close()


def lock_account(account_id):

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE accounts
            SET status = 'LOCKED'
            WHERE account_id = ?
            """,
            (account_id,)
        )

        connection.commit()

    finally:
        connection.close()


def update_balance(account_id, new_balance):

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (new_balance, account_id)
        )

        connection.commit()

    finally:
        connection.close()


def record_transaction(
    account_id,
    transaction_type,
    amount,
    balance_after,
    status="SUCCESS"
):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO transactions (
                account_id,
                transaction_type,
                amount,
                balance_after,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                account_id,
                transaction_type,
                amount,
                balance_after,
                status
            )
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def get_transactions(account_id):

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                transaction_id,
                transaction_type,
                amount,
                balance_after,
                status,
                timestamp
            FROM transactions
            WHERE account_id = ?
            ORDER BY timestamp DESC
            """,
            (account_id,)
        )

        return cursor.fetchall()

    finally:
        connection.close()


def initialize_atm_cash():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        denominations = [
            (500, 20),
            (200, 20),
            (100, 20)
        ]

        cursor.executemany(
            """
            INSERT OR IGNORE INTO atm_cash
            (denomination, quantity)
            VALUES (?, ?)
            """,
            denominations
        )

        connection.commit()

    finally:
        connection.close()


def get_atm_cash():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT denomination, quantity
            FROM atm_cash
            ORDER BY denomination DESC
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()


def update_atm_cash(denomination, quantity):

    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE atm_cash
            SET quantity = ?
            WHERE denomination = ?
            """,
            (quantity, denomination)
        )

        connection.commit()

    finally:
        connection.close()

def get_customer_by_email(email):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                customer_id,
                name,
                email,
                phone
            FROM customers
            WHERE email = ?
            """,
            (email,)
        )

        return cursor.fetchone()

    finally:

        connection.close()

def get_account_by_number(account_number):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM accounts
            WHERE account_number = ?
            """,
            (account_number,)
        )

        return cursor.fetchone()

    finally:

        connection.close()

def update_pin(account_id, new_pin_hash):

    connection = get_connection()

    try:

        connection.execute(
            """
            UPDATE accounts
            SET pin_hash = ?,
                failed_attempts = 0,
                status = 'ACTIVE'
            WHERE account_id = ?
            """,
            (new_pin_hash, account_id)
        )

        connection.commit()

    finally:

        connection.close()

def unlock_account(account_number):

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET status = 'ACTIVE',
                failed_attempts = 0
            WHERE account_number = ?
            """,
            (account_number,)
        )

        connection.commit()

        return cursor.rowcount > 0

    finally:
        connection.close()