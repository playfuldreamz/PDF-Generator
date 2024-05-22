import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Create a PDF from the contents of files in a directory and its subdirectories.'
    )
    parser.add_argument('directory', type=str, help='The directory containing the files to convert to PDF.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-i', '--include-hidden', action='store_true', help='Include hidden files.')
    parser.add_argument('-t', '--file-types', nargs='*', default=[], help='File types to process')  # Changed to nargs='*'
    parser.add_argument('-e', '--exclude-folders', type=str, nargs='*', default=[], help='Folders to exclude from processing') # Changed to nargs='*'
    parser.add_argument('-f', '--exclude-file-types', nargs='*', default=[], help='File types to exclude from processing') # Changed to nargs='*'

    return parser.parse_args()
