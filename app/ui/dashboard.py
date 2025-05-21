import os
import customtkinter as ctk
from PIL import Image
import datetime

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Dashboard header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Dashboard", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Stats summary
        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="new")
        self.stats_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Transcription stats
        self.transcription_frame = ctk.CTkFrame(self.stats_frame)
        self.transcription_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        self.transcription_label = ctk.CTkLabel(
            self.transcription_frame,
            text="Voice Transcriptions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.transcription_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.transcription_count = ctk.CTkLabel(
            self.transcription_frame,
            text="0",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.transcription_count.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Chat conversion stats
        self.chat_frame = ctk.CTkFrame(self.stats_frame)
        self.chat_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.chat_label = ctk.CTkLabel(
            self.chat_frame,
            text="Chat Conversions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.chat_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.chat_count = ctk.CTkLabel(
            self.chat_frame,
            text="0",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.chat_count.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Document stats
        self.document_frame = ctk.CTkFrame(self.stats_frame)
        self.document_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        
        self.document_label = ctk.CTkLabel(
            self.document_frame,
            text="Documents Created",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.document_label.grid(row=0, column=0, padx=20, pady=(10, 5), sticky="w")
        
        self.document_count = ctk.CTkLabel(
            self.document_frame,
            text="0",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.document_count.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Recent activity
        self.activity_frame = ctk.CTkFrame(self)
        self.activity_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.activity_frame.grid_columnconfigure(0, weight=1)
        self.activity_frame.grid_rowconfigure(1, weight=1)
        
        self.activity_label = ctk.CTkLabel(
            self.activity_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.activity_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Activity list (scrollable)
        self.activity_list_frame = ctk.CTkScrollableFrame(self.activity_frame)
        self.activity_list_frame.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="nsew")
        self.activity_list_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder for activity items
        self.create_activity_items()
    
    def create_activity_items(self):
        # This would normally be populated from a database or file
        # For now, we'll create some placeholder items
        placeholder_activities = [
            {"type": "transcription", "name": "Meeting with Client", "date": "2025-05-20", "status": "Completed"},
            {"type": "chat", "name": "Project Discussion", "date": "2025-05-19", "status": "Completed"},
            {"type": "document", "name": "Sales Report", "date": "2025-05-18", "status": "Completed"},
        ]
        
        for i, activity in enumerate(placeholder_activities):
            activity_item = self.create_activity_item(activity, i)
            activity_item.grid(row=i, column=0, padx=5, pady=5, sticky="ew")
    
    def create_activity_item(self, activity, index):
        item_frame = ctk.CTkFrame(self.activity_list_frame)
        item_frame.grid_columnconfigure((1, 2), weight=1)
        
        # Icon based on activity type
        icon_label = ctk.CTkLabel(
            item_frame,
            text=self.get_icon_for_type(activity["type"]),
            font=ctk.CTkFont(size=16)
        )
        icon_label.grid(row=0, column=0, padx=10, pady=10)
        
        # Activity name
        name_label = ctk.CTkLabel(
            item_frame,
            text=activity["name"],
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        
        # Activity date
        date_label = ctk.CTkLabel(
            item_frame,
            text=activity["date"],
            font=ctk.CTkFont(size=12)
        )
        date_label.grid(row=0, column=2, padx=10, pady=10)
        
        # Activity status
        status_label = ctk.CTkLabel(
            item_frame,
            text=activity["status"],
            font=ctk.CTkFont(size=12),
            text_color="green" if activity["status"] == "Completed" else "orange"
        )
        status_label.grid(row=0, column=3, padx=10, pady=10)
        
        # View button
        view_button = ctk.CTkButton(
            item_frame,
            text="View",
            width=60,
            command=lambda: self.view_activity(activity)
        )
        view_button.grid(row=0, column=4, padx=10, pady=10)
        
        return item_frame
    
    def get_icon_for_type(self, activity_type):
        # Simple text icons as placeholders
        # In a real app, you might use actual icons
        icons = {
            "transcription": "🎤",
            "chat": "💬",
            "document": "📄"
        }
        return icons.get(activity_type, "📋")
    
    def view_activity(self, activity):
        # This would open the activity in the appropriate panel
        print(f"Viewing activity: {activity['name']}")
    
    def update_stats(self, transcription_count=0, chat_count=0, document_count=0):
        # Update the stats counters
        self.transcription_count.configure(text=str(transcription_count))
        self.chat_count.configure(text=str(chat_count))
        self.document_count.configure(text=str(document_count))