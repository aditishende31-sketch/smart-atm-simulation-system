import unittest
from datetime import datetime, timedelta

from auth.session import AdminSession, Session, require_admin_session


class RequireAdminSessionTests(unittest.TestCase):

    def test_accepts_active_admin_session(self):
        session = AdminSession(admin_id=1, username="admin")

        require_admin_session(session)

        self.assertTrue(session.is_active())

    def test_rejects_regular_session(self):
        session = Session(account_id=1, account_number="100001")

        with self.assertRaises(PermissionError):
            require_admin_session(session)

    def test_rejects_expired_admin_session(self):
        session = AdminSession(admin_id=1, username="admin")
        session.last_activity = datetime.now() - timedelta(minutes=6)

        with self.assertRaisesRegex(PermissionError, "session expired"):
            require_admin_session(session)


if __name__ == "__main__":
    unittest.main()
