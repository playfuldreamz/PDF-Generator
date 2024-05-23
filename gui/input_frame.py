# gui/input_frame.py
import tkinter as tk
from tkinter import ttk, filedialog

class InputFrame(tk.LabelFrame):
    def __init__(self, master, on_input_change=None):
        super().__init__(master, text="Input Options")
        self.on_input_change = on_input_change
        self.create_widgets()

    def create_widgets(self):
        # Directory input
        directory_label = tk.Label(self, text="Directory:")
        directory_label.grid(row=0, column=0, sticky="w")
        self.directory_entry = tk.Entry(self, width=50)
        self.directory_entry.grid(row=0, column=1)
        self.directory_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter the path to the directory containing the files to convert."))
        self.directory_entry.bind("<Leave>", lambda event: self.hide_tooltip())
        browse_button = tk.Button(self, text="Browse", command=self.browse_directory)
        browse_button.grid(row=0, column=2)

        # File types input (to include)
        file_types_label = tk.Label(self, text="File Types (to include):")
        file_types_label.grid(row=1, column=0, sticky="w")
        self.file_types_entry = tk.Entry(self, width=50)
        self.file_types_entry.grid(row=1, column=1, columnspan=2)
        self.file_types_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter file extensions to include (e.g., .txt .py). Separate multiple extensions with spaces."))
        self.file_types_entry.bind("<Leave>", lambda event: self.hide_tooltip())
        self.file_types_entry.bind("<KeyRelease>", self.on_entry_change)

        # File types input (to exclude)
        exclude_file_types_label = tk.Label(self, text="File Types (to exclude):")
        exclude_file_types_label.grid(row=2, column=0, sticky="w")
        self.exclude_file_types_entry = tk.Entry(self, width=50)
        self.exclude_file_types_entry.grid(row=2, column=1, columnspan=2)
        self.exclude_file_types_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter file extensions to exclude (e.g., .tmp .log). Separate multiple extensions with spaces."))
        self.exclude_file_types_entry.bind("<Leave>", lambda event: self.hide_tooltip())
        self.exclude_file_types_entry.bind("<KeyRelease>", self.on_entry_change)

        # Exclude folders input
        exclude_folders_label = tk.Label(self, text="Folders to Exclude:")
        exclude_folders_label.grid(row=3, column=0, sticky="w")
        self.exclude_folders_entry = tk.Entry(self, width=50)
        self.exclude_folders_entry.grid(row=3, column=1, columnspan=2)
        self.exclude_folders_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter folder names to exclude from processing. Separate multiple folder names with spaces."))
        self.exclude_folders_entry.bind("<Leave>", lambda event: self.hide_tooltip())
        self.exclude_folders_entry.bind("<KeyRelease>", self.on_entry_change)

        # Include hidden files checkbox
        self.include_hidden_var = tk.BooleanVar(value=False)
        include_hidden_checkbox = tk.Checkbutton(
            self, text="Include Hidden Files:", variable=self.include_hidden_var
        )
        include_hidden_checkbox.grid(row=4, column=0, columnspan=3)
        include_hidden_checkbox.bind("<Enter>", lambda event: self.show_tooltip(event, "Check this box to include hidden files in the PDF."))
        include_hidden_checkbox.bind("<Leave>", lambda event: self.hide_tooltip())
        include_hidden_checkbox.bind("<ButtonRelease-1>", self.on_entry_change)  # Bind to button release

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)
        self.on_entry_change()

    def on_entry_change(self, event=None):
        if self.on_input_change:
            self.on_input_change()

    def get_user_inputs(self):
        return {
            "directory": self.directory_entry.get(),
            "file_types": self.file_types_entry.get().split() if self.file_types_entry.get() else None,
            "exclude_file_types": self.exclude_file_types_entry.get().split() if self.exclude_file_types_entry.get() else None,
            "exclude_folders": self.exclude_folders_entry.get().split() if self.exclude_folders_entry.get() else None,
            "include_hidden": self.include_hidden_var.get(),
        }

    def show_tooltip(self, event, text):
        # Create a tooltip widget and display it
        self.tooltip = tk.Toplevel(self)
        self.tooltip.wm_overrideredirect(True)  # Remove window decorations
        self.tooltip.wm_geometry("+%d+%d" % (event.x_root + 10, event.y_root + 10))  # Position tooltip
        label = tk.Label(self.tooltip, text=text, justify="left", background="#FFFFE0", relief="solid", borderwidth=1)
        label.pack()

    def hide_tooltip(self):
        # Destroy the tooltip widget
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()