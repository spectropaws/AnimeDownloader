import tkinter


class MainWindow:
    def __init__(self):
        self.window = tkinter.Tk()
        self.width = 700
        self.height = 480
        self.base_url = tkinter.StringVar(self.window)
        self.folder_name = tkinter.StringVar(self.window)
        self.episode_start = tkinter.StringVar(self.window)
        self.episode_end = tkinter.StringVar(self.window)
        self.server = tkinter.IntVar(self.window)

    # set up the main interface
    def setup_window(self, main_process: callable):

        self.window.geometry(f"{self.width}x{self.height}")
        self.window.resizable(False, False)
        self.window.title("Anime Downloader")

        label_frame = tkinter.Frame(self.window)
        url_frame = tkinter.Frame(self.window)
        divide_frame = tkinter.Frame(self.window)
        anime_frame = tkinter.Frame(divide_frame)
        episode_frame = tkinter.Frame(divide_frame)
        server_frame = tkinter.Frame(self.window)
        button_frame = tkinter.Frame(self.window)

        label_frame.grid(row=0, column=0)
        url_frame.grid(row=1, column=0)
        divide_frame.grid(row=2, column=0)
        server_frame.grid(row=3, column=0, pady=(20, 0))
        button_frame.grid(row=4, column=0)
        anime_frame.grid(row=0, column=0, padx=(0, 30))
        episode_frame.grid(row=0, column=1, padx=(30, 0))

        tkinter.Label(label_frame, text="Anime Downloader", font=("Century Gothic", 16), width=57,
                      height=3).grid(row=0, column=0, sticky="nsew")

        tkinter.Label(url_frame, text="Base URL: ", height=1, width=20).grid(padx=(20, 5), pady=(20, 0), row=0,
                                                                             column=0)
        tkinter.Entry(url_frame, textvariable=self.base_url, width=50,
                      font=("Century Gothic", 10)).grid(row=0, column=1, padx=(0, 20), pady=(20, 0))

        tkinter.Label(anime_frame, text="Anime name:  ", height=1).grid(row=0, column=0, padx=(10, 5), pady=30,
                                                                        sticky="e")
        tkinter.Entry(anime_frame, textvariable=self.folder_name,
                      font=("Century Gothic", 12)).grid(row=0, column=1, pady=30, padx=(0, 20))

        tkinter.Label(episode_frame, text="Episode range:  ", height=1).grid(row=0, column=0, padx=5, pady=30)
        tkinter.Entry(episode_frame, textvariable=self.episode_start, font=("Century Gothic", 12),
                      width=4).grid(row=0, column=1, pady=30, padx=5, sticky="w")
        tkinter.Label(episode_frame, text="  -  ", height=1, font=("Times", 20)).grid(row=0, column=2, padx=5, pady=30)
        tkinter.Entry(episode_frame, textvariable=self.episode_end, font=("Century Gothic", 12),
                      width=4).grid(row=0, column=3, pady=30, padx=(5, 10), sticky="w")

        tkinter.Label(server_frame, text="Choose server", height=1, font=("Times", 14)).grid(row=0, column=0, pady=10)
        tkinter.Radiobutton(server_frame, variable=self.server, value=1, text="goload.pro",
                            font=("Times", 12)).grid(row=1, column=0, pady=(0, 10))
        tkinter.Radiobutton(server_frame, variable=self.server, value=2, font=("Times", 12),
                            text="streamsb (slow but avoids recaptcha)").grid(row=1, column=1, pady=(0, 10),
                                                                              padx=(30, 0))

        tkinter.Button(button_frame, text="Download", font=("Century Gothic", 16), command=main_process,
                       width=20, height=2).grid(row=0, column=0, padx=20, pady=(40, 0))

    def hide(self):
        self.window.withdraw()

    def show(self):
        self.window.deiconify()

    def set_pos(self, x, y):
        self.window.geometry(f"+{int(x)}+{int(y)}")
