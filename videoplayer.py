import pygame
from moviepy.editor import VideoFileClip
import threading

import os
import sys

if getattr(sys, 'frozen', False):
    # If the application is run as a bundle (i.e. pyinstaller)
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(__file__)

os.environ['IMAGEIO_FFMPEG_EXE'] = os.path.join(base_dir, 'ffmpeg.exe')

# Now you can import any module that requires ffmpeg
from moviepy.editor import VideoFileClip

class VideoPlayer:

    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls, *args, **kwargs):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls(*args, **kwargs)
        return cls._instance

    def __init__(self, window_width=512, window_height=512):
        self.window_width = window_width
        self.window_height = window_height
        self.current_time = 0
        self.main_video = True
        self.change_event = threading.Event()

        pygame.init()
        pygame.display.set_caption("Talkinterface")
        icon = pygame.image.load("window_icon.png")
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))

        self.load_video("main_video.mp4")

    def load_video(self, filename):
        self.clip = VideoFileClip(filename)
        self.clip.preview()
        self.clip = self.clip.resize(height=self.window_height)
        self.current_time = 0

    def change_video(self, filename):
        with self._lock:
            self.load_video(filename)
            self.main_video = filename == "main_video.mp4"
            if not self.main_video:
                # Setzen Sie self.current_time auf self.clip.duration, um zu verhindern, dass das triggered_video erneut abgespielt wird
                self.current_time = self.clip.duration

    def initiate_talkinterface(self):
        self.run_application_loop()

    def run_application_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            if self.change_event.is_set() and self.main_video:
                self.change_video("triggered_video.mp4")
                self.change_event.clear()

            if self.current_time < self.clip.duration:
                img = self.clip.get_frame(self.current_time)
                surf = pygame.surfarray.make_surface(img.swapaxes(0, 1))
                self.screen.blit(surf, (0, 0))
                self.current_time += 1 / self.clip.fps
            else:
                self.change_video("main_video.mp4")

            pygame.display.flip()
            self.clock.tick(self.clip.fps)