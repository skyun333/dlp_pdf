import pytesseract
from pdf2image import convert_from_path
import pyperclip
import time
import os
from pathlib import Path
from tkinter import Tk, TclError
from tkinter import messagebox as msg
import re
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def convert_pdf_to_txt(my_path):
    output_string = StringIO()
    with open(my_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()

def get_clipboard_as_path():
    root = Tk()
    root.withdraw()
    try:
        content = root.selection_get(selection="CLIPBOARD")
    except TclError:
        return None
    finally:
        root.destroy()
    file = Path(content)
    try:
        if file.exists():
            return file
    except OSError:
        pass
    return None
ps=re.compile("\d{2}([0]\d|[1][0-2])([0][1-9]|[1-2]\d|[3][0-1])[-]*[1-4]\d{6}")

root= Tk()
root.withdraw()
while True:
    my_path = get_clipboard_as_path()
    if my_path:
        my_path=str(my_path)
        
        #print(my_path)
        fname, ext = os.path.splitext(my_path)
        if ext==(".pdf"):
            images = convert_from_path(my_path)
            images[0].save('res.jpg','JPEG')
            pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
            text=pytesseract.image_to_string(r'res.jpg',lang='kor')
            #print(text)
            #print("pdf파일 복사 시도 탐지")
            res=ps.search(text)
            if res!=None:
                msg.showerror('경고', 'pdf 파일에서 주민번호를 탐지하였습니다.')
                pyperclip.copy('')
    time.sleep(0.2)
