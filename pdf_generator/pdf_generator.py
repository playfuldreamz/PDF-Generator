import os
import json
import mimetypes
from typing import Callable, List, Optional

from utils.logging_utils import logger
from .pdf_operations import PDFOperations

class PDFGenerator:
    def __init__(self, directory: str, output_path: str, 
             exclude_folders: Optional[List[str]] = None, 
             exclude_file_types: Optional[List[str]] = None,
             config_path: str = 'config.json',
             ignore_file_path: str = 'ignore_folders.json'):
        
        self.directory = directory
        self.output_path = output_path
        self.exclude_folders = exclude_folders if exclude_folders else []
        self.exclude_file_types = exclude_file_types if exclude_file_types else []

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.font_family = config.get('font_family', 'Arial')
        self.font_size = config.get('font_size', 10)
        self.line_spacing = config.get('line_spacing', 10)
        
        # Load ignore folders from JSON
        try:
            with open(ignore_file_path, 'r') as ignore_file:
                self.ignore_folders = json.load(ignore_file)
        except FileNotFoundError:
            print(f"Warning: Ignore file '{ignore_file_path}' not found. Proceeding without ignoring folders.")
            self.ignore_folders = []

        self.pdf_operations = PDFOperations()
        self.found_file = False

    def filter_unsupported_chars(self, text: str) -> str:
        """Filters out characters that cannot be encoded in ASCII."""
        return text.encode("ascii", errors="ignore").decode("utf-8")

    def get_file_type(self, file_path: str) -> str:
        """Gets the MIME type of a file."""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type if mime_type else "application/octet-stream"

    def should_process_file(self, file_path: str, file_types: Optional[List[str]] = None) -> bool:
        """Determines if a file should be processed based on inclusion/exclusion lists."""
        file_extension = os.path.splitext(file_path)[-1]
        if file_extension:
            should_process = (file_types is None or file_extension in file_types) and \
                             file_extension not in self.exclude_file_types
        else:
            file_type = self.get_file_type(file_path)
            should_process = not any(
                excluded_type in file_type or excluded_type in "text"
                for excluded_type in self.exclude_file_types
            )
        return should_process

    def process_file(self, file_path: str, relative_path: str, feedback_callback: Optional[Callable] = None):
        """Processes a single file by reading its content and adding it to the PDF."""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            filtered_content = self.filter_unsupported_chars(content)

            self.pdf_operations.set_font(self.font_family, size=self.font_size)
            self.pdf_operations.add_text(f"{os.path.basename(file_path)} ({relative_path}):", align='L')
            self.pdf_operations.add_text(filtered_content, align='L')
            self.pdf_operations.add_line_break()

            logger.info(f"Processed file: {file_path}")
            if feedback_callback:
                feedback_callback(f"Processed file: {file_path}")

        except UnicodeDecodeError:
            logger.warning(f"Skipping file {file_path} due to encoding issues.")
            if feedback_callback:
                feedback_callback(f"Skipped file {file_path} due to encoding issues.")
        except OSError as e:
            logger.error(f"Error processing file {file_path}: {e}")
            if feedback_callback:
                feedback_callback(f"Error processing file {file_path}: {e}")

    def process_directory(self, directory_path: str, include_hidden: bool,
                           file_types: Optional[List[str]],
                           feedback_callback: Optional[Callable] = None,
                           progress_callback: Optional[Callable] = None,
                           current_file: int = 0,
                           total_files: int = 0):
        """Recursively processes directories and files."""
        if (not include_hidden and os.path.basename(directory_path).startswith('.')) or \
           os.path.basename(directory_path) in self.exclude_folders or \
           os.path.basename(directory_path) in self.ignore_folders:
            return current_file

        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            relative_path = os.path.relpath(item_path, start=self.directory)

            if (include_hidden or not item.startswith('.')) and os.path.isfile(item_path):
                if self.should_process_file(item_path, file_types):
                    self.found_file = True

                    if feedback_callback:
                        feedback_callback(f"Processing: {relative_path}")

                    self.process_file(item_path, relative_path, feedback_callback)

                    if progress_callback:
                        current_file += 1
                        progress_callback(current_file, total_files)

            elif os.path.isdir(item_path):
                current_file = self.process_directory(  # Update current_file from recursive call
                    item_path, include_hidden, file_types, feedback_callback,
                    progress_callback=progress_callback, current_file=current_file,
                    total_files=total_files
                )
        return current_file  # Return the updated current_file count

    def generate_pdf(self, include_hidden: bool, file_types: Optional[List[str]] = None, 
                     progress_callback: Optional[Callable] = None, 
                     feedback_callback: Optional[Callable] = None) -> Optional[bool]:
        """Main function to generate the PDF."""
        try:
            self.pdf_operations.add_page()
            self.pdf_operations.set_font(self.font_family, size=self.font_size)

            directory_name = os.path.basename(self.directory)
            self.pdf_operations.add_text(
                f"This PDF contains the contents of folders and files from the directory '{directory_name}' and its subdirectories."
            ).add_line_break()

            total_file_count = self.get_total_file_count(file_types)
            
            # Explicitly check if file_types is empty to process all
            if file_types is None or len(file_types) == 0:
                self.process_directory(self.directory, include_hidden, None, feedback_callback, 
                                       progress_callback=progress_callback, total_files=total_file_count)
            else:
                self.process_directory(self.directory, include_hidden, file_types, feedback_callback,
                                       progress_callback=progress_callback, total_files=total_file_count)

            if not self.found_file and file_types is not None:
                logger.verbose(f"No files with the following extensions were found: {', '.join(file_types)}")
                return False  # Indicate that no PDF was generated

            output_filename = os.path.join(self.output_path, f"{directory_name} dir content.pdf")
            logger.verbose("Saving PDF...")
            self.pdf_operations.save_pdf(output_filename)
            #Tell the user where the PDF is saved
            logger.verbose("PDF saved in " + output_filename)

            if progress_callback:
                progress_callback(total_file_count, total_file_count)

            return True

        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            logger.exception(e)
            return e  

    def get_total_file_count(self, file_types: Optional[List[str]] = None) -> int:
        """Calculates the total number of files to be processed."""
        total_file_count = 0
        for root, _, files in os.walk(self.directory):
            if os.path.basename(root) not in self.exclude_folders:
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.should_process_file(file_path, file_types):
                        total_file_count += 1
        return total_file_count