import tkinter as tk
from tkinter import filedialog
from pdf_generator.pdf_generator import PDFGenerator  # Assuming your PDFGenerator is in pdf_generator/pdf_generator.py

import tkinter as tk
from tkinter import filedialog
from pdf_generator.pdf_generator import PDFGenerator

def create_gui():
    root = tk.Tk()
    root.title("PDF Generator")

    # Directory input
    directory_label = tk.Label(root, text="Directory:")
    directory_label.pack()

    directory_entry = tk.Entry(root, width=50)
    directory_entry.pack()

    browse_button = tk.Button(root, text="Browse", command=lambda: browse_directory(directory_entry))
    browse_button.pack()

    # File types input
    file_types_label = tk.Label(root, text="File Types:")
    file_types_label.pack()

    file_types_entry = tk.Entry(root, width=50)
    file_types_entry.pack()

    # Include hidden files checkbox
    include_hidden_var = tk.BooleanVar(value=False)
    include_hidden_checkbox = tk.Checkbutton(root, text="Include Hidden Files:", variable=include_hidden_var)
    include_hidden_checkbox.pack()

    # Generate PDF button
    generate_button = tk.Button(root, text="Generate PDF", command=lambda: generate_pdf(directory_entry, file_types_entry, include_hidden_var))
    generate_button.pack()

    # (Optional) Progress bar
    # progress_bar = tk.ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
    # progress_bar.pack()

    def browse_directory(entry):
        directory = filedialog.askdirectory()
        entry.delete(0, tk.END)
        entry.insert(0, directory)

    def generate_pdf(directory_entry, file_types_entry, include_hidden_var):
        directory = directory_entry.get()
        file_types = file_types_entry.get().split()  # Split file types by spaces
        include_hidden = include_hidden_var.get()

        try:
            pdf_generator = PDFGenerator(directory, directory, exclude_folders=[])  # Assuming output path is the same as directory
            pdf_generator.generate_pdf(include_hidden, file_types)
            # Update progress bar if needed
            tk.messagebox.showinfo("Success", "PDF generated successfully!")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    root.mainloop()