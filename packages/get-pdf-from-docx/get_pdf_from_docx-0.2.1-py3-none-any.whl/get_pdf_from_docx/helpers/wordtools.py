import datetime
import os
import win32com.client


ID_OF_PDF_FILE_TYPE = 17
ID_OF_TEXTBOX_TYPE_IN_DOCX = 17
wdColorBlack = 0
wdColorWhite = 16777215  # BGR color


def change_text_color_of_sign_box(doc, color):
    for shape in doc.Shapes:
        if shape.Type == ID_OF_TEXTBOX_TYPE_IN_DOCX:
            text = shape.TextFrame.TextRange.Text
            if text.startswith("ตรวจ"):
                shape.TextFrame.TextRange.Font.Color = color
    return doc


def generate_pdf(input_path):
    try:
        print(f"INFO: docx input = {input_path}")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        original_filename = os.path.splitext(os.path.basename(input_path))[0]
        output_path_sign = os.path.abspath(f"{current_time}_sign.pdf")
        output_path_no_sign = os.path.abspath(f"{current_time}_no_sign.pdf")

        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False

        doc = word.Documents.Open(os.path.abspath(input_path))
        doc = change_text_color_of_sign_box(doc, wdColorBlack)
        doc.SaveAs(output_path_sign, FileFormat=ID_OF_PDF_FILE_TYPE)
        doc.Close(False)

        doc = word.Documents.Open(os.path.abspath(input_path))
        doc = change_text_color_of_sign_box(doc, wdColorWhite)
        doc.SaveAs(output_path_no_sign, FileFormat=ID_OF_PDF_FILE_TYPE)
        doc.Close(False)

        word.Quit()
        print(f"INFO: pdf(s) output {current_time}.pdf")
        return original_filename, output_path_sign, output_path_no_sign
    except Exception as e:
        print(f"Error: {e}")
