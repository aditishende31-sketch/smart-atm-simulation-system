
import tkinter as tk
from tkinter import ttk, messagebox

from banking.service import admin_get_all_accounts


class AllAccountsWindow:

    def __init__(self, parent, session):

        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("All Customer Accounts")
        self.window.geometry("1100x550")
        self.window.resizable(True, True)

        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):

        main_frame = tk.Frame(
            self.window,
            padx=20,
            pady=20
        )

        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame,
            text="ALL CUSTOMER ACCOUNTS",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.count_label = tk.Label(
            main_frame,
            text="Total Accounts: 0",
            font=("Arial", 12, "bold")
        )

        self.count_label.pack(pady=5)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = (
            "account_number",
            "name",
            "email",
            "phone",
            "balance",
            "status",
            "created_at"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "account_number": "Account Number",
            "name": "Customer Name",
            "email": "Email",
            "phone": "Phone",
            "balance": "Balance",
            "status": "Status",
            "created_at": "Registration Date"
        }

        widths = {
            "account_number": 120,
            "name": 140,
            "email": 180,
            "phone": 110,
            "balance": 100,
            "status": 90,
            "created_at": 150
        }

        for column in columns:

            self.tree.heading(
                column,
                text=headings[column]
            )

            self.tree.column(
                column,
                width=widths[column],
                anchor="center"
            )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill="x", pady=10)

        tk.Button(
            button_frame,
            text="REFRESH",
            font=("Arial", 11, "bold"),
            command=self.load_accounts
        ).pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 11, "bold"),
            command=self.window.destroy
        ).pack(side="left", fill="x", expand=True, padx=5)

    def load_accounts(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            accounts = admin_get_all_accounts(
                self.session
            )

            for account in accounts:

                (
                    account_number,
                    name,
                    email,
                    phone,
                    balance,
                    status,
                    created_at
                ) = account

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        account_number,
                        name,
                        email,
                        phone or "N/A",
                        f"₹{balance:,.2f}",
                        status,
                        created_at
                    )
                )

            self.count_label.config(
                text=f"Total Accounts: {len(accounts)}"
            )

        except PermissionError as error:

            messagebox.showerror(
                "Access Denied",
                str(error),
                parent=self.window
            )

            self.window.destroy()

        except Exception as error:

            messagebox.showerror(
                "Error",
                str(error),
                parent=self.window
            )

