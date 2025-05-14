import argparse
import os
from helpers.wordtools import generate_pdf
from pypdf import PdfReader, PdfWriter


def merge_pdf(original_filename, sign_file, no_sign_file):
    try:
        writer = PdfWriter()

        reader1 = PdfReader(sign_file)
        for page in reader1.pages:
            writer.add_page(page)

        reader2 = PdfReader(no_sign_file)
        last_page = reader2.pages[-1]
        writer.add_page(last_page)

        with open(f"{original_filename}.pdf", "wb") as f_out:
            writer.write(f_out)
        print(f"COMPLETE: save to {original_filename}.pdf")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="Convert DOCX to PDF")
    parser.add_argument("-i", "--input_path", required=True, help="Path to DOCX file")
    args = parser.parse_args()
    original_filename, sign_file, no_sign_file = generate_pdf(args.input_path)
    merge_pdf(original_filename,sign_file, no_sign_file)

    os.remove(sign_file)
    os.remove(no_sign_file)


if __name__ == "__main__":
    main()
