import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import threading

# Import audio processing module
from app.audio.transcription import transcribe_audio

class TranscriptionPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Transcription panel header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Voice Note Transcription", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Upload section
        self.upload_frame = ctk.CTkFrame(self)
        self.upload_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.upload_frame.grid_columnconfigure(1, weight=1)
        
        self.upload_label = ctk.CTkLabel(
            self.upload_frame,
            text="Upload Voice Note:",
            font=ctk.CTkFont(size=16)
        )
        self.upload_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")
        
        self.file_path_var = ctk.StringVar()
        self.file_path_entry = ctk.CTkEntry(
            self.upload_frame,
            textvariable=self.file_path_var,
            width=400
        )
        self.file_path_entry.grid(row=0, column=1, padx=(0, 10), pady=20, sticky="ew")
        
        self.browse_button = ctk.CTkButton(
            self.upload_frame,
            text="Browse",
            command=self.browse_file
        )
        self.browse_button.grid(row=0, column=2, padx=(0, 20), pady=20)
        
        # Options frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        # Transcription type
        self.transcription_type_label = ctk.CTkLabel(
            self.options_frame,
            text="Transcription Type:",
            font=ctk.CTkFont(size=14)
        )
        self.transcription_type_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.transcription_type_var = ctk.StringVar(value="cleaned")
        self.verbatim_radio = ctk.CTkRadioButton(
            self.options_frame,
            text="Verbatim",
            variable=self.transcription_type_var,
            value="verbatim"
        )
        self.verbatim_radio.grid(row=1, column=0, padx=40, pady=(10, 0), sticky="w")
        
        self.cleaned_radio = ctk.CTkRadioButton(
            self.options_frame,
            text="Cleaned",
            variable=self.transcription_type_var,
            value="cleaned"
        )
        self.cleaned_radio.grid(row=1, column=1, padx=20, pady=(10, 0), sticky="w")
        
        # Proofreading option
        self.proofreading_var = ctk.BooleanVar(value=True)
        self.proofreading_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="Enable Proofreading",
            variable=self.proofreading_var
        )
        self.proofreading_checkbox.grid(row=2, column=0, padx=20, pady=(20, 20), sticky="w")
        
        # Transcribe button
        self.transcribe_button = ctk.CTkButton(
            self.options_frame,
            text="Transcribe",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.start_transcription
        )
        self.transcribe_button.grid(row=2, column=1, padx=20, pady=(20, 20), sticky="e")
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Transcription Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Transcription text area
        self.transcription_textbox = ctk.CTkTextbox(self.results_frame, height=300)
        self.transcription_textbox.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        
        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.results_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Action buttons
        self.action_frame = ctk.CTkFrame(self.results_frame)
        self.action_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.copy_button = ctk.CTkButton(
            self.action_frame,
            text="Copy to Clipboard",
            command=self.copy_to_clipboard
        )
        self.copy_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.save_button = ctk.CTkButton(
            self.action_frame,
            text="Save as Document",
            command=self.save_as_document
        )
        self.save_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.export_button = ctk.CTkButton(
            self.action_frame,
            text="Export as Text",
            command=self.export_as_text
        )
        self.export_button.grid(row=0, column=2, padx=10, pady=10)
    
    def browse_file(self):
        filetypes = [
            ("Audio Files", "*.mp3 *.m4a *.wav *.ogg"),
            ("All Files", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)
    
    def start_transcription(self):
        file_path = self.file_path_var.get()
        if not file_path or not os.path.exists(file_path):
            self.status_var.set("Error: Please select a valid audio file")
            return
        
        # Update UI
        self.status_var.set("Transcribing... Please wait")
        self.transcribe_button.configure(state="disabled")
        self.transcription_textbox.delete("0.0", "end")
        
        # Get options
        transcription_type = self.transcription_type_var.get()
        proofreading = self.proofreading_var.get()
        
        # Start transcription in a separate thread
        threading.Thread(
            target=self.perform_transcription,
            args=(file_path, transcription_type, proofreading),
            daemon=True
        ).start()
    
    def perform_transcription(self, file_path, transcription_type, proofreading):
        try:
            # Call the transcription function from the audio module
            result = transcribe_audio(file_path, transcription_type, proofreading)
            
            # Update UI with results
            self.update_transcription_results(result)
        except Exception as e:
            # Handle errors
            self.status_var.set(f"Error: {str(e)}")
        finally:
            # Re-enable the transcribe button
            self.transcribe_button.configure(state="normal")
    
    def update_transcription_results(self, result):
        # Update the text box with transcription results
        self.transcription_textbox.delete("0.0", "end")
        self.transcription_textbox.insert("0.0", result)
        
        # Update status
        self.status_var.set("Transcription completed successfully")
    
    def copy_to_clipboard(self):
        text = self.transcription_textbox.get("0.0", "end")
        self.clipboard_clear()
        self.clipboard_append(text)
        self.status_var.set("Copied to clipboard")
    
    def save_as_document(self):
        # This would open the document panel with the transcription text
        text = self.transcription_textbox.get("0.0", "end-1c")
        if text.strip():
            self.status_var.set("Saving as document...")
            # Here we would call a function to save as document
            # For now, just update the status
            self.status_var.set("Document saved successfully")
        else:
            self.status_var.set("Error: No transcription to save")
    
    def export_as_text(self):
        text = self.transcription_textbox.get("0.0", "end-1c")
        if text.strip():
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if file_path:
                try:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(text)
                    self.status_var.set(f"Exported to {os.path.basename(file_path)}")
                except Exception as e:
                    self.status_var.set(f"Error exporting: {str(e)}")
        else:
            self.status_var.set("Error: No transcription to export")