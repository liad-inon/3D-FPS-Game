from consts import *
import time
    
class Animation:
    def __init__(self, frames, interval, loop=False):
        self.frames = frames
        self.interval = interval
        self.loop = loop

        self.current_frame_indx = 0
        self.last_change_sec = 0
        self.playing = False

    def start(self):
        self.current_frame_indx = 0
        self.last_change_sec = time.time()
        self.playing = True

    def reset(self):
        self.current_frame_indx = 0
        self.last_change_sec = time.time()

    def update(self):
        """change current frame if needed a acording to time"""
        if self.last_change_sec+self.interval < time.time() and self.playing:
            self.last_change_sec = time.time()

            if self.current_frame_indx >= len(self.frames)-1:
                if self.loop:
                    self.current_frame_indx = 0
                else:
                    self.playing = False
            else:
                self.current_frame_indx += 1

    @property
    def current_frame(self):
        return self.frames[self.current_frame_indx]


        