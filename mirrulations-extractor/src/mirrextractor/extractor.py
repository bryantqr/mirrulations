import os
import time
import io
import pdfminer.high_level
import pdfminer.layout
import pikepdf
from datetime import datetime

class Extractor:
    """
    Class containing methods to extract text from files.
    """ 
    @staticmethod
    def extract_pdf(attachment_path, save_path):
        """
        This method takes a complete path to a pdf and stores the extracted text in the save_path.
        *Note* If a file exists at save_path, it will be overwritten.

        Parameters
        ----------
        attachment_path : str
            the complete file path for the attachment that is being extracted
            ex. /path/to/pdf/attachment_1.pdf
        save_path : str
            the complete path to store the extract text
            ex. /path/to/text/attachment_1.txt
        """
        print(f"Extracting text from {attachment_path}")
        try:
            pdf = pikepdf.open(attachment_path)
        except pikepdf.PdfError as e:
            if isinstance(e.inner_exception, pikepdf.ReadError):
                pdf = pikepdf.open(attachment_path, recover=True)
            else:
                print(f"FAILURE: failed to open {attachment_path}")
                return
        # Check if the PDF is already linearized
        # Linearize the PDF
        pdf.save(attachment_path, linearize=True)
        # Extract all text from the PDF using pdfminer.six
        with open(attachment_path, "rb") as f:
            pdf_bytes = io.BytesIO(f.read())
        text = pdfminer.high_level.extract_text(pdf_bytes)
        # Save the extracted text to a file
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"SUCCESS: Saved pdf at {save_path}")


if __name__ == '__main__':
    now = datetime.now()

    while True:
        for (root, dirs, files) in os.walk('/data'):
            for file in files:
                # Checks for pdfs
                if file.endswith('pdf'):
                    save_path = '' # TODO: generate path
                    if not save_path.is_file():
                        # extractor = Extractor(os.path.join(root, file), save_path)
                        Extractor.extract_pdf(os.path.join(root, file), save_path)
        
        # sleep for a hour
        current_time = now.strftime("%H:%M:%S")
        print(f"Sleeping for an hour : started at {current_time}")
        time.sleep(3600)