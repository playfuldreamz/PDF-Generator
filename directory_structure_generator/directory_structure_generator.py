# directory_structure_generator.py
"""
Generates a PDF file containing the directory structure of the given directory.

The directory name is used to generate the output file name. The output file 
is written to the 'output' subdirectory. 

Args:
    directory (str): The path to the directory to generate the structure for.
"""
# directory_structure_generator.py
import os
from .directory_structure import create_pdf_from_directory_structure

class DirectoryStructureGenerator:
    def __init__(self, directory, output_path):
        self.directory = directory
        self.output_path = output_path

    def generate_directory_structure(self):
        directory_name = os.path.basename(self.directory)
        output_file_name = f"{directory_name} directory content.txt"
        
        # Combine the output directory and file name to get the full output path
        full_output_path = os.path.join(self.output_path, output_file_name)

        create_pdf_from_directory_structure(self.directory, full_output_path)
