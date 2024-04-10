import math
from maze_generator import generate_maze

class Map:
    """Contains the map and map logic"""

    def generate_map(self, size):
        self.map_array = generate_maze(size, 2)
        self.colision_map = self.generate_collision_map()

    def generate_collision_map(self):
        """Generate a dict with cordination as key and a boolean indicating collision as value"""
        colision_map = {}

        for j, cloumn in enumerate(self.map_array):
            for i, cell in enumerate(cloumn):
                if bool(cell):
                    colision_map[(j, i)] = True

        return colision_map
    
    def collides(self, pos):
        """Returns True if the position is colision"""
        return (int(pos[0]), int(pos[1])) in self.colision_map.keys()
    
    def separated_by_wall(self, p1, p2):
        """ Returns true if points are separated by a wall """
        x1, y1 = (int(p1[0]), int(p1[1]))
        x2, y2 = (int(p2[0]), int(p2[1]))
        slope = 2 * (y2 - y1) 
        slope_error = slope - (x2 - x1)
        y = y1 

        step = -1 if x1 > x2 else 1
        for x in range(x1, x2+step, step):

            if self.collides((x, y)):
                return True

            if (slope_error*step >= 0): 
                y = y+step
                slope_error = slope_error - 2 * (x2 - x1)
                
            slope_error = slope_error + slope 

        return False
    
    def opening_angle(self, pos):
        """ Returns the angle of an adjacent none wall cell """
        surrounding_cells = ((pos[0]+1, pos[1]), (pos[0], pos[1]+1), (pos[0]-1, pos[1]), (pos[0], pos[1]-1))
        for cell_indx in range(4):
            if not self.collides(surrounding_cells[cell_indx]):
                return math.radians(90)*cell_indx
            
        raise Exception("No opening angle found (This should not happen, there should always be an adjecent none wall cell to every cell).")
    

    def get_array(self):
        """Returns the map array"""
        return self.map_array



