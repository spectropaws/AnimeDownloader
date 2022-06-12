import time
import requests
import os
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import tkinter
from tkinter import ttk
from tkinter import messagebox
import mttkinter

# 5 uses nearly 70 mb of RAM
Maximum_parallel_downloads = 10

# change brave's location if not in 'Program Files' or want to use chrome
browser_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Referer": ""}


def fetch_urls(num):
    global server
    global first_run
    if server.get() == 1:
        page = requests.get(base_url.get() + str(num)).content
        soup = BeautifulSoup(page, 'html.parser')
        options = Options()
        options.binary_location = browser_location
        options.add_argument("--incognito")
        download_page = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        download_page.minimize_window()
        download_page.get(soup.select_one("li.dowloads a").attrs['href'])  # web developer hasn't corrected the typo yet
        soup = BeautifulSoup(download_page.page_source, 'html.parser')
        download_links = soup.select("div.mirror_link div.dowload a")      # web developer hasn't corrected the typo yet
        download_link = ""
        string_1080p = """Download
                        (1080P - mp4)"""
        for link in download_links:
            if link.string == string_1080p:
                download_link = link.attrs['href']
        return download_link

    elif server.get() == 2:
        page = requests.get(base_url.get() + str(num)).content
        soup = BeautifulSoup(page, 'html.parser')
        streamsb_video_link_raw = soup.select_one("li.streamsb a").attrs['data-video']
        temp = streamsb_video_link_raw.split('/')
        streamsb_page_name = temp[len(temp) - 1]
        options = Options()
        options.binary_location = browser_location
        options.add_argument("--incognito")

        download_page = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        download_page.minimize_window()
        download_page.get('https://sbplay2.xyz/d/' + streamsb_page_name)

        try:
            # download_page.find_element_by_link_text("High quality").click()
            download_page.execute_script("arguments[0].click();",
                                         download_page.find_element(By.LINK_TEXT, "High quality"))
        except selenium.common.exceptions.NoSuchElementException:
            try:
                # download_page.find_element_by_link_text("Normal quality").click()
                download_page.execute_script('arguments[0].click();',
                                             download_page.find_element(By.LINK_TEXT, "Normal quality"))
            except selenium.common.exceptions.NoSuchElementException:
                return ""

        if not first_run:
            time.sleep(10)
        download_page.execute_script('arguments[0].click();',
                                     download_page.find_element(By.CLASS_NAME, "g-recaptcha"))
        try:
            WebDriverWait(download_page, 20).until(
                expected_conditions.presence_of_element_located((By.XPATH,
                                                                 "// a[contains(text(),'Direct Download Link')]"))
            )
            download_link = download_page.find_element(By.XPATH, "// a[contains(text(),'Direct Download Link')]"). \
                get_attribute('href')
            return download_link
        except selenium.common.exceptions.TimeoutException:
            return ''


def main_process():

    def prevent_exit():
        pass

    def start_download_threads():
        threads = []
        for i in range(len(download_list)):
            if download_list[i] == '':
                messagebox.showerror("Not found!", f"Episode {download_indexes[i]} 1080p Not found! skipping...")
            else:
                t = threading.Thread(target=download_anime, args=(download_list[i], download_indexes[i]))
                threads.append(t)
                t.start()
                time.sleep(0.1)
                if threading.active_count() > Maximum_parallel_downloads + 1:
                    t.join()
        for thread in threads:
            thread.join()
        window.event_generate("<<exit_event>>")
        root.event_generate("<<exit_event>>")

    def download_anime(url, num):
        video = requests.get(url, headers=headers, stream=True)

        frame = tkinter.Frame(window)
        frame.pack(fill=tkinter.X, pady=10, padx=10)
        tkinter.Label(frame, text=f"Episode {num}").grid(row=0, column=0)
        progress_bar = ttk.Progressbar(frame, orient=tkinter.HORIZONTAL, mode="determinate", length=350)
        progress_bar.grid(row=0, column=1)
        progress_bar['maximum'] = int(float(video.headers['Content-Length']) / (1024 * 1024))
        with open(f"{anime_folder_name}\\Episode {num}.mp4", "wb") as file:
            for chunk in video.iter_content(1024 * 1024 * 5):
                if chunk:
                    file.write(chunk)
                    progress_bar['value'] += int(len(chunk) / (1024 * 1024))
                    window.update_idletasks()
        frame.destroy()

    anime_folder_name = folder_name.get()
    server_id = server.get()
    window = tkinter.Tk()
    window.title('Progress')
    window.config(width=500)

    root.withdraw()
    if not os.path.isdir(anime_folder_name):
        os.mkdir(anime_folder_name)

    download_indexes = [num for num in range(int(episode_start.get()), int(episode_end.get()) + 1)]
    download_list = []
    for index in range(int(episode_start.get()), int(episode_end.get()) + 1):
        download_list.append(fetch_urls(index))

    if server_id == 1:
        headers['Referer'] = "https://goload.pro/"
    elif server_id == 2:
        headers['Referer'] = "https://sbplay2.xyz"

    window.after(50, threading.Thread(target=start_download_threads).start)
    window.protocol("WM_DELETE_WINDOW", prevent_exit)
    window.bind("<<exit_event>>", lambda e: window.quit())
    window.mainloop()


first_run = True

root = tkinter.Tk()

root.geometry("700x480")
root.resizable(False, False)
root.title("Anime Downloader")
label_frame = tkinter.Frame(root)
url_frame = tkinter.Frame(root)
divide_frame = tkinter.Frame(root)
anime_frame = tkinter.Frame(divide_frame)
episode_frame = tkinter.Frame(divide_frame)
server_frame = tkinter.Frame(root)
button_frame = tkinter.Frame(root)
label_frame.grid(row=0, column=0)
url_frame.grid(row=1, column=0)
divide_frame.grid(row=2, column=0)
server_frame.grid(row=3, column=0, pady=(20, 0))
button_frame.grid(row=4, column=0)
anime_frame.grid(row=0, column=0, padx=(0, 30))
episode_frame.grid(row=0, column=1, padx=(30, 0))

base_url = tkinter.StringVar(root)
folder_name = tkinter.StringVar(root)
episode_start = tkinter.StringVar(root)
episode_end = tkinter.StringVar(root)
server = tkinter.IntVar(root)

tkinter.Label(label_frame, text="Anime Downloader", font=("Century Gothic", 16), width=57,
              height=3).grid(row=0, column=0, sticky="nsew")

tkinter.Label(url_frame, text="Base URL: ", height=1, width=20).grid(padx=(20, 5), pady=(20, 0), row=0, column=0)
tkinter.Entry(url_frame, textvariable=base_url, width=50, font=("Century Gothic", 10)).grid(row=0, column=1,
                                                                                            padx=(0, 20), pady=(20, 0))

tkinter.Label(anime_frame, text="Anime name:  ", height=1).grid(row=0, column=0, padx=(10, 5), pady=30, sticky="e")
tkinter.Entry(anime_frame, textvariable=folder_name, font=("Century Gothic", 12)).grid(row=0, column=1,
                                                                                       pady=30, padx=(0, 20))

tkinter.Label(episode_frame, text="Episode range:  ", height=1).grid(row=0, column=0, padx=5, pady=30)
tkinter.Entry(episode_frame, textvariable=episode_start, font=("Century Gothic", 12),
              width=4).grid(row=0, column=1, pady=30, padx=5, sticky="w")
tkinter.Label(episode_frame, text="  -  ", height=1, font=("Times", 20)).grid(row=0, column=2, padx=5, pady=30)
tkinter.Entry(episode_frame, textvariable=episode_end, font=("Century Gothic", 12),
              width=4).grid(row=0, column=3, pady=30, padx=(5, 10), sticky="w")

tkinter.Label(server_frame, text="Choose server", height=1, font=("Times", 14)).grid(row=0, column=0, pady=10)
tkinter.Radiobutton(server_frame, variable=server, value=1, text="goload.pro",
                    font=("Times", 12)).grid(row=1, column=0, pady=(0, 10))
tkinter.Radiobutton(server_frame, variable=server, value=2, font=("Times", 12),
                    text="streamsb (slow but avoids recaptcha)").grid(row=1, column=1, pady=(0, 10), padx=(30, 0))

tkinter.Button(button_frame, text="Download", font=("Century Gothic", 16), command=main_process,
               width=20, height=2).grid(row=0, column=0, padx=20, pady=(40, 0))

root.bind("<<exit_event>>", lambda e: root.quit())
root.mainloop()

# Creator: Spectropaws.X

"""
Working:

1. program asks for base url for anime to iterate over it for multiple episodes

2. program asks for anime folder name to save episodes in and range of episodes to download

3. program asks for server to download from...
    use goload.pro for faster download link search
    use streamsb when recaptcha is preventing goload.pro from displaying download links
    
4. program fetches download urls from the specified server 
    goload.pro takes 5-7 seconds to load url
    streamsb takes nearly 17 seconds to generate url for each episode (avoid if you are downloading more than 25
    
5. program starts a new thread if active_threads < Maximum_parallel_downloads
    each thread calls download_anime(links, indexes) function that requests for video and downloads it in chunks of 5mb
    
Note: program uses mttkinter to update progress bars in threads
"""

# TODO complete final update
