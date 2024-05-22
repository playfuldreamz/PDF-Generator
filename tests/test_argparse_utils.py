import unittest
from unittest.mock import patch
from utils.argparse_utils import parse_arguments

class TestArgparseUtils(unittest.TestCase):
    def test_parse_arguments_required_arguments(self):
        with patch("sys.argv", ["script_name", "test_directory", "test_output_path"]):
            args = parse_arguments()

        self.assertEqual(args.directory, "test_directory")
        self.assertEqual(args.output_path, "test_output_path")
        self.assertFalse(args.verbose)
        self.assertFalse(args.include_hidden)
        self.assertEqual(args.file_types, [])

    def test_parse_arguments_optional_arguments(self):
        with patch("sys.argv", ["script_name", "test_directory", "test_output_path", "-v", "-i", "-t", ".txt", ".log"]):
            args = parse_arguments()

        self.assertEqual(args.directory, "test_directory")
        self.assertEqual(args.output_path, "test_output_path")
        self.assertTrue(args.verbose)
        self.assertTrue(args.include_hidden)
        self.assertEqual(args.file_types, [".txt", ".log"])

if __name__ == "__main__":
    unittest.main()