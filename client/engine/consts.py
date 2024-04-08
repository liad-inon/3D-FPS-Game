import math
from conf import *

FOV = math.radians(90)
HALF_FOV = FOV/2
HALF_WIDTH = RESOLOTION[0] // 2
HALF_HEIGHT = RESOLOTION[1] // 2
TEXTURE_SIZE = 255
HALF_TEXTURE_SIZE = TEXTURE_SIZE // 2
RAYS_NUM = RESOLOTION[0]//2
SCREEN_DIST = HALF_WIDTH / math.tan(HALF_FOV)
SCALE = RESOLOTION[0]//RAYS_NUM
HALF_NUM_RAYS = RAYS_NUM // 2
DELTA_ANGLE = FOV / RAYS_NUM
RAY_MAX_STEPS = 20