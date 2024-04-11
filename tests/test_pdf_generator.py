import unittest
import os
from pdf_generator.pdf_generator import PDFGenerator

class TestPDFGenerator(unittest.TestCase):

    def setUp(self):
        # Initialize any necessary objects or variables before each test method
        self.pdf_generator = PDFGenerator("C:/Users/obose/Documents/GitHub/ThreadsExpress", "C:/Users/obose/Documents/GitHub/ThreadsExpress")
        self.pdf_generator.pdf_operations.add_page()  # Add this line

    def test_filter_unsupported_chars(self):
        # Test the filter_unsupported_chars method
        text = "Sample text with unsupported characters: é"
        filtered_text = self.pdf_generator.filter_unsupported_chars(text)
        self.assertNotIn("é", filtered_text)

    def test_process_directory_with_files(self):
        # Test the process_directory method with files in the directory
        # Assuming you have some files in the 'test_directory'
        self.pdf_generator.process_directory("C:/Users/obose/Documents/GitHub/ThreadsExpress", False, None)
        self.assertTrue(self.pdf_generator.found_file)

    def test_generate_pdf(self):
        # Test the generate_pdf method
        self.pdf_generator.generate_pdf(False, None)
        # Assuming the output_path is 'output_path' and there is a file generated 'test_directory dir content.pdf'
        self.assertTrue(os.path.isfile("C:/Users/obose/Documents/GitHub/ThreadsExpress/ThreadsExpress dir content.pdf"))

if __name__ == '__main__':
    unittest.main()
