import os
import tkinter as tk
from dotenv import load_dotenv
import customtkinter as ctk

# Import application modules
from app.ui.dashboard import Dashboard
from app.ui.transcription_panel import TranscriptionPanel
from app.ui.chat_panel import ChatPanel
from app.ui.document_panel import DocumentPanel
from app.ui.automation_panel import AutomationPanel
from app.ui.login_screen import LoginScreen
from app.auth.authentication import Authentication

# Load environment variables
load_dotenv()

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class WhatsDocApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("WhatsDoc Automator")
        self.geometry("1100x700")
        self.minsize(800, 600)
        
        # Initialize authentication
        self.auth = Authentication()
        self.current_user = None
        
        # Show login screen first
        self.withdraw()  # Hide main window until login
        self.after(100, self.show_login)
    
    def show_login(self):
        """
        Show login screen
        """
        login_screen = LoginScreen(self, on_login_success=self.on_login_success)
        self.wait_window(login_screen)  # Wait for login window to close
        
        # If no user is logged in after login window closes, exit the app
        if not self.current_user:
            self.destroy()
    
    def on_login_success(self, username):
        """
        Called when login is successful
        """
        self.current_user = username
        self.initialize_ui()
        self.deiconify()  # Show main window
    
    def initialize_ui(self):
        """
        Initialize the main UI after successful login
        """
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        # App logo/title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="WhatsDoc", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # User info
        self.user_label = ctk.CTkLabel(self.sidebar_frame, text=f"User: {self.current_user}", font=ctk.CTkFont(size=12))
        self.user_label.grid(row=0, column=0, padx=20, pady=(50, 0))
        
        # Sidebar buttons
        self.dashboard_button = ctk.CTkButton(self.sidebar_frame, text="Dashboard", command=self.show_dashboard)
        self.dashboard_button.grid(row=1, column=0, padx=20, pady=10)
        
        self.transcription_button = ctk.CTkButton(self.sidebar_frame, text="Voice Transcription", command=self.show_transcription)
        self.transcription_button.grid(row=2, column=0, padx=20, pady=10)
        
        self.chat_button = ctk.CTkButton(self.sidebar_frame, text="Chat Conversion", command=self.show_chat)
        self.chat_button.grid(row=3, column=0, padx=20, pady=10)
        
        self.document_button = ctk.CTkButton(self.sidebar_frame, text="Documents", command=self.show_documents)
        self.document_button.grid(row=4, column=0, padx=20, pady=10)
        
        self.automation_button = ctk.CTkButton(self.sidebar_frame, text="Automation", command=self.show_automation)
        self.automation_button.grid(row=5, column=0, padx=20, pady=10)
        
        # Logout button
        self.logout_button = ctk.CTkButton(self.sidebar_frame, text="Logout", command=self.logout, fg_color="gray")
        self.logout_button.grid(row=6, column=0, padx=20, pady=(50, 10))
        
        # Create main frame for content
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, rowspan=4, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)
        
        # Initialize panels (frames)
        self.dashboard = Dashboard(self.main_frame)
        self.transcription_panel = TranscriptionPanel(self.main_frame)
        self.chat_panel = ChatPanel(self.main_frame)
        self.document_panel = DocumentPanel(self.main_frame)
        self.automation_panel = AutomationPanel(self.main_frame)
        
        # Show dashboard by default
        self.show_dashboard()
    
    def logout(self):
        """
        Logout the current user
        """
        self.auth.logout()
        self.current_user = None
        
        # Clear UI
        for widget in self.winfo_children():
            widget.destroy()
        
        # Show login screen again
        self.withdraw()
        self.after(100, self.show_login)
    
    def show_dashboard(self):
        self.hide_all_frames()
        self.dashboard.grid(row=0, column=0, sticky="nsew")
        self.dashboard_button.configure(fg_color=["#3a7ebf", "#1f538d"])
    
    def show_transcription(self):
        self.hide_all_frames()
        self.transcription_panel.grid(row=0, column=0, sticky="nsew")
        self.transcription_button.configure(fg_color=["#3a7ebf", "#1f538d"])
    
    def show_chat(self):
        self.hide_all_frames()
        self.chat_panel.grid(row=0, column=0, sticky="nsew")
        self.chat_button.configure(fg_color=["#3a7ebf", "#1f538d"])
    
    def show_documents(self):
        self.hide_all_frames()
        self.document_panel.grid(row=0, column=0, sticky="nsew")
        self.document_button.configure(fg_color=["#3a7ebf", "#1f538d"])
    
    def show_automation(self):
        self.hide_all_frames()
        self.automation_panel.grid(row=0, column=0, sticky="nsew")
        self.automation_button.configure(fg_color=["#3a7ebf", "#1f538d"])
    
    def hide_all_frames(self):
        self.dashboard.grid_forget()
        self.transcription_panel.grid_forget()
        self.chat_panel.grid_forget()
        self.document_panel.grid_forget()
        self.automation_panel.grid_forget()
        
        # Reset button colors
        self.dashboard_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.transcription_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.chat_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.document_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])
        self.automation_button.configure(fg_color=["#3B8ED0", "#1F6AA5"])

if __name__ == "__main__":
    app = WhatsDocApp()
    app.mainloop()
