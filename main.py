"""
Main entry point for the PDF generator application.

Parses command line arguments, sets up logging, determines output paths, 
instantiates the PDFGenerator and DirectoryStructureGenerator, and runs 
them in parallel using a ThreadPoolExecutor.
"""
import os
from concurrent.futures import ThreadPoolExecutor

from pdf_generator.pdf_generator import PDFGenerator 
from directory_structure_generator.directory_structure_generator import DirectoryStructureGenerator

from utils.argparse_utils import parse_arguments
from utils.logging_utils import configure_logging

def main():
    """
    Creates a logs directory in the same directory as the script, and configures logging to write to a log file in that directory.
    """
    logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
    os.makedirs(logs_dir, exist_ok=True)
    log_file = os.path.join(logs_dir, 'pdf_generator.log')
    logger = configure_logging(log_file)
    
    args = parse_arguments()
    
    # 1. Get Directory Input (Command Line or Prompt)
    if args.directory:
        directory = args.directory 
    else:
        directory = input("Enter the directory path: ")

    # 2. Validate Directory
    if not os.path.isdir(directory):
        logger.error(f"Invalid directory path: {directory}")
        print("Invalid directory path: " + directory)
        print("Please provide a valid directory path.")
        exit(1)
 
    # Determine the output folder path using a relative path from main.py
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder_path = os.path.join(script_dir, 'output')

    # Create a subdirectory named after the directory being processed
    directory_name = os.path.basename(args.directory)
    output_subdir_path = os.path.join(output_folder_path, directory_name)
    os.makedirs(output_subdir_path, exist_ok=True)

    # Pass the output subdirectory path to the PDFGenerator and DirectoryStructureGenerator
    pdf_generator = PDFGenerator(args.directory, output_subdir_path, args.exclude_folders, args.exclude_file_types)
    directory_structure_generator = DirectoryStructureGenerator(args.directory, output_subdir_path)

    # Use ThreadPoolExecutor to run the tasks in parallel
    with ThreadPoolExecutor() as executor:
        # Start the PDF generation task
        pdf_generation_future = executor.submit(pdf_generator.generate_pdf, args.include_hidden, args.file_types)

        # Start the directory structure generation task
        directory_structure_future = executor.submit(directory_structure_generator.generate_directory_structure)

        # Wait for both tasks to complete and handle exceptions
        try:
            pdf_generation_future.result()
            logger.verbose('PDF generation successful')
        except Exception as e:
            logger.verbose(f'PDF generation failed: {e}')
            logger.exception(e)

        try:
            directory_structure_future.result()
            logger.verbose('Directory structure generation successful')
        except Exception as e:
            logger.verbose(f'Directory structure generation failed: {e}')
            logger.exception(e)

if __name__ == '__main__':
    main()
