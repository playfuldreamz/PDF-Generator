import tkinter as tk
from tkinter import ttk

class OutputFrame(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="Output & Feedback")  # Frame title
        self.create_widgets()

    def create_widgets(self):
        # Progress Bar
        self.progress_bar = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="determinate"
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, pady=(5, 0))  # Adjust padding

        # Status Label 
        self.status_label = tk.Label(self, text="")
        self.status_label.grid(row=1, column=0, columnspan=2)

        # Feedback Listbox
        self.feedback_listbox = tk.Listbox(self, width=60, height=10)
        self.feedback_listbox.grid(row=2, column=0, columnspan=2, pady=(5, 0))  # Adjust padding

        # Add a scrollbar to the Listbox (optional but recommended)
        scrollbar = tk.Scrollbar(self, orient="vertical", command=self.feedback_listbox.yview)
        scrollbar.grid(row=2, column=2, sticky="ns") 
        self.feedback_listbox.config(yscrollcommand=scrollbar.set)

    def update_progress(self, current, total):
        """Updates the progress bar."""
        if total > 0:
            progress = (current / total) * 100
            self.progress_bar["value"] = progress
        else:
            self.progress_bar["value"] = 100
        self.progress_bar.update()

    def update_status(self, message):
        """Updates the status label."""
        self.status_label.config(text=message)
        self.status_label.update()

    def add_feedback(self, message):
        """Adds a message to the feedback listbox."""
        self.feedback_listbox.insert(tk.END, message)
        self.feedback_listbox.see(tk.END)  # Auto-scroll to the end 