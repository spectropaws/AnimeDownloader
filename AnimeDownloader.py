import DownloadHandler
import GUIHandler
import tkinter
import threading
import mttkinter


def prevent_exit():
    pass


def main_process():

    def quit_application():
        window.destroy()
        root.window.destroy()

    anime = DownloadHandler.Anime(root.base_url.get(), root.folder_name.get(), root.server.get(),
                                  (int(root.episode_start.get()), int(root.episode_end.get())))

    window = tkinter.Tk()
    window.title('Progress')
    window.config(width=500)
    window.geometry(f"+{int(screen_width/2 - 250)}+200")
    window.withdraw()
    root.hide()

    window.after(50, lambda: threading.Thread(target=anime.start_download, args=(window,)).start())
    window.protocol("WM_DELETE_WINDOW", prevent_exit)
    window.bind("<<exit_event>>", lambda e: quit_application())
    window.mainloop()


if __name__ == "__main__":
    root = GUIHandler.MainWindow()
    root.setup_window(main_process)

    screen_height = root.window.winfo_screenheight()
    screen_width = root.window.winfo_screenwidth()

    y_cord = screen_height/2 - root.height/2
    x_cord = screen_width/2 - root.width/2

    root.set_pos(x_cord, y_cord)
    root.window.mainloop()

# Creator: Spectropaws.X

"""
Working:

1. program asks for base url for anime to iterate over it for multiple episodes

2. program asks for anime folder name to save episodes in and range of episodes to download

3. program asks for server to download from...
    use goload.pro for faster download link search (very slow download speed)
    use streamsb when recaptcha is preventing goload.pro from displaying download links
    
4. program fetches download urls from the specified server 
    goload.pro takes 5-7 seconds to load url
    streamsb takes nearly 17 seconds to generate url for each episode (avoid if you are downloading more than 25
    
5. program starts a new thread if active_threads < Maximum_parallel_downloads
    each thread calls download_anime(links, indexes) function that requests for video and downloads it in chunks of 5mb
    
Note: program uses mttkinter to update progress bars in threads
"""

# TODO complete final update
