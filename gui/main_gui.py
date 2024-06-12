import os
import tkinter as tk
from tkinter import font

from .settings_frame import SettingsFrame
from .input_frame import InputFrame
from .output_frame import OutputFrame
from .event_handler import GUIEventHandler

from tkinterdnd2 import DND_FILES, TkinterDnD

class PDFGeneratorApp:
    def __init__(self, master):
        self.master = master 
        self.master.title("PDF Generator")
        self.config_path = 'config.json'

        # Configure default font style
        default_font = font.Font(family="Inter", size=10, weight="bold")
        master.option_add("*Font", default_font)

        # Create Frames
        self.input_frame = InputFrame(self.master, on_input_change=self.handle_input_change)
        self.input_frame.pack(padx=10, pady=10)

        # Enable drag and drop on the directory entry
        self.input_frame.directory_entry.dnd_bind("<<Drop>>", self.input_frame.drop_inside_entry)

        self.output_frame = OutputFrame(master)
        self.output_frame.pack(padx=10, pady=(0, 10))  # Adjust padding

        self.settings_frame = SettingsFrame(master, self.config_path)
        self.settings_frame.pack(padx=10, pady=10)

        # Event Handler
        self.event_handler = GUIEventHandler(self)

        # Generate PDF Button
        generate_button = tk.Button(
            master, text="Generate PDF", command=self.event_handler.handle_generate_pdf
        )
        generate_button.pack(pady=10)

    def handle_input_change(self):
        """Handles changes to input fields. Updates status based on input validity."""
        inputs = self.input_frame.get_user_inputs()
        directory = inputs['directory']
        file_types = inputs['file_types']

        # Input Validation
        if not directory or not os.path.isdir(directory):
            self.output_frame.update_status("Please select a valid directory.")
            return

        for file_type in file_types or []:
            if not file_type.startswith("."):
                self.output_frame.update_status("File types must start with a '.' (e.g., .txt)")
                return

        # If all inputs are valid, update status to indicate readiness
        self.output_frame.update_status("Inputs are valid. Ready to generate PDF.")         

def create_gui():
    root = TkinterDnD.Tk()
    PDFGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()