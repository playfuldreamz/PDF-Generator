# PDF Generator: Convert Directory Contents to PDFs

This Python application allows you to easily convert the contents of files within a directory and its subdirectories into a well-structured PDF document. It also generates a text file outlining the directory structure for easy reference.

## Features

*   **Easy to use:** Simply provide the directory path and let the application do its magic!
*   **Customizable:** Choose which file types to include and exclude specific folders and file types. 
*   **Parallel processing:** Generates the PDF and directory structure text file simultaneously for faster execution.
*   **Interface Options:** Choose the interface that suits your workflow:
    *   **Command-line interface (CLI):** For automation and scripting.
    *   **Graphical user interface (GUI):** For interactive use. 
*   **Cross-platform:** Works seamlessly on Windows, macOS, and Linux.
*   **Open-source:** Freely use, modify, and contribute to the project. 

## Getting Started

### Prerequisites:

*   Python 3.6 or later
*   Tkinter library (usually included with Python) 
*   `tree` command (available on most Unix-based systems and through tools like Cygwin on Windows)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/playfuldreamz/PDF-Generator
   ```

2. **Navigate to the project directory:**
   ```bash
   cd PDF-Generator
   ```

3. **Create and activate a virtual environment (recommended):**
   ```bash
   # Create the environment
   python3 -m venv env  # Or use 'python -m venv env'

   # Activate the environment
   source env/bin/activate  # Linux/macOS
   env\Scripts\activate.bat  # Windows
   ```

4. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage:

### Command-Line Interface (CLI):
# Basic usage
```
python main.py <directory_path> [options]
```

**Options:**

*   **`<directory_path>` (required):** The path to the directory containing the files to convert to PDF. 
*   **`-v`, `--verbose`:** Enable verbose mode for more detailed logging output.
*   **`-i`, `--include-hidden`:** Include hidden files in the PDF.
*   **`-t`, `--file-types`:** Specify the file types to include (e.g., `.txt`, `.py`). You can provide multiple file types separated by spaces. 
*   **`-e`, `--exclude-folders`:** Specify folders to exclude from processing. You can provide multiple folder names separated by spaces.
*   **`-f`, `--exclude-file-types`:** Specify file types to exclude, regardless of whether they have extensions or not. You can provide multiple file types separated by spaces. 

**Examples:**

*   Generate PDF from files in the "my\_project" directory:

```
python main.py my_project 
```

*   Include hidden files:

```
python main.py my_project -i
``` 

*   Process only .txt and .py files:

```
python main.py my_project -t .txt .py
``` 

*   Exclude the "logs" and "venv" folders:

```
python main.py my_project -e logs venv
``` 

*   Exclude files with the .scmp extension or identified as "SCMP" or plain text: 
```
python main.py my_project -f .scmp 
``` 

### Graphical User Interface (GUI):

1.  Run `python run_gui.py`.
2.  Use the GUI to select the directory, specify file types, and choose options. 
3.  Click "Generate PDF".

## Configuration

- **`config.json`:** You can customize default settings like font family, font size, and line spacing by modifying the `config.json` file.
- **GUI Settings:** The GUI provides an interface to change these settings as well.

## Contributing

We welcome contributions to make this project even better! Here's how you can get involved:

*   **Report bugs:** If you encounter any issues, please open an issue on GitHub.
*   **Suggest features:** Have an idea for a cool new feature? Share it with us!
*   **Submit pull requests:** Fix bugs, implement new features, or improve the documentation.

## Development Setup

1.Fork the repository.
2.Create a virtual environment:
```bash
python -m venv venv
```

3.Activate the virtual environment:
Windows:

```bash
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

4.Install development dependencies:
```
pip install -r requirements-dev.txt
```

## Run tests
```
pytest
```
