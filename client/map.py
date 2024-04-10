

class Map:
    """Contains the map and map logic"""
        
    def init(self, map_array):
        """For initializing the class from the map sent by the server"""
        self.map_array = map_array
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
    def get_array(self):
        """Returns the map array"""
        return self.map_array