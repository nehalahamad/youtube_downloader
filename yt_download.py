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
from concurrent.futures import ThreadPoolExecutor
from icecream import ic

class DownloadFrameChild(ttk.Frame):
    def __init__(self, master, i, video_url):
        def on_progress(stream, chunk, bytes_remaining):
            file_size = stream.filesize
            bytes_downloaded = file_size - bytes_remaining
            progress = int((bytes_downloaded / file_size) * 100)
            self.progress_value.set(value=progress)
        
        super().__init__(master)
        self.grid(row=i, column=0, sticky="EW")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.progress_value = IntVar(value=2)
        self.yt = YouTube(video_url, on_progress_callback=on_progress)
        self.label = ttk.Label(self, text=f"{i+1}: {self.yt.title}", background='#edf0ee'*((i+1)%2))
        self.label.grid(row=0, column=0, sticky="EW")
        ttk.Progressbar(self, bootstyle="success", variable=self.progress_value, orient=HORIZONTAL, mode=DETERMINATE, length=60, value=20).grid(row=0, column=1, sticky=E, padx=13)
        

class DownloadFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.onn = False
        self.yt_obj_list = []

    def add_items(self, url_list):
        for frame1 in self.yt_obj_list:
            frame1.destroy()
        self.yt_obj_list.clear()
        # -----------------------------------------------------
        self.yt_obj_list = [-1] * len(url_list) #initializing the lenth of  yt_obj_list
        pool = ThreadPoolExecutor(max_workers=25)
        pool.map(self._add_items, range(len(url_list)), url_list)
        # -----------------------------------------------------
    def _add_items(self, i, video_url):
        dd = DownloadFrameChild(self, i, video_url)
        self.yt_obj_list[i] = dd


         

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
            for url in p.video_urls:
                self.p_list.append(url)
        else:
            self.single_video_url.append(url)

            if 'list' in url:
                p = Playlist(url)
                for link in p.video_urls:
                    self.p_list.append(link)

        first_download_frame.add_items(ptube.p_list)
        second_download_frame.add_items(ptube.single_video_url)

    def download(self, *args):
        pool = ThreadPoolExecutor(max_workers=3)
        if first_download_frame.onn:
            # ------------------------------------------------------------------------------
            pool.map(self._download, first_download_frame.yt_obj_list)
            # ------------------------------------------------------------------------------

        elif second_download_frame.onn:
            pool.map(self._download, second_download_frame.yt_obj_list)

            # for yt_progress_value_frame_obj in second_download_frame.yt_obj_list:
                # self._download(yt_progress_value_frame_obj)

    def _download(self, yt_progress_value_frame_obj):
        try:
            mystream = yt_progress_value_frame_obj.yt.streams.get_by_itag(resolution.get())
            yt_progress_value_frame_obj.label['text'] += f' | {mystream.filesize_mb:.2f}MB'
            mystream.download(output_path=file_path.get())
            root.update_idletasks()
        except Exception as e:
            print(e)

# -----------------------------------------------------------------------------------
class MainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master) # this line is similar to "ttk.Frame(master)"
        self.pack(expand=True, fill=BOTH, padx=3, pady=3)
        

class URLFrame(ttk.Frame):
    """URL row"""
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="URL", width=4).grid(row=0, column=0, sticky="EW")
        ptube.url.trace_add("write", ptube.get_playlist)
        ttk.Entry(self, textvariable=ptube.url, width=70).grid(row=0, column=1, columnspan=3, pady=3, sticky=(W, E))


class SavePathFrame(ttk.Frame):
    """Save path row"""
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        ttk.Label(self, text="Save Path").grid(row=0, column=0, sticky="EW")
        ttk.Entry(self, textvariable=file_path, width=50).grid(row=0, column=1, padx=3, pady=3, sticky=(W, E))
        ttk.Button(self, text="Browse", command=self.browse_file_location_path).grid(row=0, column=2, sticky=E)

    def browse_file_location_path(self):
        file_path.set(filedialog.askdirectory())
       

class ResolutionAndPlaylistCheckboxFrame(ttk.Frame):
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
        ttk.Radiobutton(self, text='360      ', variable=resolution, value=18).grid(row=0, column=1, sticky="EW")
        ttk.Radiobutton(self, text='720      ', variable=resolution, value=22).grid(row=0, column=2, sticky="EW")
        # 3 Checkbox button
        self.play_list = BooleanVar(value=False)
        check = ttk.Checkbutton(self, text='playlist', command=self.create_download_frame, variable=self.play_list)
        check.grid(row=0, column=8, columnspan=3, sticky='E')


    def create_download_frame(self):
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
            

class YoutubeContentFrame(ScrolledFrame):
    def __init__(self, master):
        super().__init__(master, autohide=True)
        self.pack(expand=True, fill=BOTH)


class DownloadButtonFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(side=BOTTOM, fill=ttk.X)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.download_label = ttk.Label(self, text='---')
        self.download_label.pack(side=LEFT)

        self.download_button = ttk.Button(self, text="Download", command=ptube.download).pack(side=RIGHT)
    
# ====================================================
class YTDownload:
    def __init__(self, root):
        self._root_configure(root)
        mainframe = MainFrame(root)

        self.url_frame = URLFrame(mainframe)
        self.save_path_frame = SavePathFrame(mainframe)
        self.resolution_frame = ResolutionAndPlaylistCheckboxFrame(mainframe)

        yt_content_frame = YoutubeContentFrame(mainframe) #scrolled_frame

        global first_download_frame
        global second_download_frame
        first_download_frame = DownloadFrame(yt_content_frame)
        second_download_frame = DownloadFrame(yt_content_frame)
        second_download_frame.onn = True
        second_download_frame.pack(expand=True, fill=BOTH)
        
        self.download_frame = DownloadButtonFrame(mainframe)

    def _root_configure(self, root):
        root.title("Nehal's YT Downloader")
        root.minsize(400,300)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

# ==================================================================
root = ttk.Window(themename='journal')
ptube = PyTube()
first_download_frame = ''
second_download_frame = ''
file_path = StringVar()
resolution = IntVar(value=22)

yt_app = YTDownload(root)
root.mainloop()