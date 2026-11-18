
import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from gui.atm_cash import ATMCashWindow
from gui.refill_atm import RefillATMWindow
from gui.all_accounts import AllAccountsWindow
from gui.all_transactions import AllTransactionsWindow

from banking.service import (
    admin_get_atm_cash_summary,
    admin_get_all_accounts,
    admin_get_all_transactions
)


class AdminDashboardWindow:

    def __init__(self, root, session, on_logout):

        self.root = root
        self.session = session
        self.on_logout = on_logout

        self.root.title("Smart ATM | Administration Panel")
        self.root.geometry("1150x760")
        self.root.minsize(1000, 680)
        self.root.configure(bg="#F3F6FB")

        self.stat_labels = {}

        self.create_widgets()
        self.load_statistics()

    # -----------------------------------------
    # MAIN DASHBOARD
    # -----------------------------------------

    def create_widgets(self):

        # LEFT SIDEBAR
        self.sidebar = tk.Frame(
            self.root,
            bg="#14213D",
            width=235
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        # MAIN CONTENT
        self.content = tk.Frame(
            self.root,
            bg="#F3F6FB"
        )

        self.content.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_sidebar()
        self.create_header()
        self.create_statistics()
        self.create_quick_actions()

    # -----------------------------------------
    # SIDEBAR
    # -----------------------------------------

    def create_sidebar(self):

        tk.Label(
            self.sidebar,
            text="🏦 SMART ATM",
            font=("Arial", 21, "bold"),
            bg="#14213D",
            fg="white"
        ).pack(pady=(35, 5))

        tk.Label(
            self.sidebar,
            text="ADMINISTRATION PANEL",
            font=("Arial", 9, "bold"),
            bg="#14213D",
            fg="#AAB8D0"
        ).pack(pady=(0, 40))

        tk.Label(
            self.sidebar,
            text="MAIN MENU",
            font=("Arial", 9, "bold"),
            bg="#14213D",
            fg="#8293B2"
        ).pack(anchor="w", padx=25, pady=(0, 12))

        self.create_sidebar_button(
            "▦   Dashboard",
            self.load_statistics
        )

        self.create_sidebar_button(
            "🏧   View ATM Cash",
            self.view_atm_cash
        )

        self.create_sidebar_button(
            "💵   Refill ATM Cash",
            self.refill_atm_cash
        )

        self.create_sidebar_button(
            "👥   All Accounts",
            self.view_all_accounts
        )

        self.create_sidebar_button(
            "📜   All Transactions",
            self.view_transactions
        )

        tk.Frame(
            self.sidebar,
            bg="#344563",
            height=1
        ).pack(fill="x", padx=20, pady=25)

        tk.Label(
            self.sidebar,
            text="ADMIN ACCOUNT",
            font=("Arial", 9, "bold"),
            bg="#14213D",
            fg="#8293B2"
        ).pack(anchor="w", padx=25, pady=5)

        tk.Label(
            self.sidebar,
            text=f"👤  {self.session.username}",
            font=("Arial", 11, "bold"),
            bg="#14213D",
            fg="white"
        ).pack(anchor="w", padx=25, pady=10)

        tk.Button(
            self.sidebar,
            text="🚪  Logout",
            font=("Arial", 11, "bold"),
            bg="#C0394B",
            fg="white",
            activebackground="#A93243",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=self.logout
        ).pack(
            side="bottom",
            fill="x",
            padx=20,
            pady=25,
            ipady=10
        )

    def create_sidebar_button(self, text, command):

        button = tk.Button(
            self.sidebar,
            text=text,
            font=("Arial", 11),
            bg="#14213D",
            fg="#E7ECF5",
            activebackground="#253B60",
            activeforeground="white",
            relief="flat",
            anchor="w",
            cursor="hand2",
            command=command
        )

        button.pack(
            fill="x",
            padx=12,
            pady=4,
            ipady=11
        )

    # -----------------------------------------
    # HEADER
    # -----------------------------------------

    def create_header(self):

        header = tk.Frame(
            self.content,
            bg="#F3F6FB"
        )

        header.pack(
            fill="x",
            padx=35,
            pady=(30, 15)
        )

        left = tk.Frame(
            header,
            bg="#F3F6FB"
        )

        left.pack(side="left")

        tk.Label(
            left,
            text="Dashboard Overview",
            font=("Arial", 24, "bold"),
            bg="#F3F6FB",
            fg="#172B4D"
        ).pack(anchor="w")

        tk.Label(
            left,
            text=f"Welcome back, {self.session.username}!",
            font=("Arial", 11),
            bg="#F3F6FB",
            fg="#718096"
        ).pack(anchor="w", pady=5)

        right = tk.Frame(
            header,
            bg="#F3F6FB"
        )

        right.pack(side="right")

        tk.Label(
            right,
            text=datetime.now().strftime("%d %B %Y"),
            font=("Arial", 10, "bold"),
            bg="#F3F6FB",
            fg="#52627A"
        ).pack(pady=5)

        tk.Button(
            right,
            text="↻  Refresh Statistics",
            font=("Arial", 10, "bold"),
            bg="#FFFFFF",
            fg="#2457A6",
            activebackground="#E7EFFB",
            relief="flat",
            cursor="hand2",
            command=self.load_statistics
        ).pack(pady=5)

    # -----------------------------------------
    # STATISTICS CARDS
    # -----------------------------------------

    def create_statistics(self):

        tk.Label(
            self.content,
            text="SYSTEM STATISTICS",
            font=("Arial", 12, "bold"),
            bg="#F3F6FB",
            fg="#52627A"
        ).pack(anchor="w", padx=35, pady=(15, 10))

        self.stats_frame = tk.Frame(
            self.content,
            bg="#F3F6FB"
        )

        self.stats_frame.pack(
            fill="x",
            padx=25
        )

        cards = [
            ("accounts", "Total Accounts", "0", "#2878D0"),
            ("cash", "Total ATM Cash", "₹0", "#169B75"),
            ("transactions", "Transactions", "0", "#805AD5"),
            ("active", "Active Accounts", "0", "#E69B26")
        ]

        for column in range(4):
            self.stats_frame.columnconfigure(
                column,
                weight=1
            )

        for index, (key, title, value, accent) in enumerate(cards):

            card = tk.Frame(
                self.stats_frame,
                bg="white",
                highlightbackground="#E1E7F0",
                highlightthickness=1
            )

            card.grid(
                row=0,
                column=index,
                sticky="nsew",
                padx=8,
                pady=8,
                ipady=10
            )

            tk.Frame(
                card,
                bg=accent,
                height=5
            ).pack(fill="x")

            tk.Label(
                card,
                text=title,
                font=("Arial", 10, "bold"),
                bg="white",
                fg="#718096"
            ).pack(
                anchor="w",
                padx=15,
                pady=(15, 8)
            )

            value_label = tk.Label(
                card,
                text=value,
                font=("Arial", 21, "bold"),
                bg="white",
                fg="#172B4D"
            )

            value_label.pack(
                anchor="w",
                padx=15,
                pady=(0, 15)
            )

            self.stat_labels[key] = value_label

    # -----------------------------------------
    # QUICK ACTIONS
    # -----------------------------------------

    def create_quick_actions(self):

        section = tk.Frame(
            self.content,
            bg="#F3F6FB"
        )

        section.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=(25, 15)
        )

        tk.Label(
            section,
            text="QUICK ACTIONS",
            font=("Arial", 12, "bold"),
            bg="#F3F6FB",
            fg="#52627A"
        ).pack(anchor="w", pady=(0, 12))

        actions_frame = tk.Frame(
            section,
            bg="#F3F6FB"
        )

        actions_frame.pack(
            fill="both",
            expand=True
        )

        actions_frame.columnconfigure(0, weight=1)
        actions_frame.columnconfigure(1, weight=1)

        self.create_action_card(
            actions_frame,
            "🏧  ATM Cash Management",
            "Check the available denominations and total cash inside the ATM.",
            "VIEW ATM CASH",
            self.view_atm_cash,
            0,
            0
        )

        self.create_action_card(
            actions_frame,
            "💵  Refill ATM Cash",
            "Add new currency notes to the ATM cash inventory.",
            "REFILL CASH",
            self.refill_atm_cash,
            0,
            1
        )

        self.create_action_card(
            actions_frame,
            "👥  Customer Accounts",
            "View registered customers, balances and account status.",
            "VIEW ACCOUNTS",
            self.view_all_accounts,
            1,
            0
        )

        self.create_action_card(
            actions_frame,
            "📜  Transaction History",
            "Monitor deposits, withdrawals and money transfers.",
            "VIEW TRANSACTIONS",
            self.view_transactions,
            1,
            1
        )

    def create_action_card(
        self,
        parent,
        title,
        description,
        button_text,
        command,
        row,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white",
            highlightbackground="#E1E7F0",
            highlightthickness=1
        )

        card.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=8,
            pady=8
        )

        tk.Label(
            card,
            text=title,
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#172B4D"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        tk.Label(
            card,
            text=description,
            font=("Arial", 10),
            bg="white",
            fg="#718096",
            wraplength=310,
            justify="left"
        ).pack(
            anchor="w",
            padx=20,
            pady=5
        )

        tk.Button(
            card,
            text=button_text,
            font=("Arial", 10, "bold"),
            bg="#2457A6",
            fg="white",
            activebackground="#173F80",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            command=command
        ).pack(
            anchor="w",
            padx=20,
            pady=(12, 18),
            ipadx=12,
            ipady=7
        )

    # -----------------------------------------
    # LOAD DASHBOARD STATISTICS
    # -----------------------------------------

    def load_statistics(self):

        if not self.session.is_active():

            messagebox.showerror(
                "Session Expired",
                "Admin session expired. Please log in again.",
                parent=self.root
            )

            self.force_logout()
            return

        try:

            accounts = admin_get_all_accounts(
                self.session
            )

            transactions = admin_get_all_transactions(
                self.session
            )

            cash_details, total_cash = admin_get_atm_cash_summary(
                self.session
            )

            active_accounts = sum(
                1 for account in accounts
                if account[5] == "ACTIVE"
            )

            self.stat_labels["accounts"].config(
                text=str(len(accounts))
            )

            self.stat_labels["cash"].config(
                text=f"₹{total_cash:,.0f}"
            )

            self.stat_labels["transactions"].config(
                text=str(len(transactions))
            )

            self.stat_labels["active"].config(
                text=str(active_accounts)
            )

        except PermissionError as error:

            messagebox.showerror(
                "Access Denied",
                str(error),
                parent=self.root
            )

            self.force_logout()

        except Exception as error:

            messagebox.showerror(
                "Dashboard Error",
                str(error),
                parent=self.root
            )

    # -----------------------------------------
    # ADMIN ACTIONS
    # -----------------------------------------

    def view_atm_cash(self):

        if not self.check_session():
            return

        ATMCashWindow(
            self.root,
            self.session
        )

    def refill_atm_cash(self):

        if not self.check_session():
            return

        RefillATMWindow(
            self.root,
            self.session
        )

    def view_all_accounts(self):

        if not self.check_session():
            return

        AllAccountsWindow(
            self.root,
            self.session
        )

    def view_transactions(self):

        if not self.check_session():
            return

        AllTransactionsWindow(
            self.root,
            self.session
        )

    # -----------------------------------------
    # SESSION MANAGEMENT
    # -----------------------------------------

    def check_session(self):

        if not self.session.is_active():

            messagebox.showwarning(
                "Session Expired",
                "Please log in again.",
                parent=self.root
            )

            self.force_logout()
            return False

        self.session.update_activity()
        return True

    def force_logout(self):

        self.session.logout()
        self.root.destroy()
        self.on_logout()

    def logout(self):

        answer = messagebox.askyesno(
            "Logout",
            "Are you sure you want to logout?",
            parent=self.root
        )

        if answer:
            self.force_logout()
