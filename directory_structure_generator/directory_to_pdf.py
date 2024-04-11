import subprocess
import os
import sys

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
        print(f"Directory structure has been saved to {output_file_path}")
    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python directory_to_pdf.py <directory> <output_path>")
        sys.exit(1)
    
    directory = sys.argv[1]
    output_path = sys.argv[2]
    
    # Extract the directory name to use as part of the output file name
    directory_name = os.path.basename(directory)
    
    # Construct the output file name
    output_file_name = f"{directory_name} directory content.txt"
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine the output directory and file name to get the full output path
    full_output_path = os.path.join(output_dir, output_file_name)
    
    create_pdf_from_directory_structure(directory, full_output_path)
