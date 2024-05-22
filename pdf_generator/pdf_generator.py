import os
import json
import mimetypes

from utils.logging_utils import logger
from .pdf_operations import PDFOperations

class PDFGenerator:
    def __init__(self, directory, output_path, exclude_folders=None, exclude_file_types=None, config_path='config.json'):
        self.directory = directory
        self.output_path = output_path
        self.exclude_folders = exclude_folders if exclude_folders else []
        self.exclude_file_types = exclude_file_types if exclude_file_types else []

        with open(config_path, 'r') as config_file:
            config = json.load(config_file)

        self.font_family = config.get('font_family', 'Arial')
        self.font_size = config.get('font_size', 10)
        self.line_spacing = config.get('line_spacing', 10)
        self.pdf_operations = PDFOperations()
        self.found_file = False

    def filter_unsupported_chars(self, text):
        return text.encode("ascii", errors="ignore").decode("utf-8")

    def get_file_type(self, file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type if mime_type else "application/octet-stream"

    def process_directory(self, directory_path, include_hidden, file_types, feedback_callback=None):
        # Check if the current directory should be excluded (hidden or in exclude_folders list)
        if (not include_hidden and os.path.basename(directory_path).startswith('.')) or \
        os.path.basename(directory_path) in self.exclude_folders:
            return  # Skip processing this directory

        # Set font for directory description
        self.pdf_operations.set_font(self.font_family, size=self.font_size)

        # Iterate over each item in the directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if (include_hidden or not item.startswith('.')) and os.path.isfile(item_path):
                # Check file type inclusion and exclusion
                file_extension = os.path.splitext(item)[-1]
                if file_extension:  # Check if extension exists
                    should_process = (file_types is None or file_extension in file_types) and \
                                     file_extension not in self.exclude_file_types
                else:
                    file_type = self.get_file_type(item_path)
                    # Check if detected file type (or "text" for broader matching) is in exclude_file_types
                    should_process = not any(
                        excluded_type in file_type or excluded_type in "text"
                        for excluded_type in self.exclude_file_types
                    )

                if should_process:
                    self.found_file = True
                    try:
                        # Attempt to open the file with utf-8 encoding and read its content
                        with open(item_path, 'r', encoding='utf-8') as file:
                            content = file.read()

                        # Filter out unsupported characters
                        filtered_content = self.filter_unsupported_chars(content)

                        # Extract the base directory name
                        base_dir_name = os.path.basename(self.directory)

                        # Construct the description including the base directory name and the relative path
                        description = os.path.join(base_dir_name, os.path.relpath(item_path, start=self.directory))

                        # Add the file name and filtered content to the PDF, including the directory path
                        self.pdf_operations.add_text(f"{item} ({description}):", align='L')
                        self.pdf_operations.add_text(filtered_content, align='L')
                        self.pdf_operations.add_line_break()

                        # Log and provide feedback for the processed file
                        logger.info(f"Processed file: {item_path}")
                        if feedback_callback:
                            feedback_callback(f"Processed file: {item_path}") 

                    except UnicodeDecodeError:
                        # If a UnicodeDecodeError occurs, skip this file
                        logger.warning(f"Skipping file {item} due to encoding issues.")
                        if feedback_callback:
                            feedback_callback(f"Skipped file {item} due to encoding issues.")

                    except OSError as e:
                        # Log other OS errors
                        logger.error(f"Error processing file {item}: {e}")
                        if feedback_callback:
                            feedback_callback(f"Error processing file {item}: {e}")

            elif os.path.isdir(item_path):
                # If the item is a directory, recursively process it
                self.process_directory(item_path, include_hidden, file_types, feedback_callback)

    def generate_pdf(self, include_hidden, file_types, progress_callback=None, feedback_callback=None):
        try:
            # Add a new page to the PDF
            self.pdf_operations.add_page()
            self.pdf_operations.set_font(self.font_family, size=self.font_size)

            # Add a description at the top of the PDF including the directory name
            directory_name = os.path.basename(self.directory)
            self.pdf_operations.add_text(
                f"This PDF contains the contents of folders and files from the directory '{directory_name}' and its subdirectories.").add_line_break()

            # Get total file count (excluding files in excluded folders)
            total_file_count = 0
            for root, _, files in os.walk(self.directory):
                if os.path.basename(root) not in self.exclude_folders:  # Only count files in non-excluded folders
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_extension = os.path.splitext(file)[-1]
                        if file_extension:
                            should_count = (file_types is None or file_extension in file_types) and \
                                           file_extension not in self.exclude_file_types
                        else:
                            file_type = self.get_file_type(file_path)
                            should_count = not any(
                                excluded_type in file_type or excluded_type in "text"
                                for excluded_type in self.exclude_file_types
                            ) 
                        if should_count:
                            total_file_count += 1

            # Process the directory and its subdirectories
            current_file_count = 0
            if not file_types:
                logger.verbose("Processing all files.")
                self.process_directory(self.directory, include_hidden, None, feedback_callback)
            else:
                logger.verbose(f"Processing files with the following extensions: {', '.join(file_types)}")
                self.process_directory(self.directory, include_hidden, file_types, feedback_callback)


            # Log a message if no files of the specified type were found
            if not self.found_file and file_types is not None:
                logger.verbose(f"No files with the following extensions were found: {', '.join(file_types)}")

            # Generate the output file name based on the directory name within the output folder
            output_filename = os.path.join(self.output_path, f"{directory_name} dir content.pdf")

            # Save the PDF with the specified name
            logger.verbose("Saving PDF...")
            self.pdf_operations.save_pdf(output_filename)

            # Final progress update
            if progress_callback:
                progress_callback(total_file_count, total_file_count)

            return True  # Indicate successful PDF generation
        
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            logger.exception(e)
            return e  # Return the exception object