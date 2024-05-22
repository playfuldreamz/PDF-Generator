import tkinter as tk
from tkinter import ttk, font
import os

from .settings_frame import SettingsFrame
from .input_frame import InputFrame
from .output_frame import OutputFrame
from .event_handler import GUIEventHandler

from pdf_generator.pdf_generator import PDFGenerator
from directory_structure_generator.directory_structure_generator import DirectoryStructureGenerator 

class PDFGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Generator")
        self.config_path = 'config.json'

        # Configure default font style
        default_font = font.Font(family="Inter", size=10, weight="bold")
        master.option_add("*Font", default_font)

        # Create Frames
        self.input_frame = InputFrame(master, on_input_change=self.handle_input_change)
        self.input_frame.pack(padx=10, pady=10)

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
        """Handles changes to input fields (currently not used, but can be extended)."""
        pass 

def create_gui():
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()

if __name__ == "__main__":
    create_gui()