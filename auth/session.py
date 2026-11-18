from datetime import datetime, timedelta


class Session:

    def __init__(
        self,
        account_id,
        account_number,
        timeout_minutes=5
    ):

        self.account_id = account_id
        self.account_number = account_number

        self.timeout_minutes = timeout_minutes

        self.login_time = datetime.now()
        self.last_activity = datetime.now()

        self.active = True

    def update_activity(self):

        if self.active:
            self.last_activity = datetime.now()

    def is_expired(self):

        if not self.active:
            return True

        elapsed = (
            datetime.now()
            - self.last_activity
        )

        return elapsed > timedelta(
            minutes=self.timeout_minutes
        )

    def is_active(self):

        if self.is_expired():
            self.active = False

        return self.active

    def logout(self):

        self.active = False

    
class AdminSession:

    def __init__(
        self,
        admin_id,
        username,
        timeout_minutes=5
    ):

        self.admin_id = admin_id
        self.username = username
        self.role = "ADMIN"

        self.timeout_minutes = timeout_minutes

        self.login_time = datetime.now()
        self.last_activity = datetime.now()

        self.active = True

    def update_activity(self):

        if self.active:
            self.last_activity = datetime.now()

    def is_expired(self):

        if not self.active:
            return True

        elapsed = datetime.now() - self.last_activity

        return elapsed > timedelta(
            minutes=self.timeout_minutes
        )

    def is_active(self):

        if self.is_expired():
            self.active = False

        return self.active

    def logout(self):

        self.active = False


def require_admin_session(session):

    if not isinstance(session, AdminSession):
        raise PermissionError(
            "Administrator access is required."
        )

    if session.role != "ADMIN":
        raise PermissionError(
            "Administrator access is required."
        )

    if not session.is_active():
        raise PermissionError(
            "Admin session expired. Please log in again."
        )

    session.update_activity()
