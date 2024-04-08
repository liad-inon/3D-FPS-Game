from dataclasses import dataclass

@dataclass
class Pose:
    x: float
    y: float
    angle: float

    def get_pos(self):
        return (self.x, self.y)
    
    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]