import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
import os
import json

from pdf_generator.pdf_generator import PDFGenerator
from directory_structure_generator.directory_structure_generator import DirectoryStructureGenerator

class PDFGeneratorApp:
    def __init__(self, master):
        self.master = master
        master.title("PDF Generator")

        # Load config.json
        self.config_path = 'config.json'
        self.load_config()
        
        # Configure default font style
        default_font = font.Font(family="Inter", size=10, weight="bold")  # Adjust as needed
        master.option_add("*Font", default_font) 

        # Create frames for better organization
        input_frame = tk.LabelFrame(master, text="Input Options")
        input_frame.pack(padx=10, pady=10)

        output_frame = tk.LabelFrame(master, text="Output Options")
        output_frame.pack(padx=10, pady=10)

        feedback_frame = tk.LabelFrame(master, text="Feedback")
        feedback_frame.pack(padx=10, pady=5) 

        # Directory input
        directory_label = tk.Label(input_frame, text="Directory:")
        directory_label.pack()

        self.directory_entry = tk.Entry(input_frame, width=50)
        self.directory_entry.pack()

        browse_button = tk.Button(input_frame, text="Browse", command=self.browse_directory)
        browse_button.pack()

        # File types input (to include)
        file_types_label = tk.Label(input_frame, text="File Types (to include):")
        file_types_label.pack()

        self.file_types_entry = tk.Entry(input_frame, width=50)
        self.file_types_entry.pack()
        self.file_types_entry.bind("<Enter>", lambda event: event.widget.config(fg="blue"))  # Example tooltip
        self.file_types_entry.bind("<Leave>", lambda event: event.widget.config(fg="black"))

        # File types input (to exclude)
        exclude_file_types_label = tk.Label(input_frame, text="File Types (to exclude):")
        exclude_file_types_label.pack()

        self.exclude_file_types_entry = tk.Entry(input_frame, width=50)
        self.exclude_file_types_entry.pack()

        # Exclude folders input
        exclude_folders_label = tk.Label(input_frame, text="Folders to Exclude:")
        exclude_folders_label.pack()

        self.exclude_folders_entry = tk.Entry(input_frame, width=50)
        self.exclude_folders_entry.pack()

        # Include hidden files checkbox
        self.include_hidden_var = tk.BooleanVar(value=False)
        include_hidden_checkbox = tk.Checkbutton(input_frame, text="Include Hidden Files:", variable=self.include_hidden_var)
        include_hidden_checkbox.pack()

        # Settings Frame
        settings_frame = tk.LabelFrame(master, text="PDF Settings")
        settings_frame.pack(padx=10, pady=10)

        # Font Family
        font_family_label = tk.Label(settings_frame, text="Font Family:")
        font_family_label.grid(row=0, column=0, sticky="w")
        self.font_family_entry = tk.Entry(settings_frame, width=20)
        self.font_family_entry.insert(0, self.config['font_family'])
        self.font_family_entry.grid(row=0, column=1)

        # Font Size
        font_size_label = tk.Label(settings_frame, text="Font Size:")
        font_size_label.grid(row=1, column=0, sticky="w")
        self.font_size_entry = tk.Entry(settings_frame, width=20)
        self.font_size_entry.insert(0, self.config['font_size'])
        self.font_size_entry.grid(row=1, column=1)

        # Line Spacing
        line_spacing_label = tk.Label(settings_frame, text="Line Spacing:")
        line_spacing_label.grid(row=2, column=0, sticky="w")
        self.line_spacing_entry = tk.Entry(settings_frame, width=20)
        self.line_spacing_entry.insert(0, self.config['line_spacing'])
        self.line_spacing_entry.grid(row=2, column=1)

        # Save Settings Button
        save_settings_button = tk.Button(settings_frame, text="Save Settings", command=self.save_config)
        save_settings_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Progress bar
        self.progress_bar = ttk.Progressbar(output_frame, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.pack()

        # Feedback listbox
        self.feedback_listbox = tk.Listbox(feedback_frame, width=80, height=15)  # Adjust width/height as needed
        self.feedback_listbox.pack(fill=tk.BOTH, expand=True) 

        # Status label
        self.status_label = tk.Label(output_frame, text="")
        self.status_label.pack()

        # Generate PDF button and its command
        generate_button = tk.Button(output_frame, text="Generate PDF", command=self.generate_pdf)
        generate_button.pack()

        # Example of adding tooltips
        self.directory_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter the directory path where files are located"))
        self.directory_entry.bind("<Leave>", lambda event: self.hide_tooltip())

        self.file_types_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter file types to include (e.g., .txt, .py)")) 
        self.file_types_entry.bind("<Leave>", lambda event: self.hide_tooltip())

        self.exclude_file_types_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter file types to exclude (e.g., .scmp)"))
        self.exclude_file_types_entry.bind("<Leave>", lambda event: self.hide_tooltip())

        self.exclude_folders_entry.bind("<Enter>", lambda event: self.show_tooltip(event, "Enter folder names to exclude (separated by spaces)"))
        self.exclude_folders_entry.bind("<Leave>", lambda event: self.hide_tooltip())
        
    def load_config(self):
        """Loads configuration from config.json."""
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)

    def save_config(self):
        """Saves the current settings to config.json."""
        self.config['font_family'] = self.font_family_entry.get()
        self.config['font_size'] = int(self.font_size_entry.get()) # Convert to int
        self.config['line_spacing'] = int(self.line_spacing_entry.get()) # Convert to int

        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)

        messagebox.showinfo("Success", "Settings saved successfully!")

    def browse_directory(self):
        directory = filedialog.askdirectory()
        self.directory_entry.delete(0, tk.END)
        self.directory_entry.insert(0, directory)

    def generate_pdf(self):
        directory = self.directory_entry.get()
        file_types = self.file_types_entry.get().split()
        exclude_file_types = self.exclude_file_types_entry.get().split()
        exclude_folders = self.exclude_folders_entry.get().split()
        include_hidden = self.include_hidden_var.get()

        # Create output subdirectory path
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of gui_app.py
        output_folder_path = os.path.join(script_dir, 'output')  # Go up one level to the project root
        directory_name = os.path.basename(directory)
        output_subdir_path = os.path.join(output_folder_path, directory_name)
        os.makedirs(output_subdir_path, exist_ok=True)

        # Input validation
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        for file_type in file_types:
            if not file_type.startswith("."):
                messagebox.showerror("Error", "File types must start with a '.' (e.g., .txt)")
                return

        for exclude_file_type in exclude_file_types:
            if not exclude_file_type.startswith("."):
                messagebox.showerror("Error", "Excluded file types must start with a '.' (e.g., .scmp)")
                return

        try:
            self.update_status("Processing files...")
            pdf_generator = PDFGenerator(directory, output_subdir_path, exclude_folders=exclude_folders, exclude_file_types=exclude_file_types)
            result = pdf_generator.generate_pdf(include_hidden, file_types, self.update_progress, self.update_feedback)

            if result is True:  # Check if PDF was successfully generated
                print("PDF generated successfully!") # Console message for success
                self.update_status("Generating directory structure...")
                dir_structure_gen = DirectoryStructureGenerator(directory, output_subdir_path)
                dir_structure_gen.generate_directory_structure()
                print("Directory structure text file generated successfully!") # Console success message

                self.update_status("Completed!")  
                messagebox.showinfo("Success", "PDF and directory structure generated successfully!")
            elif isinstance(result, Exception):  # Check if result is an exception
                error_message = f"An error occurred: {result}"
                self.update_feedback(error_message)
                raise Exception("Failed to generate PDF.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.update_status("")  # Clear status message

    def update_progress(self, current, total):
        if total > 0:
            self.progress_bar["value"] = (current / total) * 100
        else:
            self.progress_bar["value"] = 100  # Assuming completion when total is 0
        self.master.update_idletasks()

    def update_feedback(self, message):
        self.feedback_listbox.insert(tk.END, message)
        self.master.update_idletasks()  

    def update_status(self, message):
        self.status_label.config(text=message)

    def show_tooltip(self, event, text):
        self.tooltip_window = tk.Toplevel(self.master)
        self.tooltip_window.wm_overrideredirect(True) 
        self.tooltip_window.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
        tooltip_label = tk.Label(self.tooltip_window, text=text, justify='left', 
                                 background="#ffffe0", relief='solid', borderwidth=1)
        tooltip_label.pack(ipadx=1)

    def hide_tooltip(self):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()