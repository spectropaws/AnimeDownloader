import time
import requests
import os
import threading
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import selenium.common.exceptions
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from tkinter import ttk
from tkinter import messagebox
import tkinter


# change brave's location if not in 'Program Files' or want to use chrome
browser_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/102.0.5005.115 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           "Referer": ""}


class Anime:
    def __init__(self, base_url: str, folder_name: str, server: int, episode_range: tuple):
        self.base_url = re.match(r"(.+-)\d*", base_url).group(1)
        self.folder_name = folder_name
        self.server = server
        self.episode_range = episode_range
        self.max_parallel_downloads = 10
        self.__download_indexes = []
        self.__download_list = []

    # Create anime directory, set the referer in headers and start a thread __start_download_threads
    def start_download(self, progress_window: tkinter.Tk):
        global headers

        if not os.path.isdir(self.folder_name):
            os.mkdir(self.folder_name)

        frame = tkinter.Frame(progress_window)
        frame.pack(fill=tkinter.X, pady=10, padx=10)
        tkinter.Label(frame, text=f"Fetching links:").grid(row=0, column=0)
        progress_bar = ttk.Progressbar(frame, orient=tkinter.HORIZONTAL, mode="determinate", length=350)
        progress_bar.grid(row=0, column=1)
        progress_bar['maximum'] = self.episode_range[1] + 1 - self.episode_range[0]

        progress_window.deiconify()
        self.__download_indexes = [num for num in range(self.episode_range[0], self.episode_range[1] + 1)]
        for index in range(self.episode_range[0], self.episode_range[1] + 1):
            self.__download_list.append(self.fetch_url(index))
            progress_bar['value'] += 1
            progress_window.update_idletasks()
        frame.destroy()

        threads = []
        if self.server == 1:
            headers['Referer'] = "https://goload.pro/"

        elif self.server == 2:
            headers['Referer'] = "https://sbplay2.xyz/"
            headers['Accept'] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp," \
                                "image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9 "
            headers['Accept-Encoding'] = "gzip, deflate, br"
            headers['Accept-Language'] = "en-US"
            headers['Connection'] = "keep-alive"
            headers['Sec-Fetch-Dest'] = "document"
            headers['Sec-Fetch-Mode'] = "navigate"
            headers['Sec-Fetch-Site'] = "cross-site"
            headers['Sec-Fetch-User'] = "?1"
            headers['Sec-GPC'] = "1"
            headers['Upgrade-Insecure-Requests'] = "1"

        for i in range(len(self.__download_list)):
            if self.__download_list[i] == '':
                messagebox.showerror("Not found!", f"Episode {self.__download_indexes[i]} 1080p Not found! skipping...")
            else:
                t = threading.Thread(target=self.__download_episode, args=(self.__download_list[i],
                                                                           self.__download_indexes[i], progress_window))
                threads.append(t)
                t.start()
                time.sleep(0.05)
                while True:
                    if threading.active_count() > self.max_parallel_downloads + 1:
                        time.sleep(5)
                        continue
                    else:
                        break

        for thread in threads:
            thread.join()
        progress_window.event_generate("<<exit_event>>")

    def __download_episode(self, url, num, progress_window: tkinter.Tk):
        video = requests.get(url, headers=headers, stream=True)

        frame = tkinter.Frame(progress_window)
        frame.pack(fill=tkinter.X, pady=10, padx=10)
        tkinter.Label(frame, text=f"Episode {num}").grid(row=0, column=0)
        progress_bar = ttk.Progressbar(frame, orient=tkinter.HORIZONTAL, mode="determinate", length=350)
        progress_bar.grid(row=0, column=1)
        progress_bar['maximum'] = int(float(video.headers['Content-Length']) / (1024 * 1024))
        with open(f"{self.folder_name}\\Episode {num}.mp4", "wb") as file:
            for chunk in video.iter_content(1024 * 1024 * 5):
                if chunk:
                    file.write(chunk)
                    progress_bar['value'] += int(len(chunk) / (1024 * 1024))
                    progress_window.update_idletasks()
        frame.destroy()

    def fetch_url(self, num):
        if self.server == 1:
            return self.__fetch_from_goload(num)
        elif self.server == 2:
            return self.__fetch_from_streamsb(num)

    def __fetch_from_goload(self, num):
        page = requests.get(self.base_url + str(num), timeout=30).content
        soup = BeautifulSoup(page, 'html.parser')
        options = Options()
        options.binary_location = browser_location
        options.add_argument("--incognito")
        options.add_argument("headless")
        download_page = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        download_page.minimize_window()
        download_page.get(soup.select_one("li.dowloads a").attrs['href'])  # web developer hasn't corrected the typo yet
        soup = BeautifulSoup(download_page.page_source, 'html.parser')
        download_links = soup.select("div.mirror_link div.dowload a")  # web developer hasn't corrected the typo yet
        download_link = ""
        string_1080p = """Download
                                (1080P - mp4)"""
        string_720p = """Download
                                (720P - mp4)"""
        for link in download_links:
            if link.string == string_1080p:
                download_link = link.attrs['href']

        if download_link == '':
            for link in download_links:
                if link.string == string_720p:
                    download_link = link.attrs['href']

        return download_link

    def __fetch_from_streamsb(self, num):
        page = requests.get(self.base_url + str(num), timeout=30).content
        soup = BeautifulSoup(page, 'html.parser')
        streamsb_video_link_raw = soup.select_one("li.streamsb a").attrs['data-video']
        temp = streamsb_video_link_raw.split('/')
        streamsb_domain_name = 'https://' + temp[2] + '/'
        streamsb_page_name = temp[len(temp) - 1]
        options = Options()
        options.binary_location = browser_location
        options.add_argument("--incognito")
        options.add_argument("headless")
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                             'like Gecko) Chrome/102.0.5005.115 Safari/537.36')

        download_page = webdriver.Chrome(executable_path="chromedriver.exe", options=options)
        download_page.get(streamsb_domain_name + "d/" + streamsb_page_name)

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

        time.sleep(10)
        download_page.execute_script('arguments[0].click();',
                                     download_page.find_element(By.CLASS_NAME, "g-recaptcha"))
        try:
            WebDriverWait(download_page, 20).until(
                expected_conditions.presence_of_element_located((By.XPATH,
                                                                 "// a[contains(text(),'Download Video')]"))
            )
            download_link = download_page.find_element(By.XPATH, "// a[contains(text(),'Download Video')]"). \
                get_attribute('href')
            return download_link
        except selenium.common.exceptions.TimeoutException:
            return ''
