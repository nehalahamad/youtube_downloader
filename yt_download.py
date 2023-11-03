# https://tkdocs.com/widgets/index.html
# https://tcl.tk/man/tcl8.6/TkCmd/contents.htm

from tkinter import *
# from tkinter import ttk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
from pytube import YouTube
from pytube import Playlist

from tkinter import filedialog

from icecream import ic

class DownloadFrameChild(ttk.Frame):
    def __init__(self, master, i, video_url):
        def on_progress(stream, chunk, bytes_remaining):
            file_size = stream.filesize
            bytes_downloaded = file_size - bytes_remaining
            progress = int((bytes_downloaded / file_size) * 100)
            self.progress_value.set(value=progress)
            root.update_idletasks()
        
        super().__init__(master)
        # self.pack(fill=ttk.X)
        self.pack(expand=True, fill=BOTH)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.progress_value = IntVar(value=2)
        self.yt = YouTube(video_url, on_progress_callback=on_progress)
        ttk.Checkbutton(self, text=self.yt.title, onvalue='yes', offvalue='no').grid(row=i, column=0, sticky=W)
        ttk.Progressbar(self, bootstyle="success", variable=self.progress_value, orient=HORIZONTAL, mode=DETERMINATE, length=60, value=20).grid(row=i, column=1, sticky=E, padx=3)
    

class DownloadFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # self.pack(expand=True, fill=BOTH)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure("Frame.TFrame", background="blue")
        self.config(style="Frame.TFrame")
        self.config(height = 50)
        self.onn = False
        self.yt_obj_list = []

    def add_items(self, url_list):
        for frame1 in self.yt_obj_list:
            frame1.destroy()
        self.yt_obj_list.clear()
        for i, video_url in enumerate(url_list) :
            dd = DownloadFrameChild(self, i, video_url)
            self.yt_obj_list.append(dd)
         

class PyTube:
    def __init__(self) -> None:
        self.url = StringVar()
        self.single_video_url = []
        self.p_list = []

    def get_playlist(self, var, index, mode):
        self.single_video_url.clear()
        self.p_list.clear()

        url = self.url.get()
        if 'playlist' in url:
            p = Playlist(url)
            for url in p.video_urls:#[:3]:
                self.p_list.append(url)
        else:
            self.single_video_url.append(url)

            if 'list' in url:
                p = Playlist(url)
                for link in p.video_urls:#[:3]:
                    self.p_list.append(link)

        first_download_frame.add_items(ptube.p_list)
        second_download_frame.add_items(ptube.single_video_url)



class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master) # this line is similar to "ttk.Frame(master)"
        self.pack(expand=True, fill=BOTH, padx=3, pady=3)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
# URL Frame
class FirstRowFrame(ttk.Frame):
    """URL row"""
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="URL", width=4).grid(row=0, column=0, sticky="EW")
        ptube.url.trace_add("write", ptube.get_playlist)
        ttk.Entry(self, textvariable=ptube.url, width=70).grid(row=0, column=1, columnspan=3, pady=3, sticky=(W, E))

# Save Path Frame
class SecondRowFrame(ttk.Frame):
    """Save path row"""
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="save path").grid(row=0, column=0, sticky="EW")
        # self.file_path = StringVar()
        self.path_entry = ttk.Entry(self, textvariable=file_path, width=50)
        self.path_entry.grid(row=0, column=1, padx=3, pady=3, sticky=(W, E))
        browse_button = ttk.Button(self, text="Browse", command=self.browse_file_location_path).grid(row=0, column=2, sticky=E)

    def browse_file_location_path(self):
        file_path.set(filedialog.askdirectory())
       
# Resolution and Checkbox Frame
class ThirdRowFrame(ttk.Frame):
    """Resolution row"""
    def __init__(self, master):
        self.master = master
        super().__init__(master)
        self.pack(fill=ttk.X, pady=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(5, weight=1)

        # 1 Label
        ttk.Label(self, text="Resolution: ").grid(row=0, column=0, sticky=W)

        # 2 Radio Buttons
        # self.resolution = StringVar()
        rbutton_360 = ttk.Radiobutton(self, text='360      ', variable=resolution, value=18).grid(row=0, column=1, sticky="EW")
        rbutton_720 = ttk.Radiobutton(self, text='720      ', variable=resolution, value=22).grid(row=0, column=2, sticky="EW")

        # 3 Checkbox button
        self.play_list = BooleanVar(value=False)
        check = ttk.Checkbutton(self, text='playlist', command=self.create_download_frame, variable=self.play_list)
        check.grid(row=0, column=8, columnspan=3, sticky='E')


    def create_download_frame(self):
        # https://www.youtube.com/watch?v=41qgdwd3zAg&list=PLS1QulWo1RIaJECMeUT4LFwJ-ghgoSH6n
        if self.play_list.get():
            second_download_frame.pack_forget()
            second_download_frame.onn = False
            first_download_frame.pack(expand=True, fill=BOTH)
            first_download_frame.onn = True
            
        else:
            first_download_frame.pack_forget()
            first_download_frame.onn = False
            second_download_frame.pack(expand=True, fill=BOTH)
            second_download_frame.onn = True
            
# Scrolled Frame
class FourthRowFrame(ScrolledFrame):
    def __init__(self, master):
        super().__init__(master, autohide=True)
        self.pack(expand=True, fill=BOTH)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

#Download Button Frame
class FifthRowFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=BOTTOM, fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        download_button = ttk.Button(self, text="Download", command=self.download).grid(row=0, column=8, columnspan=3, sticky=E)
    
    def download(self, *args):
        if first_download_frame.onn:
            for yt_progress_value_frame_obj in first_download_frame.yt_obj_list:
                mystream = yt_progress_value_frame_obj.yt.streams.get_by_itag(resolution.get())
                print('downloading: ', yt_progress_value_frame_obj.yt.title)
                mystream.download(output_path=file_path.get())

        elif second_download_frame.onn:
            pass

# ====================================================
class YTDownload:
    def __init__(self, root):
        self._root_configure(root)

        """
        s = ttk.Style()
        s.configure('MainFrame.TFrame', background='red', borderwidth=5, relief='raised')
        s.configure('FirstRowFrame.TFrame', background='green', borderwidth=5, relief='raised')
        s.configure('SecoondRowFrame.TFrame', background='blue', borderwidth=5, relief='raised')
        s.configure('ThirdRowFrame.TFrame', background='yellow', borderwidth=5, relief='raised')
        """

        mainframe = MainFrame(root)
        firstrowframe = FirstRowFrame(mainframe) #url
        secondrowframe = SecondRowFrame(mainframe)  #save path
        thirdrowframe = ThirdRowFrame(mainframe)  #Playlist

        fourthrowframe = FourthRowFrame(mainframe) #scrolled_frame

        global first_download_frame
        global second_download_frame
        first_download_frame = DownloadFrame(fourthrowframe)
        second_download_frame = DownloadFrame(fourthrowframe)
        second_download_frame.pack(expand=True, fill=BOTH)
        
        fifthrowframe = FifthRowFrame(mainframe) #Download


    
    def _root_configure(self, root):
        root.title("YouTube Downloader")
        # root.geometry("400x300")
        root.minsize(400,300)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)




root = ttk.Window(themename='journal')
# url = StringVar()
ptube = PyTube()
first_download_frame = ''
second_download_frame = ''
file_path = StringVar()
resolution = IntVar(value=22)

YTDownload(root)
root.mainloop()


"""
when link paster in url, then create play list -- trace_add() function

"""