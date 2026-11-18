
import tkinter as tk
from tkinter import ttk, messagebox

from banking.service import admin_get_all_transactions


class AllTransactionsWindow:

    def __init__(self, parent, session):

        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("All ATM Transactions")
        self.window.geometry("1150x550")
        self.window.resizable(True, True)

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):

        main_frame = tk.Frame(
            self.window,
            padx=20,
            pady=20
        )

        main_frame.pack(fill="both", expand=True)

        tk.Label(
            main_frame,
            text="ALL ATM TRANSACTIONS",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        self.count_label = tk.Label(
            main_frame,
            text="Total Transactions: 0",
            font=("Arial", 12, "bold")
        )

        self.count_label.pack(pady=5)

        table_frame = tk.Frame(main_frame)
        table_frame.pack(fill="both", expand=True, pady=10)

        columns = (
            "transaction_id",
            "account_number",
            "customer_name",
            "transaction_type",
            "amount",
            "balance_after",
            "status",
            "timestamp"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        headings = {
            "transaction_id": "Transaction ID",
            "account_number": "Account Number",
            "customer_name": "Customer Name",
            "transaction_type": "Transaction Type",
            "amount": "Amount",
            "balance_after": "Balance After",
            "status": "Status",
            "timestamp": "Date & Time"
        }

        widths = {
            "transaction_id": 100,
            "account_number": 120,
            "customer_name": 140,
            "transaction_type": 150,
            "amount": 110,
            "balance_after": 120,
            "status": 90,
            "timestamp": 160
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
            command=self.load_transactions
        ).pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 11, "bold"),
            command=self.window.destroy
        ).pack(side="left", fill="x", expand=True, padx=5)

    def load_transactions(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            transactions = admin_get_all_transactions(
                self.session
            )

            for transaction in transactions:

                (
                    transaction_id,
                    account_number,
                    customer_name,
                    transaction_type,
                    amount,
                    balance_after,
                    status,
                    timestamp
                ) = transaction

                self.tree.insert(
                    "",
                    "end",
                    values=(
                        transaction_id,
                        account_number,
                        customer_name,
                        transaction_type,
                        f"₹{amount:,.2f}",
                        f"₹{balance_after:,.2f}",
                        status,
                        timestamp
                    )
                )

            self.count_label.config(
                text=f"Total Transactions: {len(transactions)}"
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
