
import getpass

from database.database import get_connection
from auth.security import hash_password


def create_admin():

    print("\n===== SMART ATM ADMIN SETUP =====")

    username = input("Enter admin username: ").strip()

    if not username:
        print("Username cannot be empty.")
        return

    password = getpass.getpass("Create admin password: ")
    confirm_password = getpass.getpass("Confirm admin password: ")

    if password != confirm_password:
        print("Passwords do not match.")
        return

    try:
        password_hash = hash_password(password)

    except ValueError as error:
        print(error)
        return

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO admins (username, password_hash)
            VALUES (?, ?)
            """,
            (username, password_hash)
        )

        connection.commit()

        print("\nAdmin account created successfully!")

    except Exception as error:
        connection.rollback()

        if "UNIQUE constraint failed" in str(error):
            print("This admin username already exists.")
        else:
            print("Error creating admin:", error)

    finally:
        connection.close()


if __name__ == "__main__":
    create_admin()
