import os
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import threading

# Import document generation module
from app.document.generator import generate_document

class DocumentPanel(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        # Document panel header
        self.header_frame = ctk.CTkFrame(self)
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        self.header_label = ctk.CTkLabel(
            self.header_frame, 
            text="Document Templates", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.grid(row=0, column=0, padx=20, pady=(10, 10), sticky="w")
        
        # Templates section
        self.templates_frame = ctk.CTkFrame(self)
        self.templates_frame.grid(row=1, column=0, padx=20, pady=(20, 0), sticky="ew")
        self.templates_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        
        # Template cards
        self.create_template_cards()
        
        # Document editor frame
        self.editor_frame = ctk.CTkFrame(self)
        self.editor_frame.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.editor_frame.grid_rowconfigure(1, weight=1)
        
        self.editor_label = ctk.CTkLabel(
            self.editor_frame,
            text="Document Editor",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.editor_label.grid(row=0, column=0, padx=20, pady=(10, 0), sticky="w")
        
        # Document editor
        self.editor_textbox = ctk.CTkTextbox(self.editor_frame)
        self.editor_textbox.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="nsew")
        
        # Status label
        self.status_var = ctk.StringVar(value="Ready")
        self.status_label = ctk.CTkLabel(
            self.editor_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=12)
        )
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="w")
        
        # Action buttons
        self.action_frame = ctk.CTkFrame(self.editor_frame)
        self.action_frame.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="ew")
        
        self.export_pdf_button = ctk.CTkButton(
            self.action_frame,
            text="Export as PDF",
            command=self.export_as_pdf
        )
        self.export_pdf_button.grid(row=0, column=0, padx=10, pady=10)
        
        self.export_docx_button = ctk.CTkButton(
            self.action_frame,
            text="Export as DOCX",
            command=self.export_as_docx
        )
        self.export_docx_button.grid(row=0, column=1, padx=10, pady=10)
        
        self.save_template_button = ctk.CTkButton(
            self.action_frame,
            text="Save as Template",
            command=self.save_as_template
        )
        self.save_template_button.grid(row=0, column=2, padx=10, pady=10)
    
    def create_template_cards(self):
        # Template data
        templates = [
            {
                "name": "Meeting Summary",
                "description": "Structured summary of meeting discussions, decisions, and action items",
                "icon": "📝"
            },
            {
                "name": "Client Brief",
                "description": "Detailed overview of client requirements and project specifications",
                "icon": "👥"
            },
            {
                "name": "Sales Report",
                "description": "Summary of sales activities, opportunities, and results",
                "icon": "📊"
            },
            {
                "name": "Real Estate Checklist",
                "description": "Property details, client requirements, and transaction tracking",
                "icon": "🏠"
            }
        ]
        
        # Create a card for each template
        for i, template in enumerate(templates):
            card = self.create_template_card(template)
            card.grid(row=i // 2, column=i % 2, padx=10, pady=10, sticky="nsew")
    
    def create_template_card(self, template):
        card_frame = ctk.CTkFrame(self.templates_frame)
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Icon
        icon_label = ctk.CTkLabel(
            card_frame,
            text=template["icon"],
            font=ctk.CTkFont(size=36)
        )
        icon_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Template name
        name_label = ctk.CTkLabel(
            card_frame,
            text=template["name"],
            font=ctk.CTkFont(size=16, weight="bold")
        )
        name_label.grid(row=1, column=0, padx=20, pady=(0, 10))
        
        # Template description
        desc_label = ctk.CTkLabel(
            card_frame,
            text=template["description"],
            font=ctk.CTkFont(size=12),
            wraplength=200
        )
        desc_label.grid(row=2, column=0, padx=20, pady=(0, 10))
        
        # Use template button
        use_button = ctk.CTkButton(
            card_frame,
            text="Use Template",
            command=lambda t=template: self.use_template(t)
        )
        use_button.grid(row=3, column=0, padx=20, pady=(0, 20))
        
        return card_frame
    
    def use_template(self, template):
        # Load template content
        template_content = self.load_template_content(template["name"])
        
        # Update editor
        self.editor_textbox.delete("0.0", "end")
        self.editor_textbox.insert("0.0", template_content)
        
        # Update status
        self.status_var.set(f"Loaded template: {template['name']}")
    
    def load_template_content(self, template_name):
        # This would load template content from files
        # For now, return placeholder content
        templates = {
            "Meeting Summary": "# Meeting Summary\n\n## Meeting Overview\n[Enter meeting purpose, date, and participants]\n\n## Key Discussion Points\n- Point 1\n- Point 2\n- Point 3\n\n## Decisions Made\n- Decision 1\n- Decision 2\n\n## Next Steps\n- Action 1 (Owner: [Name], Deadline: [Date])\n- Action 2 (Owner: [Name], Deadline: [Date])",
            
            "Client Brief": "# Client Brief\n\n## Client Information\nClient Name: [Name]\nContact Person: [Contact]\nContact Details: [Email/Phone]\n\n## Project Requirements\n[Detailed description of client requirements]\n\n## Timeline\n- Start Date: [Date]\n- Milestones: [List key milestones]\n- Completion Date: [Date]\n\n## Budget\n[Budget details]\n\n## Additional Notes\n[Any other relevant information]",
            
            "Sales Report": "# Sales Report\n\n## Overview\n[Summary of sales period and key results]\n\n## Key Accounts\n- Account 1: [Status update]\n- Account 2: [Status update]\n\n## Sales Pipeline\n[Description of current opportunities]\n\n## Forecast\n[Projected sales for next period]\n\n## Challenges & Solutions\n[Any issues encountered and how they were addressed]",
            
            "Real Estate Checklist": "# Real Estate Checklist\n\n## Property Details\nAddress: [Address]\nProperty Type: [Type]\nListing Price: [Price]\n\n## Client Requirements\n- Requirement 1\n- Requirement 2\n- Requirement 3\n\n## Viewing Notes\n[Notes from property viewings]\n\n## Transaction Tracking\n- [ ] Initial consultation\n- [ ] Property search\n- [ ] Viewings\n- [ ] Offer submission\n- [ ] Negotiations\n- [ ] Contract signing\n- [ ] Closing"
        }
        
        return templates.get(template_name, "# New Document\n\nEnter your content here.")
    
    def export_as_pdf(self):
        # Get document content
        content = self.editor_textbox.get("0.0", "end-1c")
        if not content.strip():
            self.status_var.set("Error: Document is empty")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.status_var.set("Exporting to PDF...")
                # Call document generator to create PDF
                generate_document(content, file_path, "pdf")
                self.status_var.set(f"Exported to {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"Error exporting: {str(e)}")
    
    def export_as_docx(self):
        # Get document content
        content = self.editor_textbox.get("0.0", "end-1c")
        if not content.strip():
            self.status_var.set("Error: Document is empty")
            return
        
        # Ask for save location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                self.status_var.set("Exporting to DOCX...")
                # Call document generator to create DOCX
                generate_document(content, file_path, "docx")
                self.status_var.set(f"Exported to {os.path.basename(file_path)}")
            except Exception as e:
                self.status_var.set(f"Error exporting: {str(e)}")
    
    def save_as_template(self):
        # Get document content
        content = self.editor_textbox.get("0.0", "end-1c")
        if not content.strip():
            self.status_var.set("Error: Document is empty")
            return
        
        # Ask for template name
        template_name = ctk.CTkInputDialog(
            text="Enter template name:",
            title="Save Template"
        ).get_input()
        
        if template_name:
            # This would save the template to a file
            # For now, just update the status
            self.status_var.set(f"Template '{template_name}' saved successfully")