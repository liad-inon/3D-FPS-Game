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
    
class AnimationManager:
    def __init__(self, defult_animation, animations: dict[str, Animation]):
        if not defult_animation.loop:
            raise NotImplementedError("defult animation must loop")

        self.defult_animation = defult_animation
        self.animations = animations
        self.current_animation = defult_animation
        
    def play(self, name):
        self.current_animation = self.animations[name].start()
        self.current_animation.play()

    def get_current_frame(self):
        self.current_animation.update()

        if not self.current_animation.playing:
            self.current_animation = self.defult_animation
            self.current_animation.play()
            return self.current_frame
        else:
            return self.current_animation


        