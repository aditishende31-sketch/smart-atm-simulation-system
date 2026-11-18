import tkinter as tk
from tkinter import messagebox
from gui.balance import BalanceWindow
from gui.deposit import DepositWindow
from gui.withdrawal import WithdrawalWindow
from gui.transfer import TransferWindow
from gui.transaction_history import TransactionHistoryWindow
from gui.change_pin import ChangePinWindow


class DashboardWindow:

    def __init__(self, root, session, on_logout):

        self.root = root
        self.session = session
        self.on_logout = on_logout

        self.root.title("Smart ATM - Dashboard")
        self.root.geometry("600x700")
        self.root.resizable(False, False)

        self.create_widgets()

    # -----------------------------------------
    # Create Dashboard
    # -----------------------------------------

    def create_widgets(self):

        main_frame = tk.Frame(
            self.root,
            padx=40,
            pady=30
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # ATM icon
        logo = tk.Label(
            main_frame,
            text="🏦",
            font=("Arial", 45)
        )

        logo.pack(pady=(5, 0))

        # Title
        title = tk.Label(
            main_frame,
            text="SMART ATM",
            font=("Arial", 24, "bold")
        )

        title.pack()

        # Welcome message
        welcome = tk.Label(
            main_frame,
            text=f"Welcome\nAccount: {self.session.account_number}",
            font=("Arial", 12)
        )

        welcome.pack(pady=(5, 25))

        # -----------------------------------------
        # Buttons
        # -----------------------------------------

        self.create_button(
            main_frame,
            "💰  Check Balance",
            self.check_balance
        )

        self.create_button(
            main_frame,
            "💵  Deposit Money",
            self.deposit_money
        )

        self.create_button(
            main_frame,
            "🏧  Withdraw Money",
            self.withdraw_money
        )

        self.create_button(
            main_frame,
            "🔄  Transfer Money",
            self.transfer_money
        )

        self.create_button(
            main_frame,
            "📜  Transaction History",
            self.transaction_history
        )

        self.create_button(
            main_frame,
            "🔐  Change PIN",
            self.change_pin
        )

        # Logout
        logout_button = tk.Button(
            main_frame,
            text="🚪  Logout",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=self.logout
        )

        logout_button.pack(
            fill="x",
            ipady=8,
            pady=(20, 5)
        )

        # Footer
        footer = tk.Label(
            main_frame,
            text="Smart ATM Banking System",
            font=("Arial", 9)
        )

        footer.pack(
            side="bottom",
            pady=10
        )

    # -----------------------------------------
    # Button creator
    # -----------------------------------------

    def create_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text=text,
            font=("Arial", 12, "bold"),
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            ipady=8,
            pady=5
        )

    # -----------------------------------------
    # Features - temporary placeholders
    # -----------------------------------------

    def check_balance(self):
        from gui.balance import BalanceWindow

        BalanceWindow(self.root, self.session)

    def deposit_money(self):

        DepositWindow(
            self.root,
            self.session
        )
            
    def withdraw_money(self):

        WithdrawalWindow(
            self.root,
            self.session
        )

    def transfer_money(self):
        TransferWindow(
            self.root,
            self.session
        )

    def transaction_history(self):

        TransactionHistoryWindow(
            self.root,
            self.session
        )

    def change_pin(self):
        ChangePinWindow(
            self.root, 
            self.session
            )

    # -----------------------------------------
    # Logout
    # -----------------------------------------

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?"
        )

        if answer:

            self.session.logout()

            self.root.destroy()

            self.on_logout()