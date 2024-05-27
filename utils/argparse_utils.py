import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Create a PDF from the contents of files in a directory and its subdirectories.'
    )
    parser.add_argument('directory', type=str, nargs='?', help='The directory containing the files to convert to PDF.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode.')
    parser.add_argument('-i', '--include-hidden', action='store_true', help='Include hidden files.')
    parser.add_argument('-t', '--file-types', action='append', nargs='*', default=[], help='File types to process')
    parser.add_argument('-e', '--exclude-folders', action='append', nargs='*', default=[], help='Folders to exclude from processing')
    parser.add_argument('-f', '--exclude-file-types', action='append', nargs='*', default=[], help='File types to exclude from processing')

    args = parser.parse_args()
 
    # Flatten lists of lists created by `append` action
    args.file_types = [item for sublist in args.file_types for item in sublist] if args.file_types else []
    args.exclude_folders = [item for sublist in args.exclude_folders for item in sublist] if args.exclude_folders else []
    args.exclude_file_types = [item for sublist in args.exclude_file_types for item in sublist] if args.exclude_file_types else []

    return args