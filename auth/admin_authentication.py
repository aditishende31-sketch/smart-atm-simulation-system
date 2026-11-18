
from database.database import get_connection
from auth.security import verify_password


class AdminAuthenticationService:

    def login(self, username, password):

        if not username:
            return False, "Username is required."

        if not password:
            return False, "Password is required."

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT admin_id, username, password_hash, status
                FROM admins
                WHERE username = ?
                """,
                (username.strip(),)
            )

            admin = cursor.fetchone()

            if admin is None:
                return False, "Invalid username or password."

            admin_id, username, password_hash, status = admin

            if status != "ACTIVE":
                return False, "Admin account is not active."

            if not verify_password(password, password_hash):
                return False, "Invalid username or password."

            return True, {
                "message": "Admin login successful.",
                "admin_id": admin_id,
                "username": username,
                "role": "ADMIN"
            }

        finally:
            connection.close()
