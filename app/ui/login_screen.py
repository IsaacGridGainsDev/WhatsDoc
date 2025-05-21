import os
import tkinter as tk
import customtkinter as ctk
from app.auth.authentication import Authentication

class LoginScreen(ctk.CTkToplevel):
    """
    Login screen for WhatsDoc app
    """
    def __init__(self, master, on_login_success=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Configure window
        self.title("WhatsDoc - Login")
        self.geometry("400x500")
        self.resizable(False, False)
        
        # Make this window modal
        self.transient(master)
        self.grab_set()
        
        # Center the window
        self.center_window()
        
        # Initialize authentication
        self.auth = Authentication()
        
        # Callback for successful login
        self.on_login_success = on_login_success
        
        # Create UI elements
        self.create_widgets()
        
        # Focus on username entry
        self.username_entry.focus_set()
    
    def center_window(self):
        """
        Center the window on the screen
        """
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """
        Create UI widgets
        """
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(
            self.main_frame, 
            text="WhatsDoc", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.logo_label.pack(pady=(20, 10))
        
        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Document Automation Tool", 
            font=ctk.CTkFont(size=14)
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # Login frame
        self.login_frame = ctk.CTkFrame(self.main_frame)
        self.login_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Tab view for login/register
        self.tab_view = ctk.CTkTabview(self.login_frame)
        self.tab_view.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.login_tab = self.tab_view.add("Login")
        self.register_tab = self.tab_view.add("Register")
        
        # Login tab
        self.username_label = ctk.CTkLabel(
            self.login_tab, 
            text="Username:", 
            font=ctk.CTkFont(size=14)
        )
        self.username_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.username_entry = ctk.CTkEntry(
            self.login_tab, 
            width=300, 
            placeholder_text="Enter your username"
        )
        self.username_entry.pack(pady=(0, 15))
        
        self.password_label = ctk.CTkLabel(
            self.login_tab, 
            text="Password:", 
            font=ctk.CTkFont(size=14)
        )
        self.password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.password_entry = ctk.CTkEntry(
            self.login_tab, 
            width=300, 
            placeholder_text="Enter your password", 
            show="•"
        )
        self.password_entry.pack(pady=(0, 20))
        
        self.login_button = ctk.CTkButton(
            self.login_tab, 
            text="Login", 
            width=300, 
            command=self.login
        )
        self.login_button.pack(pady=(10, 0))
        
        self.login_status = ctk.CTkLabel(
            self.login_tab, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.login_status.pack(pady=(10, 0))
        
        # Register tab
        self.reg_username_label = ctk.CTkLabel(
            self.register_tab, 
            text="Username:", 
            font=ctk.CTkFont(size=14)
        )
        self.reg_username_label.pack(anchor=tk.W, pady=(20, 5))
        
        self.reg_username_entry = ctk.CTkEntry(
            self.register_tab, 
            width=300, 
            placeholder_text="Choose a username"
        )
        self.reg_username_entry.pack(pady=(0, 15))
        
        self.reg_email_label = ctk.CTkLabel(
            self.register_tab, 
            text="Email (optional):", 
            font=ctk.CTkFont(size=14)
        )
        self.reg_email_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.reg_email_entry = ctk.CTkEntry(
            self.register_tab, 
            width=300, 
            placeholder_text="Enter your email"
        )
        self.reg_email_entry.pack(pady=(0, 15))
        
        self.reg_password_label = ctk.CTkLabel(
            self.register_tab, 
            text="Password:", 
            font=ctk.CTkFont(size=14)
        )
        self.reg_password_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.reg_password_entry = ctk.CTkEntry(
            self.register_tab, 
            width=300, 
            placeholder_text="Choose a password", 
            show="•"
        )
        self.reg_password_entry.pack(pady=(0, 15))
        
        self.reg_confirm_label = ctk.CTkLabel(
            self.register_tab, 
            text="Confirm Password:", 
            font=ctk.CTkFont(size=14)
        )
        self.reg_confirm_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.reg_confirm_entry = ctk.CTkEntry(
            self.register_tab, 
            width=300, 
            placeholder_text="Confirm your password", 
            show="•"
        )
        self.reg_confirm_entry.pack(pady=(0, 20))
        
        self.register_button = ctk.CTkButton(
            self.register_tab, 
            text="Register", 
            width=300, 
            command=self.register
        )
        self.register_button.pack(pady=(10, 0))
        
        self.register_status = ctk.CTkLabel(
            self.register_tab, 
            text="", 
            font=ctk.CTkFont(size=12),
            text_color="red"
        )
        self.register_status.pack(pady=(10, 0))
        
        # Set default tab
        self.tab_view.set("Login")
        
        # Bind Enter key to login/register
        self.username_entry.bind("<Return>", lambda event: self.password_entry.focus_set())
        self.password_entry.bind("<Return>", lambda event: self.login())
        self.reg_username_entry.bind("<Return>", lambda event: self.reg_email_entry.focus_set())
        self.reg_email_entry.bind("<Return>", lambda event: self.reg_password_entry.focus_set())
        self.reg_password_entry.bind("<Return>", lambda event: self.reg_confirm_entry.focus_set())
        self.reg_confirm_entry.bind("<Return>", lambda event: self.register())
    
    def login(self):
        """
        Handle login button click
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Validate input
        if not username or not password:
            self.login_status.configure(text="Please enter username and password")
            return
        
        # Attempt login
        success, message = self.auth.login(username, password)
        
        if success:
            # Call the success callback
            if self.on_login_success:
                self.on_login_success(username)
            
            # Close the login window
            self.destroy()
        else:
            # Show error message
            self.login_status.configure(text=message)
    
    def register(self):
        """
        Handle register button click
        """
        username = self.reg_username_entry.get()
        email = self.reg_email_entry.get()
        password = self.reg_password_entry.get()
        confirm = self.reg_confirm_entry.get()
        
        # Validate input
        if not username or not password:
            self.register_status.configure(text="Please enter username and password")
            return
        
        if password != confirm:
            self.register_status.configure(text="Passwords do not match")
            return
        
        # Attempt registration
        success, message = self.auth.register(username, password, email)
        
        if success:
            # Show success message
            self.register_status.configure(text_color="green")
            self.register_status.configure(text="Registration successful! You can now login.")
            
            # Clear fields
            self.reg_username_entry.delete(0, tk.END)
            self.reg_email_entry.delete(0, tk.END)
            self.reg_password_entry.delete(0, tk.END)
            self.reg_confirm_entry.delete(0, tk.END)
            
            # Switch to login tab
            self.tab_view.set("Login")
        else:
            # Show error message
            self.register_status.configure(text=message)
