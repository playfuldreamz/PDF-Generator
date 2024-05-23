import tkinter as tk
from tkinter import messagebox
import json

class SettingsFrame(tk.LabelFrame):
    def __init__(self, master, config_path, on_save_callback=None): 
        super().__init__(master, text="PDF Settings")
        self.config_path = config_path
        self.on_save_callback = on_save_callback  
        self.load_config()
        self.create_widgets()

    def create_widgets(self):
        # Font Family
        font_family_label = tk.Label(self, text="Font Family:")
        font_family_label.grid(row=0, column=0, sticky="w")
        self.font_family_entry = tk.Entry(self, width=20)
        self.font_family_entry.insert(0, self.config['font_family'])
        self.font_family_entry.grid(row=0, column=1)

        # Font Size
        font_size_label = tk.Label(self, text="Font Size:")
        font_size_label.grid(row=1, column=0, sticky="w")
        self.font_size_entry = tk.Entry(self, width=20)
        self.font_size_entry.insert(0, self.config['font_size'])
        self.font_size_entry.grid(row=1, column=1)

        # Line Spacing
        line_spacing_label = tk.Label(self, text="Line Spacing:")
        line_spacing_label.grid(row=2, column=0, sticky="w")
        self.line_spacing_entry = tk.Entry(self, width=20)
        self.line_spacing_entry.insert(0, self.config['line_spacing'])
        self.line_spacing_entry.grid(row=2, column=1)

        # Save Settings Button
        save_settings_button = tk.Button(self, text="Save Settings", command=self.save_config)
        save_settings_button.grid(row=3, column=0, columnspan=2, pady=10)

    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        """Saves settings and notifies the main GUI."""
        self.config['font_family'] = self.font_family_entry.get()
        self.config['font_size'] = int(self.font_size_entry.get())
        self.config['line_spacing'] = int(self.line_spacing_entry.get())

        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

        messagebox.showinfo("Success", "Settings saved successfully!")

        # Notify the main GUI that settings have been saved (optional)
        if self.on_save_callback:
            self.on_save_callback()
