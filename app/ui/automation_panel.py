import os
import json
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image

class AutomationPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Automation panel header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Automation Panel", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Presets section
        self.presets_frame = ctk.CTkFrame(self)
        self.presets_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.presets_frame.grid_columnconfigure(0, weight=1)
        
        self.presets_label = ctk.CTkLabel(
            self.presets_frame,
            text="Saved Presets",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.presets_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Preset list
        self.preset_listbox_frame = ctk.CTkFrame(self.presets_frame)
        self.preset_listbox_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.preset_listbox_frame.grid_columnconfigure(0, weight=1)
        
        self.preset_listbox = ctk.CTkTextbox(self.preset_listbox_frame, height=150)
        self.preset_listbox.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")
        
        # Preset buttons
        self.preset_buttons_frame = ctk.CTkFrame(self.presets_frame)
        self.preset_buttons_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.load_preset_button = ctk.CTkButton(
            self.preset_buttons_frame,
            text="Load Preset",
            command=self.load_preset
        )
        self.load_preset_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.delete_preset_button = ctk.CTkButton(
            self.preset_buttons_frame,
            text="Delete Preset",
            command=self.delete_preset
        )
        self.delete_preset_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.create_preset_button = ctk.CTkButton(
            self.preset_buttons_frame,
            text="Create New Preset",
            command=self.create_preset
        )
        self.create_preset_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Automation settings
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.settings_frame.grid_columnconfigure(0, weight=1)
        
        self.settings_label = ctk.CTkLabel(
            self.settings_frame,
            text="Automation Settings",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.settings_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Auto-run settings
        self.autorun_frame = ctk.CTkFrame(self.settings_frame)
        self.autorun_frame.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="ew")
        self.autorun_frame.grid_columnconfigure(1, weight=1)
        
        self.autorun_label = ctk.CTkLabel(
            self.autorun_frame,
            text="Auto-Run Settings:",
            font=ctk.CTkFont(size=14)
        )
        self.autorun_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Checkboxes for auto-run options
        self.auto_transcribe_var = ctk.BooleanVar(value=False)
        self.auto_transcribe_checkbox = ctk.CTkCheckBox(
            self.autorun_frame,
            text="Auto-Transcribe after Upload",
            variable=self.auto_transcribe_var
        )
        self.auto_transcribe_checkbox.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="w")
        
        self.auto_summarize_var = ctk.BooleanVar(value=False)
        self.auto_summarize_checkbox = ctk.CTkCheckBox(
            self.autorun_frame,
            text="Auto-Summarize after Processing",
            variable=self.auto_summarize_var
        )
        self.auto_summarize_checkbox.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="w")
        
        self.auto_export_var = ctk.BooleanVar(value=False)
        self.auto_export_checkbox = ctk.CTkCheckBox(
            self.autorun_frame,
            text="Auto-Export after Completion",
            variable=self.auto_export_var
        )
        self.auto_export_checkbox.grid(row=3, column=0, padx=40, pady=(0, 10), sticky="w")
        
        # Export format
        self.export_format_label = ctk.CTkLabel(
            self.autorun_frame,
            text="Default Export Format:",
            font=ctk.CTkFont(size=14)
        )
        self.export_format_label.grid(row=1, column=1, padx=20, pady=(0, 10), sticky="w")
        
        self.export_format_var = ctk.StringVar(value="PDF")
        self.export_format_dropdown = ctk.CTkOptionMenu(
            self.autorun_frame,
            values=["PDF", "DOCX", "TXT"],
            variable=self.export_format_var
        )
        self.export_format_dropdown.grid(row=2, column=1, padx=40, pady=(0, 10), sticky="w")
        
        # Export history
        self.history_frame = ctk.CTkFrame(self.settings_frame)
        self.history_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.history_frame.grid_columnconfigure(0, weight=1)
        
        self.history_label = ctk.CTkLabel(
            self.history_frame,
            text="Export History",
            font=ctk.CTkFont(size=14)
        )
        self.history_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # History list
        self.history_listbox = ctk.CTkTextbox(self.history_frame, height=150)
        self.history_listbox.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        
        # History buttons
        self.history_buttons_frame = ctk.CTkFrame(self.history_frame)
        self.history_buttons_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.open_export_button = ctk.CTkButton(
            self.history_buttons_frame,
            text="Open Selected",
            command=self.open_export
        )
        self.open_export_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.export_archive_button = ctk.CTkButton(
            self.history_buttons_frame,
            text="Export Archive",
            command=self.export_archive
        )
        self.export_archive_button.grid(row=0, column=1, padx=10, pady=10)
        
        # Save settings button
        self.save_settings_button = ctk.CTkButton(
            self.settings_frame,
            text="Save Settings",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.save_settings
        )
        self.save_settings_button.grid(row=3, column=0, padx=20, pady=(20, 20), sticky="e")
        
        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.settings_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Load presets and history
        self.load_presets()
        self.load_history()
    
    def load_presets(self):
        # This would load presets from a file
        # For now, add some placeholder presets
        presets = [
            "Real Estate Agent",
            "Course Creator",
            "Project Manager"
        ]
        
        # Display presets in the listbox
        self.preset_listbox.delete("0.0", "end")
        for preset in presets:
            self.preset_listbox.insert("end", f"{preset}\n")
    
    def load_history(self):
        # This would load export history from a file
        # For now, add some placeholder history items
        history_items = [
            "Meeting_Summary_2025-05-15.pdf",
            "Client_Brief_2025-05-14.docx",
            "Sales_Report_2025-05-10.pdf"
        ]
        
        # Display history in the listbox
        self.history_listbox.delete("0.0", "end")
        for item in history_items:
            self.history_listbox.insert("end", f"{item}\n")
    
    def load_preset(self):
        # This would load the selected preset
        # For now, just update the status
        self.status_var.set("Preset loaded successfully")
    
    def delete_preset(self):
        # This would delete the selected preset
        # For now, just update the status
        self.status_var.set("Preset deleted successfully")
    
    def create_preset(self):
        # This would create a new preset
        preset_name = ctk.CTkInputDialog(
            text="Enter preset name:",
            title="Create Preset"
        ).get_input()
        
        if preset_name:
            self.status_var.set(f"Preset '{preset_name}' created successfully")
    
    def open_export(self):
        # This would open the selected export file
        # For now, just update the status
        self.status_var.set("Opening export file...")
    
    def export_archive(self):
        # This would export all history as an archive
        file_path = filedialog.asksaveasfilename(
            defaultextension=".zip",
            filetypes=[("ZIP Files", "*.zip"), ("All Files", "*.*")]
        )
        if file_path:
            self.status_var.set(f"Archive exported to {os.path.basename(file_path)}")
    
    def save_settings(self):
        # This would save the automation settings
        settings = {
            "auto_transcribe": self.auto_transcribe_var.get(),
            "auto_summarize": self.auto_summarize_var.get(),
            "auto_export": self.auto_export_var.get(),
            "export_format": self.export_format_var.get()
        }
        
        # In a real app, this would save to a file
        # For now, just update the status
        self.status_var.set("Settings saved successfully")