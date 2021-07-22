import pytesseract
from pdf2image import convert_from_path
import time
import os
from pathlib import Path
from tkinter import Tk, TclError
from tkinter import messagebox as msg
import re
import win32api
import win32file
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class Handler(FileSystemEventHandler):        
    def on_created(self, event):
        if event.is_directory:
            print ("directory created")
        else: # not event.is_directory
            Fname, Extension = os.path.splitext(os.path.basename(event.src_path))
            if Extension == '.pdf':
                ps=re.compile("\d{2}([0]\d|[1][0-2])([0][1-9]|[1-2]\d|[3][0-1])[-]*[1-4]\d{6}")
                root= Tk()
                root.withdraw()
                print ("pdf 파일 복사를 탐지하였습니다.")
                print ("민감한 데이터 포함 여부를 확인중입니다....")
                images = convert_from_path(event.src_path)
                images[0].save('res.jpg','JPEG')
                pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
                text=pytesseract.image_to_string(r'res.jpg',lang='kor')
                #print("pdf파일 복사 시도 탐지")
                res=ps.search(text)
                if res!=None:
                    msg.showerror('경고', 'pdf 파일에서 주민번호를 탐지하였습니다.')
                        #print("%s"%(event.src_path))
                
                    

class Watcher:
    def __init__(self, path):
        print ("file copy detecting....")
        self.event_handler = None     
        self.observer = Observer() 
        self.target_directory = path
        self.currentDirectorySetting()


    def currentDirectorySetting(self):
        print ("watching directory =", end="")
        os.chdir(self.target_directory)
        print ("{cwd}".format(cwd = os.getcwd()))
        print ("--------------------------------------")

 
    def run(self):
        self.event_handler = Handler()
        self.observer.schedule(
            self.event_handler,
            self.target_directory,
            recursive=False
        )

        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt as e:
            self.observer.stop() 
while True:
    drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
    time.sleep(1)
    if len(drives)>=3:
        new_drive=drives[-1]
        myWatcher = Watcher(new_drive)
        myWatcher.run()
