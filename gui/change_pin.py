
import tkinter as tk
from tkinter import messagebox
from banking.service import change_pin


class ChangePinWindow:

    def __init__(self, parent, session):

        self.parent = parent
        self.session = session

        self.window = tk.Toplevel(parent)
        self.window.title("Change PIN")
        self.window.geometry("450x550")
        self.window.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):

        frame = tk.Frame(self.window, padx=40, pady=25)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="🔐",
            font=("Arial", 40)
        ).pack()

        tk.Label(
            frame,
            text="Change ATM PIN",
            font=("Arial", 20, "bold")
        ).pack(pady=10)

        tk.Label(
            frame,
            text=f"Account: {self.session.account_number}",
            font=("Arial", 10)
        ).pack(pady=(0, 20))

        tk.Label(
            frame,
            text="Current PIN",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(5, 5))

        self.current_pin_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center",
            show="*"
        )
        self.current_pin_entry.pack(fill="x", ipady=7)

        tk.Label(
            frame,
            text="New PIN",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.new_pin_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center",
            show="*"
        )
        self.new_pin_entry.pack(fill="x", ipady=7)

        tk.Label(
            frame,
            text="Confirm New PIN",
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=(15, 5))

        self.confirm_pin_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center",
            show="*"
        )
        self.confirm_pin_entry.pack(fill="x", ipady=7)

        tk.Button(
            frame,
            text="CHANGE PIN",
            font=("Arial", 12, "bold"),
            command=self.change_pin_action,
            cursor="hand2"
        ).pack(fill="x", pady=(25, 10), ipady=8)

        tk.Button(
            frame,
            text="CANCEL",
            command=self.window.destroy,
            cursor="hand2"
        ).pack(fill="x", ipady=5)

        self.current_pin_entry.focus()

        self.window.bind(
            "<Return>",
            lambda event: self.change_pin_action()
        )

    def change_pin_action(self):

        current_pin = self.current_pin_entry.get().strip()
        new_pin = self.new_pin_entry.get().strip()
        confirm_pin = self.confirm_pin_entry.get().strip()

        if not current_pin or not new_pin or not confirm_pin:
            messagebox.showerror(
                "Missing Details",
                "Please fill in all PIN fields.",
                parent=self.window
            )
            return

        if not current_pin.isdigit() or len(current_pin) != 4:
            messagebox.showerror(
                "Invalid PIN",
                "Current PIN must contain exactly 4 digits.",
                parent=self.window
            )
            return

        if not new_pin.isdigit() or len(new_pin) != 4:
            messagebox.showerror(
                "Invalid PIN",
                "New PIN must contain exactly 4 digits.",
                parent=self.window
            )
            return

        if new_pin != confirm_pin:
            messagebox.showerror(
                "PIN Mismatch",
                "New PIN and confirmation PIN do not match.",
                parent=self.window
            )
            return

        confirmed = messagebox.askyesno(
            "Confirm PIN Change",
            "Are you sure you want to change your ATM PIN?",
            parent=self.window
        )

        if not confirmed:
            return

        success, message = change_pin(
            self.session.account_number,
            current_pin,
            new_pin
        )

        if success:

            messagebox.showinfo(
                "Success",
                message,
                parent=self.window
            )

            self.window.destroy()

        else:

            messagebox.showerror(
                "Change PIN Failed",
                message,
                parent=self.window
            )
