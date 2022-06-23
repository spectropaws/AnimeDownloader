# AnimeDownloader
Python app to mass download anime.

This app provides an easy interface to download anime from gogoanime website.

*NOTE*: You need to change `self._event_queue = queue.Queue(1)`  to  `self._event_queue = queue.Queue(0)` 
in mtTinker.py in mttinker package to ensure that the program runs correctly.

Simply run the python file and fill in the Base URL of anime (URL of any random episode of required Anime), Anime name, Range of episodes to download and server to use
then click the Download button to start the download.
A pop-up window shows the download progress of each episode.

Fill in the same number in start and end entries of episode range if you want to download a single episode.

*NOTE*: You need the manually close the program from task manager after the download is complete. 
        Alternatively, if you run the program using IDE, you can stop it through the IDE.
        This issue will be fixed in the next update.
