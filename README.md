📁 PDF Generator: Convert Directory Contents to PDFs 📄

This Python application helps you effortlessly convert the contents of files within a directory and its subdirectories into a well-formatted PDF document. It also generates a text file outlining the directory structure for easy reference.

✨ Features
Easy to use: Simply provide the directory path and let the application do its magic! 🪄
Customizable: Choose which file types to include and exclude specific folders. 🎯
Parallel processing: Generates the PDF and directory structure text file simultaneously for faster execution. ⚡
GUI or command-line interface: Choose the interface that suits your workflow. 💻
Cross-platform: Works seamlessly on Windows, macOS, and Linux. 🐧
Open-source: Freely use, modify, and contribute to the project. 🤝

🚀 Getting Started
Prerequisites:
Python 3.6 or later
Tkinter library (usually included with Python)

Installation:
Clone or download the repository.
Open a terminal in the project directory.
Install the required dependencies:
pip install -r requirements.txt

Usage:
# Basic usage
python main.py <directory_path>

# Example: Generate PDF from files in "my_project" directory
python main.py my_project

# Include hidden files
python main.py my_project -i

# Specify file types to process (e.g., .txt and .py)
python main.py my_project -t .txt .py

# Exclude specific folders (e.g., "logs" and "venv")
python main.py my_project -e logs venv

# Combine options
python main.py my_project -i -t .txt .py -e logs venv

GUI:
Run python main.py.
Use the GUI to select the directory, specify file types, and choose options.
Click "Generate PDF".

🛠️ Contributing
We welcome contributions to make this project even better! Here's how you can get involved:
Report bugs: If you encounter any issues, please open an issue on GitHub. 🐛
Suggest features: Have an idea for a cool new feature? Share it with us! ✨
Submit pull requests: Fix bugs, implement new features, or improve the documentation. 

📝 Development Setup:
Fork the repository.
Create a virtual environment:
python -m venv venv

Activate the virtual environment:
Windows: venv\Scripts\activate
macOS/Linux: source venv/bin/activate

Install development dependencies:
pip install -r requirements.txt

Run tests:
pytest
