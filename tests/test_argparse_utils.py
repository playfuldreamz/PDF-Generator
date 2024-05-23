import subprocess
import unittest
from unittest.mock import patch
import argparse
from utils.argparse_utils import parse_arguments


class TestArgparseUtils(unittest.TestCase):
    def test_parse_arguments_required_arguments(self):
        with patch("sys.argv", ["script_name", "test_directory"]):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertFalse(args.verbose)
            self.assertFalse(args.include_hidden)
            self.assertEqual(args.file_types, [])
            self.assertEqual(args.exclude_folders, [])
            self.assertEqual(args.exclude_file_types, [])

    def test_parse_arguments_optional_arguments(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-v", "-i", "-t", ".txt", ".log", "-e", "folder1", "folder2", "-f", ".ignore", ".tmp"],  
        ):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertTrue(args.verbose)
            self.assertTrue(args.include_hidden)
            self.assertEqual(args.file_types, [".txt", ".log"])
            self.assertEqual(args.exclude_folders, ["folder1", "folder2"])
            self.assertEqual(args.exclude_file_types, [".ignore", ".tmp"])


    def test_invalid_directory(self):
        invalid_directories = [
            "nonexistent_directory",
            "tests/test_argparse_utils.py",  # Existing file
            "",  # Empty string
        ]
        for directory in invalid_directories:
            with self.subTest(directory=directory):
                result = subprocess.run(
                    ["python", "main.py", directory],  # Adjust command as needed
                    capture_output=True,
                    text=True,
                )
                self.assertNotEqual(result.returncode, 0, f"Expected non-zero exit code for directory: {directory}")
                # Add assertions to check stderr for specific error messages

    def test_invalid_file_types(self):
        invalid_file_types = [
            "txt",  # Missing leading dot
            " .txt",  # Leading space
            ". txt",  # Space after dot
        ]
        for file_type in invalid_file_types:
            with self.subTest(file_type=file_type):
                result = subprocess.run(
                    ["python", "main.py", "test_directory", "-t", file_type],
                    capture_output=True, 
                    text=True, 
                )
                self.assertNotEqual(result.returncode, 0, f"Expected non-zero exit code for file type: {file_type}")
                # Add assertions to check stderr for specific error messages

    def test_empty_optional_arguments(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-t", "-e", "-f"],  # Empty lists
        ):
            args = parse_arguments()
            self.assertEqual(args.file_types, [])
            self.assertEqual(args.exclude_folders, [])
            self.assertEqual(args.exclude_file_types, [])
            
    def test_parse_arguments_multiple_file_types(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-t", ".txt", ".log", ".pdf"],
        ):
            args = parse_arguments()
            self.assertEqual(args.file_types, [".txt", ".log", ".pdf"])

    def test_parse_arguments_multiple_exclude_folders(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-e", "folder1", "folder2", "folder3"],
        ):
            args = parse_arguments()
            self.assertEqual(args.exclude_folders, ["folder1", "folder2", "folder3"])


if __name__ == "__main__":
    unittest.main()