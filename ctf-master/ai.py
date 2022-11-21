import math
import pymunk
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
import maps

# NOTE: use only 'map0' during development!

MIN_ANGLE_DIF = math.radians(3) # 3 degrees, a bit more than we can turn each tick



def angle_between_vectors(vec1, vec2):
    """ Since Vec2d operates in a cartesian coordinate space we have to
        convert the resulting vector to get the correct angle for our space.
    """
    vec = vec1 - vec2 
    vec = vec.perpendicular()
    return vec.angle

def periodic_difference_of_angles(angle1, angle2): 
    return  (angle1% (2*math.pi)) - (angle2% (2*math.pi))


class Ai:
    """ A simple ai that finds the shortest path to the target using 
    a breadth first search. Also capable of shooting other tanks and or wooden
    boxes. """

    def __init__(self, tank,  game_objects_list, tanks_list, space, currentmap):
        self.tank               = tank
        self.game_objects_list  = game_objects_list
        self.tanks_list         = tanks_list
        self.space              = space
        self.currentmap         = currentmap
        self.flag = None
        self.MAX_X = currentmap.width - 1 
        self.MAX_Y = currentmap.height - 1

        self.path = deque()
        self.move_cycle = self.move_cycle_gen()
        self.update_grid_pos()

    def update_grid_pos(self):
        """ This should only be called in the beginning, or at the end of a move_cycle. """
        self.grid_pos = self.get_tile_of_position(self.tank.body.position)
    
    def decide(self):
        """ Main decision function that gets called on every tick of the game. """
        next(self.move_cycle)

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """
        pass # To be implemented

    
    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """ 
        
        
        while True:
            #print("hej")
            
            path = self.find_shortest_path()
            if not path:
                yield
                continue
            path.popleft() # Removes the starting position from the path
            tank_angle = self.tank.body.angle
            next_coord = path.popleft() + (0.5, 0.5) #0.5 to get the center of the tile

            angle_to_next_coord = angle_between_vectors(self.tank.body.position, next_coord)

            p_diff = periodic_difference_of_angles(tank_angle, angle_to_next_coord)
            self.tank.stop_moving()
            yield
            while (tank_angle - p_diff) > MIN_ANGLE_DIF:    
                self.tank.turn_left()
                #print(tank_angle)
                #print(p_diff)
                
                yield
                tank_angle = self.tank.body.angle
            self.tank.stop_turning()

            distance_to_next_coord = self.tank.body.position.get_distance(next_coord)
            current_distance = 100
            while (current_distance - distance_to_next_coord) > 0:
                self.tank.accelerate()

                current_distance = self.tank.body.position.get_distance(next_coord)
                yield
                distance_to_next_coord = self.tank.body.position.get_distance(next_coord)
                yield
            print(tank_angle - p_diff)
            #print("hej2")
            #print(self.tank.body.position)
            self.tank.stop_moving()
            self.update_grid_pos()
            #print(self.tank.body.position)
            yield
            continue
        
            #move_cycle = move_cycle_gen()           
            
 
    def find_shortest_path(self):
        """ A simple Breadth First Search using integer coordinates as our nodes.
            Edges are calculated as we go, using an external function.
        """
        source_node = self.grid_pos
        queue = deque()
        shortest_path = []
        visited_node = set()
        #target_tile = self.get_target_tile()
        queue.append((source_node, []))
        
        while queue:
            #print(queue)
            target, path = queue.popleft()
            
            if target == self.get_target_tile():
                path.append(target)
                shortest_path = path
                
                break
            
            neighboring_tiles = self.get_tile_neighbors(target)
            for tiles in neighboring_tiles:
                #print(tiles.int_tuple in visited_node)
                if tiles.int_tuple not in visited_node:
                    
                    queue.append((tiles, path + [target])) #path is actually a list but does not yet know it's a list
                                                           #so we can not append target. But we can make target into a list
                                                           # and then combine the two lists 
                    #print(path)
                    visited_node.add(tiles.int_tuple)
                    #print(visited_node)
                    
        return deque(shortest_path)
            
    def get_target_tile(self):
        """ Returns position of the flag if we don't have it. If we do have the flag,
            return the position of our home base.
        """
        if self.tank.flag != None:
            x, y = self.tank.start_position
        else:
            self.get_flag() # Ensure that we have initialized it.
            x, y = self.flag.x, self.flag.y
        return Vec2d(int(x), int(y))

    def get_flag(self):
        """ This has to be called to get the flag, since we don't know
            where it is when the Ai object is initialized.
        """
        if self.flag == None:
        # Find the flag in the game objects list
            for obj in self.game_objects_list:
                if isinstance(obj, gameobjects.Flag):
                    self.flag = obj
                    break
        return self.flag

    def get_tile_of_position(self, position_vector):
        """ Converts and returns the float position of our tank to an integer position. """
        x, y = position_vector
        return Vec2d(int(x), int(y))

    def get_tile_neighbors(self, coord_vec):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        self.coord_vec = coord_vec
        neighbors = [coord_vec + delta for delta in [(0,1), (-1,0), (0,-1), (1,0)]]
        
 # Find the coordinates of the tiles' four neighbors
        return list(filter(self.filter_tile_neighbors, neighbors))

    def filter_tile_neighbors (self, coord):
        
        if coord[0] <= self.MAX_X and coord[0] >= 0\
             and coord[1] <= self.MAX_Y and coord[1] >= 0:

            if self.currentmap.boxAt(coord[0], coord[1]) == 0:
                return True
            return False



SimpleAi = Ai # Legacy