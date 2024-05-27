import unittest
import os
import shutil
import tempfile

from pdf_generator.pdf_generator import PDFGenerator
from pypdf import PdfReader

class TestPDFGenerator(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()  # Create a temporary directory for testing
        self.output_dir = os.path.join(self.test_dir, 'output')
        os.makedirs(self.output_dir, exist_ok=True)

        # Create some test files
        self.create_test_file("file1.txt", "This is a test file.")
        self.create_test_file("file2.py", "print('Hello, world!')")
        self.create_test_file("file3.md", "# Test Markdown File")
        self.create_test_file(".hidden_file.txt", "This is a hidden file.")

        # Create a subdirectory
        self.subdir = os.path.join(self.test_dir, "subdir")
        os.makedirs(self.subdir, exist_ok=True)
        self.create_test_file(os.path.join(self.subdir, "subfile.txt"), "Content of subfile.")

    def tearDown(self):
        # Clean up the temporary directory after each test
        shutil.rmtree(self.test_dir)

    def create_test_file(self, file_name, content, encoding='utf-8'):
        """Helper function to create test files."""
        file_path = os.path.join(self.test_dir, file_name)
        with open(file_path, 'w', encoding=encoding) as f:
            f.write(content)

    def test_generate_pdf_no_file_types(self):
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir)
        result = pdf_generator.generate_pdf(False, None)
        self.assertTrue(result, "PDF generation failed unexpectedly.")

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.test_dir, f"{temp_dir_name} dir content.pdf")
        self.assertTrue(os.path.isfile(output_pdf), "PDF file not found.")
        self.assert_pdf_content(output_pdf, [
            "file1.txt", "This is a test file.",
            "file2.py", "print('Hello, world!')", 
            "file3.md", "# Test Markdown File",
            "subdir", "subfile.txt", "Content of subfile."
        ])

    def test_generate_pdf_specific_file_types(self):
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir)
        result = pdf_generator.generate_pdf(False, [".txt", ".md"])
        self.assertTrue(result)

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.test_dir, f"{temp_dir_name} dir content.pdf") 
        self.assert_pdf_content(
            output_pdf,
            ["file1.txt", "This is a test file.", "file3.md", "# Test Markdown File", "subdir", "subfile.txt", "Content of subfile."],
        )

    def test_generate_pdf_include_hidden(self):
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir)
        result = pdf_generator.generate_pdf(True, None)
        self.assertTrue(result)

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.test_dir, f"{temp_dir_name} dir content.pdf") 
        self.assert_pdf_content(
            output_pdf,
            ["file1.txt", "This is a test file.", "file2.py", "print('Hello, world!')", "file3.md", "# Test Markdown File", ".hidden_file.txt", "This is a hidden file.", "subdir", "subfile.txt", "Content of subfile."],
        )

    def test_generate_pdf_exclude_folders(self):
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir, exclude_folders=['subdir'])
        result = pdf_generator.generate_pdf(False, None)
        self.assertTrue(result)

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.test_dir, f"{temp_dir_name} dir content.pdf")
        self.assert_pdf_content(
            output_pdf,
            ["file1.txt", "This is a test file.", "file2.py", "print('Hello, world!')", "file3.md", "# Test Markdown File"],
        )

    def test_generate_pdf_exclude_file_types(self):
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir, exclude_file_types=['.py'])
        result = pdf_generator.generate_pdf(False, None)  
        self.assertTrue(result)

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.test_dir, f"{temp_dir_name} dir content.pdf") 
        self.assert_pdf_content(
            output_pdf,
            ["file1.txt", "This is a test file.", "file3.md", "# Test Markdown File", "subdir", "subfile.txt", "Content of subfile."],
        )

    def test_generate_pdf_empty_directory(self):
        empty_dir = os.path.join(self.test_dir, 'empty_dir')
        os.makedirs(empty_dir, exist_ok=True)
        pdf_generator = PDFGenerator(empty_dir, self.test_dir)
        result = pdf_generator.generate_pdf(False, None)
        self.assertTrue(result)  # Should complete without errors

    def test_generate_pdf_encoding_error(self):
        self.create_test_file("file4.txt", "Non-UTF-8 content", encoding='latin-1')
        pdf_generator = PDFGenerator(self.test_dir, self.test_dir)
        result = pdf_generator.generate_pdf(False, None)  # Process all file types
        self.assertTrue(result)  # Should complete but skip the file with encoding error

    def assert_pdf_content(self, pdf_path, expected_content):
        """Asserts that the PDF file contains the expected content strings."""
        with open(pdf_path, 'rb') as f:
            pdf_reader = PdfReader(f)
            num_pages = len(pdf_reader.pages)
            pdf_text = ""
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                pdf_text += page.extract_text()

        for content_string in expected_content:
            self.assertIn(content_string, pdf_text,
                          f"Expected content '{content_string}' not found in PDF.")