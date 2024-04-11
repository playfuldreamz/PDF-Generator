"""
Generates a text file containing the directory structure of the provided directory.

directory: The path to the directory to generate the structure for.
output_file_path: The path to write the generated directory structure text file to.
"""
import subprocess

def print_directory_structure(start_path):
    """
    Executes the 'tree' command for the provided directory and returns its output.
    """
    # Construct the command to execute
    command = f'tree /f "{start_path}"'
    
    # Execute the command and capture its output
    try:
        output = subprocess.check_output(command, shell=True, text=True)
    except subprocess.CalledProcessError as e:
        # Handle errors, such as the 'tree' command not being found
        print(f"Error executing 'tree' command: {e}")
        return ""
    
    return output

def create_pdf_from_directory_structure(directory, output_file_path):
    """
    Generate a text file with the directory structure.
    """
    # Generate the directory structure as a string
    directory_structure = print_directory_structure(directory)
    
    # Write the directory structure to the text file
    try:
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(directory_structure)
        print(f"Saving Directory structure txt...")
    except IOError as e:
        print(f"Error writing to file: {e}")