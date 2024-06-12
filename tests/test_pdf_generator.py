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
            
    def test_generate_pdf_no_matching_files(self):
        """Tests when no files match the specified file types."""
        pdf_generator = PDFGenerator(self.test_dir, self.output_dir)
        result = pdf_generator.generate_pdf(False, [".docx"])  # Provide an uncommon file type
        self.assertFalse(result, "Expected PDF generation to return False as no matching files found.")
        
    def test_generate_pdf_with_empty_file(self):
        """Tests processing a directory with an empty file."""
        self.create_test_file("empty_file.txt", "")  # Create an empty file
        pdf_generator = PDFGenerator(self.test_dir, self.output_dir)
        result = pdf_generator.generate_pdf(False, None)
        self.assertTrue(result, "PDF generation failed unexpectedly.")
        
        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.output_dir, f"{temp_dir_name} dir content.pdf")
        self.assert_pdf_content(output_pdf, ["empty_file.txt"])  # Check if the filename is present
        
    def test_generate_pdf_exclude_files_without_extension(self):
        """Tests excluding files without extensions."""
        self.create_test_file("no_extension", "Content of file without extension")
        pdf_generator = PDFGenerator(self.test_dir, self.output_dir, exclude_file_types=["text"])
        result = pdf_generator.generate_pdf(False, None)  # Process all files
        self.assertTrue(result, "PDF generation failed unexpectedly.")

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.output_dir, f"{temp_dir_name} dir content.pdf")
        self.assertNotIn("no_extension", self.get_text_from_pdf(output_pdf),
                         "File without extension should be excluded")
        
    def test_generate_pdf_multiple_nested_directories(self):
        """Tests processing multiple levels of nested directories."""
        subsubdir = os.path.join(self.subdir, "subsubdir")
        os.makedirs(subsubdir, exist_ok=True)
        self.create_test_file(os.path.join(subsubdir, "nested_file.txt"), "Nested file content.")

        pdf_generator = PDFGenerator(self.test_dir, self.output_dir)
        result = pdf_generator.generate_pdf(False, None)
        self.assertTrue(result, "PDF generation failed unexpectedly.")

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.output_dir, f"{temp_dir_name} dir content.pdf")
        self.assert_pdf_content(output_pdf, ["subdir", "subsubdir", "nested_file.txt", "Nested file content."])

    def test_generate_pdf_ignore_folders(self):
        """Test if specified folders are ignored."""
        ignore_folder_name = "ignore_this"
        ignore_folder_path = os.path.join(self.test_dir, ignore_folder_name)
        os.makedirs(ignore_folder_path, exist_ok=True)
        self.create_test_file(os.path.join(ignore_folder_path, "ignored_file.txt"), "This file should be ignored.")

        pdf_generator = PDFGenerator(self.test_dir, self.output_dir, ignore_file_path="tests/test_ignore_folders.json")
        result = pdf_generator.generate_pdf(False, None)

        self.assertTrue(result, "PDF generation failed unexpectedly.")

        temp_dir_name = os.path.basename(self.test_dir)
        output_pdf = os.path.join(self.output_dir, f"{temp_dir_name} dir content.pdf")
        pdf_text = self.get_text_from_pdf(output_pdf)

        self.assertNotIn(ignore_folder_name, pdf_text, "Ignored folder found in the PDF")
        self.assertNotIn("ignored_file.txt", pdf_text, "File from ignored folder found in the PDF")

    def get_text_from_pdf(self, pdf_path):
        """Helper to extract text from a PDF."""
        with open(pdf_path, 'rb') as f:
            pdf = PdfReader(f)
            num_pages = len(pdf.pages)
            pdf_text = ""
            for page_num in range(num_pages):
                page = pdf.pages[page_num]
                pdf_text += page.extract_text()
            return pdf_text

    def test_get_total_file_count_empty_directory(self):
        """Tests get_total_file_count() with an empty directory."""
        empty_dir = tempfile.mkdtemp()  # Create a new empty directory
        pdf_generator = PDFGenerator(empty_dir, self.output_dir)
        count = pdf_generator.get_total_file_count()
        shutil.rmtree(empty_dir)  # Clean up temporary directory
        self.assertEqual(count, 0, "Expected count to be 0 for an empty directory.")