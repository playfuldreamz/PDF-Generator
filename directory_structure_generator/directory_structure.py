"""
Generates a text file containing the directory structure of the provided directory.

directory: The path to the directory to generate the structure for.
output_file_path: The path to write the generated directory structure text file to.
"""

import json
import os

def print_directory_structure(start_path: str, ignore_file_path) -> list:
    """Generates a nested list representing the directory structure.
       Ignores folders specified in a JSON file.

    Args:
        start_path (str): The starting directory path.
        ignore_file_path (str, optional): The path to the JSON file containing the ignore list. Defaults to 'ignore_folders.json'.

    Returns:
        list: A nested list representing the directory structure.
    """
    try:
        with open(ignore_file_path, 'r') as ignore_file:
            ignore_folders = json.load(ignore_file)
    except FileNotFoundError:
        print(f"Warning: Ignore file '{ignore_file_path}' not found. Proceeding without ignoring folders.")
        ignore_folders = []

    structure = []
    for item in os.listdir(start_path):
        item_path = os.path.join(start_path, item)
        if item in ignore_folders:
            continue  # Skip this item if it's in the ignore list

        if os.path.isdir(item_path):
            structure.append({
                "name": item,
                "type": "dir",
                "children": print_directory_structure(item_path, ignore_file_path)
            })
        else:
            structure.append({"name": item, "type": "file"})
    return structure

def create_pdf_from_directory_structure(directory, output_file_path, ignore_file_path):
    """
    Generate a text file with the directory structure.
    """    
    # Write the directory structure to the text file
    try:
        # Generate the directory structure as a string
        directory_structure = print_directory_structure(directory, ignore_file_path)

        # Convert the list to JSON string before writing
        directory_structure = json.dumps(directory_structure, indent=4)
        
        print(f"Writing directory structure to file: {output_file_path}")
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(directory_structure)
        print(f"Directory structure generation successful!")
    except IOError as e:
        print(f"Error writing to file: {e}")