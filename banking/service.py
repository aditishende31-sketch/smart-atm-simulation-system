from database.database import get_connection
from auth.session import require_admin_session
from database.operations import get_atm_cash, update_atm_cash

def deposit(account_id, amount):

    if amount <= 0:
        raise ValueError(
            "Deposit amount must be greater than zero."
        )

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id = ?
            """,
            (account_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Account not found.")

        current_balance = result[0]
        new_balance = current_balance + amount

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (new_balance, account_id)
        )

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
                "DEPOSIT",
                amount,
                new_balance,
                "SUCCESS"
            )
        )

        transaction_id = cursor.lastrowid

        connection.commit()

        return transaction_id, new_balance

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()



def withdraw(account_id, amount):

    if amount <= 0:
        raise ValueError(
            "Withdrawal amount must be greater than zero."
        )

    if not isinstance(amount, int):
        raise ValueError("Withdrawal amount must be a whole number.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # STEP 1: Check customer account balance
        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id = ?
            """,
            (account_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise ValueError("Account not found.")

        current_balance = result[0]

        if amount > current_balance:
            raise ValueError("Insufficient account balance.")

        # STEP 2: Check available ATM notes
        cursor.execute(
            """
            SELECT denomination, quantity
            FROM atm_cash
            ORDER BY denomination DESC
            """
        )

        cash_details = cursor.fetchall()

        remaining_amount = amount
        note_distribution = {}

        for denomination, quantity in cash_details:

            notes_needed = min(
                remaining_amount // denomination,
                quantity
            )

            note_distribution[denomination] = notes_needed

            remaining_amount -= denomination * notes_needed

        if remaining_amount != 0:
            raise ValueError(
                "ATM does not have the required notes for this amount."
            )

        # STEP 3: Deduct ATM notes
        for denomination, notes_used in note_distribution.items():

            if notes_used > 0:

                cursor.execute(
                    """
                    UPDATE atm_cash
                    SET quantity = quantity - ?
                    WHERE denomination = ?
                    AND quantity >= ?
                    """,
                    (notes_used, denomination, notes_used)
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        "ATM cash inventory changed. Please try again."
                    )

        # STEP 4: Update customer balance
        new_balance = current_balance - amount

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (new_balance, account_id)
        )

        # STEP 5: Record transaction
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
                "WITHDRAWAL",
                amount,
                new_balance,
                "SUCCESS"
            )
        )

        transaction_id = cursor.lastrowid

        connection.commit()

        return transaction_id, new_balance

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()

def transfer(
    sender_account_id,
    receiver_account_id,
    amount
):

    if amount <= 0:
        raise ValueError(
            "Transfer amount must be greater than zero."
        )

    if sender_account_id == receiver_account_id:
        raise ValueError(
            "Sender and receiver cannot be the same account."
        )

    connection = get_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id = ?
            """,
            (sender_account_id,)
        )

        sender = cursor.fetchone()

        if sender is None:
            raise ValueError(
                "Sender account not found."
            )

        sender_balance = sender[0]

        if amount > sender_balance:
            raise ValueError(
                "Insufficient balance."
            )

        cursor.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_id = ?
            """,
            (receiver_account_id,)
        )

        receiver = cursor.fetchone()

        if receiver is None:
            raise ValueError(
                "Receiver account not found."
            )

        receiver_balance = receiver[0]

        new_sender_balance = (
            sender_balance - amount
        )

        new_receiver_balance = (
            receiver_balance + amount
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (
                new_sender_balance,
                sender_account_id
            )
        )

        cursor.execute(
            """
            UPDATE accounts
            SET balance = ?
            WHERE account_id = ?
            """,
            (
                new_receiver_balance,
                receiver_account_id
            )
        )

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
                sender_account_id,
                "TRANSFER_SENT",
                amount,
                new_sender_balance,
                "SUCCESS"
            )
        )

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
                receiver_account_id,
                "TRANSFER_RECEIVED",
                amount,
                new_receiver_balance,
                "SUCCESS"
            )
        )

        connection.commit()

        return (
            new_sender_balance,
            new_receiver_balance
        )

    except Exception:

        connection.rollback()

        raise

    finally:

        connection.close()


def change_pin(account_number, current_pin, new_pin):
    from database.operations import get_account, update_pin
    from auth.security import verify_pin, hash_pin

    account = get_account(account_number)

    if account is None:
        return False, "Account not found."

    account_id = account[0]
    stored_pin_hash = account[3]
    status = account[5]

    if status != "ACTIVE":
        return False, "Your account is not active."

    if not verify_pin(current_pin, stored_pin_hash):
        return False, "Current PIN is incorrect."

    if current_pin == new_pin:
        return False, "New PIN must be different from your current PIN."

    try:
        new_pin_hash = hash_pin(new_pin)
        update_pin(account_id, new_pin_hash)
        return True, "PIN changed successfully."

    except ValueError as error:
        return False, str(error)


from database.operations import get_atm_cash, update_atm_cash


def get_atm_cash_summary():
    cash_details = get_atm_cash()

    total_cash = 0

    for denomination, quantity in cash_details:
        total_cash += denomination * quantity

    return cash_details, total_cash


def calculate_note_distribution(amount):
    cash_details = get_atm_cash()

    remaining_amount = amount
    note_distribution = {}

    for denomination, quantity in sorted(
        cash_details,
        key=lambda item: item[0],
        reverse=True
    ):
        notes_needed = min(
            remaining_amount // denomination,
            quantity
        )

        note_distribution[denomination] = notes_needed
        remaining_amount -= denomination * notes_needed

    if remaining_amount != 0:
        return None

    return note_distribution


def deduct_atm_cash(note_distribution):
    cash_details = dict(get_atm_cash())

    for denomination, notes_used in note_distribution.items():

        if notes_used > cash_details.get(denomination, 0):
            raise ValueError("Insufficient ATM notes.")

    for denomination, notes_used in note_distribution.items():

        if notes_used > 0:
            update_atm_cash(
                denomination,
                cash_details[denomination] - notes_used
            )


def admin_get_atm_cash_summary(session):

    # Verify administrator access
    require_admin_session(session)

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

        cash_details = cursor.fetchall()

        total_cash = sum(
            denomination * quantity
            for denomination, quantity in cash_details
        )

        return cash_details, total_cash

    finally:
        connection.close()


def admin_refill_atm_cash(session, quantities):

    # Verify administrator access
    require_admin_session(session)

    if not isinstance(quantities, dict):
        raise ValueError("Invalid refill details.")

    allowed_denominations = {500, 200, 100}

    for denomination, quantity in quantities.items():

        if denomination not in allowed_denominations:
            raise ValueError("Invalid denomination.")

        if isinstance(quantity, bool) or not isinstance(quantity, int):
            raise ValueError("Note quantities must be whole numbers.")

        if quantity < 0:
            raise ValueError("Note quantities cannot be negative.")

    if not any(quantities.values()):
        raise ValueError("Enter at least one note quantity.")

    connection = get_connection()

    try:
        cursor = connection.cursor()

        # Start a transaction that locks the database for this update
        cursor.execute("BEGIN IMMEDIATE")

        cursor.execute(
            """
            SELECT denomination
            FROM atm_cash
            """
        )

        existing_denominations = {
            row[0] for row in cursor.fetchall()
        }

        for denomination, quantity in quantities.items():

            if denomination not in existing_denominations:
                raise ValueError(
                    f"Denomination ₹{denomination} is not configured."
                )

            if quantity > 0:
                cursor.execute(
                    """
                    UPDATE atm_cash
                    SET quantity = quantity + ?
                    WHERE denomination = ?
                    """,
                    (quantity, denomination)
                )

                if cursor.rowcount != 1:
                    raise ValueError(
                        f"Could not refill ₹{denomination} notes."
                    )

        cursor.execute(
            """
            SELECT denomination, quantity
            FROM atm_cash
            ORDER BY denomination DESC
            """
        )

        cash_details = cursor.fetchall()

        total_cash = sum(
            denomination * quantity
            for denomination, quantity in cash_details
        )

        connection.commit()

        return cash_details, total_cash

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def admin_get_all_accounts(session):

    # Verify administrator access
    require_admin_session(session)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                accounts.account_number,
                customers.name,
                customers.email,
                customers.phone,
                accounts.balance,
                accounts.status,
                customers.created_at
            FROM accounts
            INNER JOIN customers
                ON accounts.customer_id = customers.customer_id
            ORDER BY accounts.account_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()

def admin_get_all_transactions(session):

    # Verify administrator access
    require_admin_session(session)

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                transactions.transaction_id,
                accounts.account_number,
                customers.name,
                transactions.transaction_type,
                transactions.amount,
                transactions.balance_after,
                transactions.status,
                transactions.timestamp
            FROM transactions
            INNER JOIN accounts
                ON transactions.account_id = accounts.account_id
            INNER JOIN customers
                ON accounts.customer_id = customers.customer_id
            ORDER BY transactions.timestamp DESC,
                     transactions.transaction_id DESC
            """
        )

        return cursor.fetchall()

    finally:
        connection.close()

