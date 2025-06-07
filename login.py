"""Implement login functionality."""
from customtkinter import *
import helper


# Set Themes for Application
set_appearance_mode("light")
set_default_color_theme("dark-blue")


class Login(CTk):
    def __init__(self, login_callback):
        super().__init__()
        self.login_callback = login_callback
        self.configure(fg_color="#fff", corner_radius=20)
        self.title("Login: RedRex")

        # Center the window on the screen
        self.update_idletasks()
        w = 400
        h = 400
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.resizable(False, False)

        # Title Frame
        title_frame = CTkFrame(master=self, fg_color="transparent")
        title_frame.pack(anchor="n", fill="x", padx=15, pady=10)
        CTkLabel(master=title_frame, text="Login", font=("Arial Black", 30)).pack(anchor="w", side="left")

        # Username Entry
        self.username_label = CTkLabel(master=self, text="Username:")
        self.username_label.pack(pady=(20, 5))
        self.username_entry = CTkEntry(master=self, width=200)
        self.username_entry.pack(pady=(0, 20))

        # Password Entry
        self.password_label = CTkLabel(master=self, text="Password:")
        self.password_label.pack(pady=(0, 5))
        self.password_entry = CTkEntry(master=self, show='*', width=200)
        self.password_entry.pack(pady=(0, 20))

        # Login Button
        self.login_button = CTkButton(master=self, text="Login", command=self.login)
        self.login_button.pack(pady=(10, 0))

    def login(self):
        """Handle login action."""
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            if self.login_callback(username, password):
                self.destroy()
                import app
            else:
                print("Login failed")
        else:
            print("Please enter both username and password")


if __name__ == "__main__":
    login_app = Login(helper.login_callback)
    login_app.mainloop()

