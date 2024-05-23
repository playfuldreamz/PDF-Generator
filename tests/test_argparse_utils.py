import subprocess
import sys
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
                    [sys.executable, "main.py", directory],  # Adjust command as needed
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
                    [sys.executable, "main.py", "test_directory", "-t", file_type],
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
            
    def test_multiple_occurrences_of_same_argument(self):
        with patch("sys.argv", ["script_name", "test_directory", "-t", ".txt", "-t", ".log"]):
            args = parse_arguments()
            self.assertEqual(args.file_types, [".txt", ".log"])

    def test_exclusion_lists_with_similar_names(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-e", "folder", "folder1", "-f", ".log", ".log1"],
        ):
            args = parse_arguments()
            self.assertEqual(args.exclude_folders, ["folder", "folder1"])
            self.assertEqual(args.exclude_file_types, [".log", ".log1"])
            
    def test_mixed_valid_invalid_file_types(self):
        with patch("sys.argv", ["script_name", "test_directory", "-t", ".txt", "invalid_type"]):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertEqual(args.file_types, [".txt", "invalid_type"])  # Should handle this gracefully, or you can add validation logic

    def test_invalid_arguments(self):
        with self.assertRaises(SystemExit):
            with patch("sys.argv", ["script_name", "-invalid"]):
                parse_arguments()

    def test_verbose_flag(self):
        with patch("sys.argv", ["script_name", "test_directory", "-v"]):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertTrue(args.verbose)
            self.assertFalse(args.include_hidden)

    def test_include_hidden_flag(self):
        with patch("sys.argv", ["script_name", "test_directory", "-i"]):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertFalse(args.verbose)
            self.assertTrue(args.include_hidden)
            
    def test_conflicting_arguments(self):
        with patch("sys.argv", ["script_name", "test_directory", "-v", "-i"]):
            args = parse_arguments()
            self.assertEqual(args.directory, "test_directory")
            self.assertTrue(args.verbose)
            self.assertTrue(args.include_hidden)
            
    def test_empty_optional_arguments(self):
        with patch(
            "sys.argv",
            ["script_name", "test_directory", "-t", "-e", "-f"]
        ):
            args = parse_arguments()
            self.assertEqual(args.file_types, [])
            self.assertEqual(args.exclude_folders, [])
            self.assertEqual(args.exclude_file_types, [])

if __name__ == "__main__":
    unittest.main()