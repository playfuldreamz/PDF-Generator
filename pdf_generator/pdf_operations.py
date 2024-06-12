from fpdf import FPDF

class PDFOperations:
    def __init__(self):
        self.pdf = FPDF()
        self.margin = 10
        self.processed_files = 0

    def add_page(self):
        self.pdf.add_page()

    def set_font(self, family, size=12):
        self.pdf.set_font(family, size=size)

    def add_text(self, text, align='L'):
        effective_page_width = self.pdf.w - 2*self.margin  # Calculate the effective page width
        self.pdf.multi_cell(effective_page_width, 10, txt=text, align=align)
        return self  # Return self to allow method chaining

    def add_line_break(self):
        self.pdf.ln(10)

    def save_pdf(self, output_path):
        self.pdf.output(output_path)
