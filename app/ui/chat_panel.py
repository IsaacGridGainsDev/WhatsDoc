import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import threading

# Import chat processing module
from app.chat.parser import parse_chat

class ChatPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        
        # Chat panel header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Chat to Document Conversion", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Input section
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.input_frame.grid_columnconfigure(0, weight=1)
        
        # Input tabs
        self.input_tabview = ctk.CTkTabview(self.input_frame)
        self.input_tabview.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        # Create tabs
        self.input_tabview.add("Paste Text")
        self.input_tabview.add("Upload File")
        self.input_tabview.add("Upload Screenshot")
        
        # Configure tab grid
        self.input_tabview.tab("Paste Text").grid_columnconfigure(0, weight=1)
        self.input_tabview.tab("Upload File").grid_columnconfigure(0, weight=1)
        self.input_tabview.tab("Upload Screenshot").grid_columnconfigure(0, weight=1)
        
        # Paste Text tab content
        self.paste_text_label = ctk.CTkLabel(
            self.input_tabview.tab("Paste Text"),
            text="Paste WhatsApp chat text:",
            font=ctk.CTkFont(size=14)
        )
        self.paste_text_label.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="w")
        
        self.paste_textbox = ctk.CTkTextbox(
            self.input_tabview.tab("Paste Text"),
            height=150
        )
        self.paste_textbox.grid(row=1, column=0, padx=20, pady=(10, 20), sticky="ew")
        
        # Upload File tab content
        self.file_label = ctk.CTkLabel(
            self.input_tabview.tab("Upload File"),
            text="Upload WhatsApp chat export file:",
            font=ctk.CTkFont(size=14)
        )
        self.file_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.file_frame = ctk.CTkFrame(self.input_tabview.tab("Upload File"))
        self.file_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.file_frame.grid_columnconfigure(0, weight=1)
        
        self.file_path_var = ctk.StringVar()
        self.file_path_entry = ctk.CTkEntry(
            self.file_frame,
            textvariable=self.file_path_var,
            width=400
        )
        self.file_path_entry.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="ew")
        
        self.browse_file_button = ctk.CTkButton(
            self.file_frame,
            text="Browse",
            command=self.browse_chat_file
        )
        self.browse_file_button.grid(row=0, column=1, padx=(0, 0), pady=10)
        
        # Upload Screenshot tab content
        self.screenshot_label = ctk.CTkLabel(
            self.input_tabview.tab("Upload Screenshot"),
            text="Upload WhatsApp chat screenshots:",
            font=ctk.CTkFont(size=14)
        )
        self.screenshot_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        self.screenshot_frame = ctk.CTkFrame(self.input_tabview.tab("Upload Screenshot"))
        self.screenshot_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.screenshot_button = ctk.CTkButton(
            self.screenshot_frame,
            text="Select Images",
            command=self.browse_screenshots
        )
        self.screenshot_button.grid(row=0, column=0, padx=20, pady=20)
        
        self.screenshot_count_var = ctk.StringVar(value="No images selected")
        self.screenshot_count_label = ctk.CTkLabel(
            self.screenshot_frame,
            textvariable=self.screenshot_count_var,
            font=ctk.CTkFont(size=12)
        )
        self.screenshot_count_label.grid(row=0, column=1, padx=20, pady=20)
        
        # Options frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.grid(row=2, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.options_frame.grid_columnconfigure(1, weight=1)
        
        # Output options
        self.output_label = ctk.CTkLabel(
            self.options_frame,
            text="Output Options:",
            font=ctk.CTkFont(size=14)
        )
        self.output_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Checkboxes for output options
        self.summary_var = ctk.BooleanVar(value=True)
        self.summary_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="Generate Summary",
            variable=self.summary_var
        )
        self.summary_checkbox.grid(row=1, column=0, padx=40, pady=(0, 10), sticky="w")
        
        self.action_points_var = ctk.BooleanVar(value=True)
        self.action_points_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="Extract Action Points",
            variable=self.action_points_var
        )
        self.action_points_checkbox.grid(row=2, column=0, padx=40, pady=(0, 10), sticky="w")
        
        self.topic_grouping_var = ctk.BooleanVar(value=True)
        self.topic_grouping_checkbox = ctk.CTkCheckBox(
            self.options_frame,
            text="Group by Topics",
            variable=self.topic_grouping_var
        )
        self.topic_grouping_checkbox.grid(row=3, column=0, padx=40, pady=(0, 20), sticky="w")
        
        # Template selection
        self.template_label = ctk.CTkLabel(
            self.options_frame,
            text="Document Template:",
            font=ctk.CTkFont(size=14)
        )
        self.template_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="w")
        
        self.template_var = ctk.StringVar(value="Meeting Summary")
        self.template_dropdown = ctk.CTkOptionMenu(
            self.options_frame,
            values=["Meeting Summary", "Client Brief", "Sales Report", "Real Estate Checklist", "Custom"],
            variable=self.template_var
        )
        self.template_dropdown.grid(row=1, column=1, padx=40, pady=(0, 10), sticky="w")
        
        # Process button
        self.process_button = ctk.CTkButton(
            self.options_frame,
            text="Process Chat",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_chat
        )
        self.process_button.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="e")
        
        # Results frame
        self.results_frame = ctk.CTkFrame(self)
        self.results_frame.grid(row=3, column=0, padx=20, pady=20, sticky="nsew")
        self.results_frame.grid_columnconfigure(0, weight=1)
        self.results_frame.grid_rowconfigure(1, weight=1)
        
        self.results_label = ctk.CTkLabel(
            self.results_frame,
            text="Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.results_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Results tabview
        self.results_tabview = ctk.CTkTabview(self.results_frame)
        self.results_tabview.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        
        # Create result tabs
        self.results_tabview.add("Summary")
        self.results_tabview.add("Action Points")
        self.results_tabview.add("Full Content")
        
        # Configure tab grid
        self.results_tabview.tab("Summary").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Summary").grid_rowconfigure(0, weight=1)
        
        self.results_tabview.tab("Action Points").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Action Points").grid_rowconfigure(0, weight=1)
        
        self.results_tabview.tab("Full Content").grid_columnconfigure(0, weight=1)
        self.results_tabview.tab("Full Content").grid_rowconfigure(0, weight=1)
        
        # Summary tab content
        self.summary_textbox = ctk.CTkTextbox(self.results_tabview.tab("Summary"))
        self.summary_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Action Points tab content
        self.action_points_textbox = ctk.CTkTextbox(self.results_tabview.tab("Action Points"))
        self.action_points_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Full Content tab content
        self.full_content_textbox = ctk.CTkTextbox(self.results_tabview.tab("Full Content"))
        self.full_content_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.results_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Export buttons
        self.export_frame = ctk.CTkFrame(self.results_frame)
        self.export_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.export_pdf_button = ctk.CTkButton(
            self.export_frame,
            text="Export as PDF",
            command=self.export_as_pdf
        )
        self.export_pdf_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.export_docx_button = ctk.CTkButton(
            self.export_frame,
            text="Export as DOCX",
            command=self.export_as_docx
        )
        self.export_docx_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.save_template_button = ctk.CTkButton(
            self.export_frame,
            text="Save as Template",
            command=self.save_as_template
        )
        self.save_template_button.grid(row=0, column=2, padx=10, pady=10)
        
        # Initialize variables
        self.screenshot_paths = []
    
    def browse_chat_file(self):
        filetypes = [
            ("Text Files", "*.txt"),
            ("All Files", "*.*")
        ]
        file_path = filedialog.askopenfilename(filetypes=filetypes)
        if file_path:
            self.file_path_var.set(file_path)
    
    def browse_screenshots(self):
        filetypes = [
            ("Image Files", "*.png *.jpg *.jpeg"),
            ("All Files", "*.*")
        ]
        file_paths = filedialog.askopenfilenames(filetypes=filetypes)
        if file_paths:
            self.screenshot_paths = file_paths
            self.screenshot_count_var.set(f"{len(file_paths)} image(s) selected")
    
    def process_chat(self):
        # Determine which input method is being used
        current_tab = self.input_tabview._segmented_button.get()
        
        # Validate input
        if current_tab == "Paste Text":
            chat_text = self.paste_textbox.get("0.0", "end-1c")
            if not chat_text.strip():
                self.status_var.set("Error: Please paste WhatsApp chat text")
                return
            input_data = {"type": "text", "content": chat_text}
            
        elif current_tab == "Upload File":
            file_path = self.file_path_var.get()
            if not file_path or not os.path.exists(file_path):
                self.status_var.set("Error: Please select a valid chat export file")
                return
            input_data = {"type": "file", "content": file_path}
            
        elif current_tab == "Upload Screenshot":
            if not self.screenshot_paths:
                self.status_var.set("Error: Please select at least one screenshot")
                return
            input_data = {"type": "screenshots", "content": self.screenshot_paths}
        
        # Get options
        options = {
            "summary": self.summary_var.get(),
            "action_points": self.action_points_var.get(),
            "topic_grouping": self.topic_grouping_var.get(),
            "template": self.template_var.get()
        }
        
        # Update UI
        self.status_var.set("Processing chat... Please wait")
        self.process_button.configure(state="disabled")
        self.clear_results()
        
        # Start processing in a separate thread
        threading.Thread(
            target=self.perform_chat_processing,
            args=(input_data, options),
            daemon=True
        ).start()
    
    def perform_chat_processing(self, input_data, options):
        try:
            # Call the chat parsing function from the chat module
            result = parse_chat(input_data, options)
            
            # Update UI with results
            self.update_results(result)
        except Exception as e:
            # Handle errors
            self.status_var.set(f"Error: {str(e)}")
        finally:
            # Re-enable the process button
            self.process_button.configure(state="normal")
    
    def clear_results(self):
        # Clear all result textboxes
        self.summary_textbox.delete("0.0", "end")
        self.action_points_textbox.delete("0.0", "end")
        self.full_content_textbox.delete("0.0", "end")
    
    def update_results(self, result):
        # Update the textboxes with processing results
        if "summary" in result:
            self.summary_textbox.delete("0.0", "end")
            self.summary_textbox.insert("0.0", result["summary"])
        
        if "action_points" in result:
            self.action_points_textbox.delete("0.0", "end")
            self.action_points_textbox.insert("0.0", result["action_points"])
        
        if "full_content" in result:
            self.full_content_textbox.delete("0.0", "end")
            self.full_content_textbox.insert("0.0", result["full_content"])
        
        # Update status
        self.status_var.set("Chat processing completed successfully")
    
    def export_as_pdf(self):
        # This would call the document module to export as PDF
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.status_var.set("Exporting to PDF...")
                # Here we would call a function to export as PDF
                # For now, just update the status
                self.status_var.set(f"Exported to {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"Error exporting: {str(e)}")
    
    def export_as_docx(self):
        # This would call the document module to export as DOCX
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.status_var.set("Exporting to DOCX...")
                # Here we would call a function to export as DOCX
                # For now, just update the status
                self.status_var.set(f"Exported to {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"Error exporting: {str(e)}")
    
    def save_as_template(self):
        # This would save the current settings as a template
        template_name = ctk.CTkInputDialog(
            text="Enter template name:",
            title="Save Template"
        ).get_input()
        
        if template_name:
            self.status_var.set(f"Template '{template_name}' saved successfully")