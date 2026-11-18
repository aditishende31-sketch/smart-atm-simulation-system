
import tkinter as tk
from tkinter import ttk, messagebox

from database.operations import get_transactions

class TransactionHistoryWindow:

    def __init__(self, parent, session):

        self.parent = parent
        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Transaction History")
        self.window.geometry("850x550")
        self.window.resizable(True, True)

        self.create_widgets()
        self.load_transactions()

    def create_widgets(self):

        main_frame = tk.Frame(
            self.window,
            padx=20,
            pady=20
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # Heading
        tk.Label(
            main_frame,
            text="📜",
            font=("Arial", 35)
        ).pack()

        tk.Label(
            main_frame,
            text="Transaction History",
            font=("Arial", 21, "bold")
        ).pack(pady=5)

        tk.Label(
            main_frame,
            text=f"Account Number: {self.session.account_number}",
            font=("Arial", 11)
        ).pack(pady=(0, 15))

        # Table frame
        table_frame = tk.Frame(main_frame)
        table_frame.pack(
            fill="both",
            expand=True
        )

        columns = (
            "id",
            "date",
            "type",
            "amount",
            "balance",
            "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        # Column headings
        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date & Time")
        self.tree.heading("type", text="Transaction Type")
        self.tree.heading("amount", text="Amount (₹)")
        self.tree.heading("balance", text="Balance After (₹)")
        self.tree.heading("status", text="Status")

        # Column widths
        self.tree.column("id", width=45, anchor="center")
        self.tree.column("date", width=150, anchor="center")
        self.tree.column("type", width=145, anchor="center")
        self.tree.column("amount", width=115, anchor="e")
        self.tree.column("balance", width=140, anchor="e")
        self.tree.column("status", width=90, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # Table styling
        style = ttk.Style()

        style.configure(
            "Treeview",
            font=("Arial", 10),
            rowheight=30
        )

        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        # Table row colors
        self.tree.tag_configure(
            "success",
            foreground="green"
        )

        # Empty message
        self.empty_label = tk.Label(
            main_frame,
            text="No transactions found.",
            font=("Arial", 11),
            fg="gray"
        )

        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(
            fill="x",
            pady=(15, 0)
        )

        tk.Button(
            button_frame,
            text="🔄 Refresh",
            font=("Arial", 11, "bold"),
            command=self.load_transactions,
            cursor="hand2"
        ).pack(
            side="left",
            ipadx=15,
            ipady=5
        )

        tk.Button(
            button_frame,
            text="CLOSE",
            font=("Arial", 11, "bold"),
            command=self.window.destroy,
            cursor="hand2"
        ).pack(
            side="right",
            ipadx=15,
            ipady=5
        )

    def load_transactions(self):

        # Clear old table records
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:

            transactions = get_transactions(
                self.session.account_id
            )

            if not transactions:

                self.empty_label.pack(pady=10)
                return

            self.empty_label.pack_forget()

            for transaction in transactions:

                (
                    transaction_id,
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
                        timestamp,
                        transaction_type.replace("_", " "),
                        f"{amount:,.2f}",
                        f"{balance_after:,.2f}",
                        status
                    ),
                    tags=("success",) if status == "SUCCESS" else ()
                )

        except Exception as error:

            messagebox.showerror(
                "Transaction History Error",
                str(error),
                parent=self.window
            )