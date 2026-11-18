
import tkinter as tk
from tkinter import messagebox

from auth.authentication import AuthenticationService
from auth.admin_authentication import AdminAuthenticationService
from auth.session import Session, AdminSession

from gui.dashboard import DashboardWindow
from gui.admin_dashboard import AdminDashboardWindow


class LoginWindow:

    def __init__(self, root):

        self.root = root
        self.root.title("Smart ATM Banking System")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        self.auth_service = AuthenticationService()
        self.admin_auth_service = AdminAuthenticationService()

        self.session = None
        self.login_mode = tk.StringVar(value="CUSTOMER")

        self.create_widgets()

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

        logo = tk.Label(
            main_frame,
            text="🏦",
            font=("Arial", 55)
        )
        logo.pack(pady=(5, 0))

        title = tk.Label(
            main_frame,
            text="SMART ATM",
            font=("Arial", 26, "bold")
        )
        title.pack()

        subtitle = tk.Label(
            main_frame,
            text="Secure Banking System",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 20))

        # Login mode selector

        mode_label = tk.Label(
            main_frame,
            text="Select Login Type",
            font=("Arial", 11, "bold")
        )
        mode_label.pack(pady=(5, 8))

        mode_frame = tk.Frame(main_frame)
        mode_frame.pack(pady=(0, 20))

        tk.Radiobutton(
            mode_frame,
            text="Customer Login",
            variable=self.login_mode,
            value="CUSTOMER",
            font=("Arial", 11),
            command=self.change_login_mode
        ).pack(side="left", padx=10)

        tk.Radiobutton(
            mode_frame,
            text="Admin Login",
            variable=self.login_mode,
            value="ADMIN",
            font=("Arial", 11),
            command=self.change_login_mode
        ).pack(side="left", padx=10)

        # Dynamic username/account label

        self.account_label = tk.Label(
            main_frame,
            text="Account Number",
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        self.account_label.pack(
            fill="x",
            pady=(5, 5)
        )

        self.account_entry = tk.Entry(
            main_frame,
            font=("Arial", 14),
            justify="center"
        )
        self.account_entry.pack(
            fill="x",
            ipady=8,
            pady=(0, 20)
        )

        # Dynamic PIN/password label

        self.pin_label = tk.Label(
            main_frame,
            text="4-Digit PIN",
            font=("Arial", 11, "bold"),
            anchor="w"
        )
        self.pin_label.pack(
            fill="x",
            pady=(5, 5)
        )

        self.pin_entry = tk.Entry(
            main_frame,
            font=("Arial", 14),
            justify="center",
            show="●"
        )
        self.pin_entry.pack(
            fill="x",
            ipady=8,
            pady=(0, 10)
        )

        # Show PIN/password

        self.show_pin_var = tk.BooleanVar()

        tk.Checkbutton(
            main_frame,
            text="Show PIN / Password",
            variable=self.show_pin_var,
            command=self.toggle_pin
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # Login button

        tk.Button(
            main_frame,
            text="LOGIN",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            command=self.login
        ).pack(
            fill="x",
            ipady=10,
            pady=10
        )

        # Clear button

        tk.Button(
            main_frame,
            text="CLEAR",
            font=("Arial", 11),
            cursor="hand2",
            command=self.clear_fields
        ).pack(
            fill="x",
            ipady=6,
            pady=5
        )

        footer = tk.Label(
            main_frame,
            text="Secure ATM Banking • Python Project",
            font=("Arial", 9)
        )
        footer.pack(
            side="bottom",
            pady=10
        )

        self.root.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.account_entry.focus()

    # -----------------------------------------
    # Change login mode
    # -----------------------------------------

    def change_login_mode(self):

        self.clear_fields()

        if self.login_mode.get() == "CUSTOMER":

            self.account_label.config(
                text="Account Number"
            )

            self.pin_label.config(
                text="4-Digit PIN"
            )

            self.pin_entry.config(
                show="●"
            )

        else:

            self.account_label.config(
                text="Admin Username"
            )

            self.pin_label.config(
                text="Admin Password"
            )

            self.pin_entry.config(
                show="●"
            )

        self.show_pin_var.set(False)

    # -----------------------------------------
    # Show / Hide PIN or Password
    # -----------------------------------------

    def toggle_pin(self):

        if self.show_pin_var.get():
            self.pin_entry.config(show="")
        else:
            self.pin_entry.config(show="●")

    # -----------------------------------------
    # Clear fields
    # -----------------------------------------

    def clear_fields(self):

        self.account_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)

        self.account_entry.focus()

    # -----------------------------------------
    # Login
    # -----------------------------------------

    def login(self):

        username_or_account = self.account_entry.get().strip()
        password_or_pin = self.pin_entry.get()

        if not username_or_account:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your username or account number."
            )
            return

        if not password_or_pin:
            messagebox.showwarning(
                "Missing Information",
                "Please enter your password or PIN."
            )
            return

        # CUSTOMER LOGIN

        if self.login_mode.get() == "CUSTOMER":

            pin = password_or_pin.strip()

            if not pin.isdigit() or len(pin) != 4:
                messagebox.showwarning(
                    "Invalid PIN",
                    "PIN must contain exactly 4 digits."
                )
                return

            success, result = self.auth_service.login(
                username_or_account,
                pin
            )

            if success:

                self.session = Session(
                    result["account_id"],
                    result["account_number"]
                )

                messagebox.showinfo(
                    "Login Successful",
                    "Welcome to Smart ATM Banking!"
                )

                self.open_customer_dashboard()

            else:

                messagebox.showerror(
                    "Login Failed",
                    result
                )

                self.pin_entry.delete(0, tk.END)

        # ADMIN LOGIN

        else:

            success, result = self.admin_auth_service.login(
                username_or_account,
                password_or_pin
            )

            if success:

                self.session = AdminSession(
                    result["admin_id"],
                    result["username"]
                )

                messagebox.showinfo(
                    "Admin Login Successful",
                    "Welcome to Smart ATM Administration!"
                )

                self.open_admin_dashboard()

            else:

                messagebox.showerror(
                    "Login Failed",
                    result
                )

                self.pin_entry.delete(0, tk.END)

    # -----------------------------------------
    # Open customer dashboard
    # -----------------------------------------

    def open_customer_dashboard(self):

        self.root.destroy()

        dashboard_root = tk.Tk()

        DashboardWindow(
            dashboard_root,
            self.session,
            self.return_to_login
        )

        dashboard_root.mainloop()

    # -----------------------------------------
    # Open admin dashboard
    # -----------------------------------------

    def open_admin_dashboard(self):

        self.root.destroy()

        dashboard_root = tk.Tk()

        AdminDashboardWindow(
            dashboard_root,
            self.session,
            self.return_to_login
        )

        dashboard_root.mainloop()

    # -----------------------------------------
    # Return to login
    # -----------------------------------------

    def return_to_login(self):

        self.root = tk.Tk()

        LoginWindow(self.root)

        self.root.mainloop()
