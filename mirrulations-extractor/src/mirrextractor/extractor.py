import os
import time
import io
import pdfminer
import pdfminer.high_level
import pikepdf
import json
from datetime import datetime
from mirrcore.path_generator import PathGenerator


class Extractor:
    """
    Class containing methods to extract text from files.
    """ 
    @staticmethod
    def extract_text(attachment_path, save_path):
        """
        This method takes a complete path to an attachment and determines which type of extraction
        will take place.
        *Note* save_path is for later use when saving the extracted text

        Parameters
        ----------
        attachment_path : str
            the complete file path for the attachment that is being extracted
            ex. /path/to/pdf/attachment_1.pdf
        save_path : str
            the complete path to store the extract text
            ex. /path/to/text/attachment_1.txt
        """
        # gets the type of the attachment file (ex. /path/to/pdf/attachment_1.pdf -> pdf)
        file_type = attachment_path[attachment_path.find('.') + 1 : len(attachment_path)]
        match file_type:
            case 'pdf':
                print(f"Extracting text from {attachment_path}")
                Extractor.extract_pdf(attachment_path, save_path)
            case _:
                print(f"FAILURE: attachment doesn't have appropriate extension {attachment_path}")


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
        try:
            pdf = pikepdf.open(attachment_path, allow_overwriting_input=True)
        except pikepdf.PdfError as e:
            if isinstance(e.inner_exception, pikepdf.ReadError):
                pdf = pikepdf.open(attachment_path, recover=True, allow_overwriting_input=True)
            else:
                print(f"FAILURE: failed to open {attachment_path}")
                return

        pdf_bytes = io.BytesIO()
        pdf.save(pdf_bytes, linearize=True)

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
                if not file.endswith('pdf'):
                    continue
                save_path = f"/data/data/{PathGenerator.get_attachment_text_save_path(json.dumps(file), file)}" # json dumps should be changed
                if not save_path.is_file():
                    complete_path = os.path.join(root, file)
                    start_time = time.time()
                    Extractor.extract_text(complete_path, save_path)
                    print(f"Time taken to extract text from {complete_path} is {start_time - time.time()} seconds")
        
        # sleep for a hour
        current_time = now.strftime("%H:%M:%S")
        print(f"Sleeping for an hour : started at {current_time}")
        time.sleep(3600)