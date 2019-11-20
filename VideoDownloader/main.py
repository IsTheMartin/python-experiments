import pytube
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from decimal import Decimal
import re

url = ""
downloadPath = ""


class Application(tk.Frame):

    video = None

    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Video Downloader")

        self.lblUrl = ttk.Label(main_window, text="Paste url:")
        self.lblUrl.place(x=10, y=10)
        
        self.txtUrl = ttk.Entry(main_window)
        self.txtUrl.place(x=100, y=10)

        self.btnAnalyzer = ttk.Button(main_window, text="Analize", command=self.analizeUrl)
        self.btnAnalyzer.place(x=10, y=40)

        self.lblTitle = ttk.Label(main_window, text="Title: ")
        self.lblTitle.place(x=10, y=80)

        self.lblDuration = ttk.Label(main_window, text="Duration: ")
        self.lblDuration.place(x=10, y=100)

        self.cmbStreams = ttk.Combobox(main_window, width=70)
        self.cmbStreams.place(x=10, y=120)

        self.btnDownload = ttk.Button(main_window, text="Download", command=self.downloadMedia)
        self.btnDownload.place(x=10, y=150)

        main_window.configure(width=500, height=300)
        self.place(width=300, height=200)

    
        print(str(100))

    def analizeUrl(self):
        if self.txtUrl.get() != "":
            try:

                url = self.txtUrl.get()
                self.video = pytube.YouTube(url=url, on_progress_callback=self.showProgressBar)

                #self.lblTitle.config(text="Title: " + str(video.player_config_args['title']))
                duration = Decimal(self.video.length) / 60
                self.lblDuration.config(text="Duration: " + str(duration) + " minutes")
                self.populateStreams(self.video.streams.all())
            except NameError as err:
                print(messagebox.showwarning(message=str(err)))
        else:
            print(messagebox.showwarning(message="Cannot analize url", title="Warning"))

    def populateStreams(self, streams):
        self.cmbStreams["values"] = streams

    def show(self):
        pass

    def downloadMedia(self):
        if self.cmbStreams.current() > -1 and self.video is not None:
            try:
                itag = re.search('itag="(.*)" mime', self.cmbStreams.get())
                self.video.register_on_progress_callback(self.showProgressBar)
                self.video.streams.get_by_itag(itag.group(1)).download()
            except NameError as err:
                print(messagebox.showwarning(message=str(err)))
        else:
            pass
                
    def showProgressBar(self, stream=None, chunk=None, file_handle=None, bytes_remaining=None):
        print("")

main_window = tk.Tk()
app = Application(main_window)
app.mainloop()