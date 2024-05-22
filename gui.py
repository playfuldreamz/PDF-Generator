import tkinter as tk
from gui_app import PDFGeneratorApp  # Import the PDFGeneratorApp class

def create_gui():
    root = tk.Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()
    
if __name__ == "__main__":
    create_gui()