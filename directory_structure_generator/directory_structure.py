"""
Generates a text file containing the directory structure of the provided directory.

directory: The path to the directory to generate the structure for.
output_file_path: The path to write the generated directory structure text file to.
"""
import os

def print_directory_structure(start_path: str, indent: str = "") -> str:
    """Generates a tree-like directory structure string.

    Args:
        start_path (str): The starting directory path.
        indent (str, optional): String used for indentation. Defaults to "".

    Returns:
        str: The directory structure as a string.
    """
    output = ""
    items = os.listdir(start_path)
    for index, item in enumerate(items):
        item_path = os.path.join(start_path, item)
        is_last_item = index == len(items) - 1  # Check if it's the last item

        if is_last_item:
            output += f"{indent}¦   {item}\n"
            if os.path.isdir(item_path):
                output += print_directory_structure(item_path, indent + "    ")  # Indentation for last folder
        else:
            output += f"{indent}+---{item}\n"
            if os.path.isdir(item_path):
                output += print_directory_structure(item_path, indent + "¦   ")

    return output

def create_pdf_from_directory_structure(directory, output_file_path):
    """
    Generate a text file with the directory structure.
    """    
    # Write the directory structure to the text file
    try:
        # Generate the directory structure as a string
        directory_structure = print_directory_structure(directory)

        print(f"Writing directory structure to file: {output_file_path}")
        with open(output_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(directory_structure)
        print(f"Directory structure generation successful!")
    except IOError as e:
        print(f"Error writing to file: {e}")