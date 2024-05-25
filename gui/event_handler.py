import os
from tkinter import messagebox
from pdf_generator.pdf_generator import PDFGenerator
from directory_structure_generator.directory_structure_generator import DirectoryStructureGenerator

class GUIEventHandler:
    def __init__(self, app):
        self.app = app 

    def handle_generate_pdf(self):
        inputs = self.app.input_frame.get_user_inputs()
        directory = inputs['directory']
        file_types = inputs['file_types']
        exclude_file_types = inputs['exclude_file_types']
        exclude_folders = inputs['exclude_folders']
        include_hidden = inputs['include_hidden']

        # 1. Input Validation:
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        for file_type in file_types or []:
            if not file_type.startswith("."):
                messagebox.showerror("Error", "File types must start with a '.' (e.g., .txt)")
                return

        for exclude_file_type in exclude_file_types or []:
            if not exclude_file_type.startswith("."):
                messagebox.showerror(
                    "Error", "Excluded file types must start with a '.' (e.g., .scmp)"
                )
                return

        # 2. Create Output Directory:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_folder_path = os.path.join(script_dir, "..", 'output')  # Go up two levels
        directory_name = os.path.basename(directory)
        output_subdir_path = os.path.join(output_folder_path, directory_name)
        os.makedirs(output_subdir_path, exist_ok=True)

        # 3. Update GUI and Start:
        self.app.output_frame.update_status("Processing files...")

        try:
            # 4. PDF Generation:
            pdf_generator = PDFGenerator(
                directory, output_subdir_path, exclude_folders=exclude_folders, exclude_file_types=exclude_file_types,
                ignore_file_path='ignore_folders.json'
            )
            result = pdf_generator.generate_pdf(
                include_hidden,
                file_types,
                progress_callback=self.app.output_frame.update_progress,
                feedback_callback=self.app.output_frame.add_feedback,
            )

            if result is True:
                print("PDF generated successfully!")
                self.app.output_frame.update_status("Generating directory structure...")

                dir_structure_gen = DirectoryStructureGenerator(directory, output_subdir_path, ignore_file_path='ignore_folders.json')
                dir_structure_gen.generate_directory_structure()

                print("Directory structure text file generated successfully!")
                self.app.output_frame.add_feedback("Directory structure text file generated successfully!")
                self.app.output_frame.update_status("Completed!")
                messagebox.showinfo("Success", "PDF and directory structure generated successfully!")
            elif result is False:  
                self.app.output_frame.update_status("No matching files found.")
                messagebox.showinfo("Info", "No matching files were found to generate a PDF.")
            elif isinstance(result, Exception):  # Check if result is an exception
                error_message = f"An error occurred during PDF generation: {result}"
                self.app.output_frame.add_feedback(error_message)
                raise Exception(error_message)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.app.output_frame.update_status("")  # Clear status message