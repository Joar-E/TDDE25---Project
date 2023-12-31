import math
import pymunk
import pygame
from pymunk import Vec2d
import gameobjects
from collections import defaultdict, deque
import heapq
from heapq import heappush, heappop

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
    boxes. 
    """

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
        self.maybe_shoot()
        next(self.move_cycle)

    def maybe_shoot(self):
        """ Makes a raycast query in front of the tank. If another tank
            or a wooden box is found, then we shoot. 
        """

        start_coord = (self.tank.body.position[0] - math.sin(self.tank.body.angle)*0.4, self.tank.body.position[1] + math.cos(self.tank.body.angle)*0.4)
        end_coord = (self.tank.body.position[0] - math.sin(self.tank.body.angle)*10, self.tank.body.position[1] + math.cos(self.tank.body.angle)*10)
        
        res = self.space.segment_query_first(start_coord, end_coord, 0, pymunk.ShapeFilter())


        if hasattr(res, 'shape'):
            if hasattr(res.shape, 'parent'):
                if isinstance(res.shape.parent, gameobjects.Box) or\
                    isinstance(res.shape.parent, gameobjects.Tank):
                    if getattr(res.shape.parent, "destructable") == True:
                        if self.tank.can_shoot():
                            self.game_objects_list.append(self.tank.shoot(self.space))

    def should_turn_right(self, angle_to_next_coord, tank_angle) -> bool:
        """ Determine if the tank should turn right based on it's angle
            and the angle to the next coordinate 
        """
        if tank_angle >= angle_to_next_coord:
            return tank_angle - math.pi > angle_to_next_coord 

        elif tank_angle < angle_to_next_coord:
            return tank_angle + math.pi > angle_to_next_coord 
        

    def angle_2_pi_converter(self, angle):
        """ Returns the angles without unnecessary 2*Pi """
        if angle >= 0:
             
            return angle % (2*math.pi)
        else:
            return (2*math.pi + angle) % (2*math.pi)
    
    def diff_between_angles(self, angle1, angle2):
        """ Returns the smallest difference between two angles """
        difference = angle1 - angle2
        if difference > math.pi:
            difference = math.pi - difference
        return difference
    
    def move_cycle_gen (self):
        """ A generator that iteratively goes through all the required steps
            to move to our goal.
        """ 
        
        while True:

            path = self.A_star_search(False)
            if not path:
                path = self.A_star_search(True)
            
            
            path.popleft() # Removes the starting position from the path
            next_coord = path.popleft() + (0.5, 0.5) #0.5 to get the center of the tile
            
            tank_angle = self.angle_2_pi_converter(self.tank.body.angle)
            angle_to_next_coord = angle_between_vectors(self.tank.body.position, next_coord)
            angle_to_next_coord = self.angle_2_pi_converter(angle_to_next_coord)
            
            yield

            while abs(self.angle_2_pi_converter(self.diff_between_angles(tank_angle, angle_to_next_coord))) > MIN_ANGLE_DIF:
                self.tank.stop_moving()
                if self.should_turn_right(angle_to_next_coord, tank_angle):
                    self.tank.turn_right()
                else:    
                    self.tank.turn_left()

                yield
                tank_angle = self.angle_2_pi_converter(self.tank.body.angle)

            self.tank.stop_turning()

            distance_to_next_coord = self.tank.body.position.get_distance(next_coord)
            current_distance = 100
            
            while (current_distance - distance_to_next_coord) > 0: #Kan förekomma buggar pga current_distance = 100, ändra senare!
                self.tank.accelerate()

                
                current_distance = self.tank.body.position.get_distance(next_coord)
                yield
                distance_to_next_coord = self.tank.body.position.get_distance(next_coord)
                yield
            
            
            #self.tank.stop_moving()
            self.update_grid_pos()

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
        queue.append((source_node, []))
        
        while queue:
            target, path = queue.popleft()
            
            if target == self.get_target_tile():
                path.append(target)
                shortest_path = path
                
                break
            
            neighboring_tiles = self.get_tile_neighbors(target)
            for tiles in neighboring_tiles:
                if tiles.int_tuple not in visited_node:
                    #print(type(target))
                    queue.append((tiles, path + [target])) #path is actually a list but does not yet know it's a list
                                                           #so we can not append target. But we can make target into a list
                                                           # and then combine the two lists 
                    visited_node.add(tiles.int_tuple)
                    
        return deque(shortest_path)


    def traceback(self, path_dict, current):
        """
        Reconstructs a path from end to start
        """
        shortest_path = deque()
        shortest_path.append(Vec2d(current))

        while True:
            current = path_dict[current]
            shortest_path.appendleft(Vec2d(current))
            if Vec2d(current) == self.grid_pos:
                return shortest_path


    def heuristic(self, node):
        """The manhattan distance between a node and the target"""
        goal = self.get_target_tile()
        h = (abs(node[0] - goal[0]) + abs(node[1] - goal[1]))
        return h


    def A_star_search(self, metal_box_allowed):
        """
        A* search for finding the shortest path for a tank
        """
        # f = g + heuristic, f is the total score of a node
        # g is the cost to get from the start to a certain node
        # The score of each node is kept in a dictionary
        f_score = defaultdict(lambda: math.inf)
        g_score = defaultdict(lambda: math.inf)
        # Keep track from wich node each node was accessed
        came_from = defaultdict()
        # contains nodes we might want to explore
        heap_queue = []
        # get the start and end nodes
        root_node = self.grid_pos.int_tuple
        end = self.get_target_tile().int_tuple
        # set the values of the root node
        g_score[root_node] = 0
        f_score[root_node] = 0
        came_from[root_node] = root_node
        # The heap queue contains both the f score of a node and the node itself, so 
        # that the node with the lowest f score always can be sorted and placed first
        heappush(heap_queue, (f_score[root_node], root_node))        

        while heap_queue:
            # The node with the lowest f value is the current one
            current = heappop(heap_queue)[1]
                        
            if current == end:
                # we found our goal, reconstruct path and return it
                return self.traceback(came_from, current)
            # Start exploring the current node
            for neighbor in self.get_tile_neighbors(Vec2d(current), metal_box_allowed):
                neighbor = neighbor.int_tuple
                # the cost from start to neighbor through current
                # (since every edge has the same value we add a constant 1)
                tentative_g_score = g_score[current] + 1
                # This path to neighbor has a lower cost than any previous one
                # (a node that hasn't been discovered yet has a g score of inf)
                if tentative_g_score < g_score[neighbor]:
                    # values for the neighbor are created
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(Vec2d(neighbor))
                    
                    if (f_score[neighbor], neighbor) not in heap_queue:
                        heappush(heap_queue, (f_score[neighbor], neighbor))

        # If the algorithm fails to find a path it returns an empty deque
        return deque()


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


    def get_tile_neighbors(self, coord_vec, metal_box_allowed):
        """ Returns all bordering grid squares of the input coordinate.
            A bordering square is only considered accessible if it is grass
            or a wooden box.
        """
        self.coord_vec = coord_vec
        neighbors = [coord_vec + delta for delta in [(0,1), (-1,0), (0,-1), (1,0)]]
        
        # Find the coordinates of the tiles' four neighbors
        if metal_box_allowed:
            return list(filter(self.filter_tile_neighbors_metal_box, neighbors))
        else:
            return list(filter(self.filter_tile_neighbors, neighbors))


    def filter_tile_neighbors (self, coord) -> bool:
        """ Filters the neighboring tiles based on which of tiles
            the tank is allowed on 
        """
        if coord[0] <= self.MAX_X and coord[0] >= 0\
             and coord[1] <= self.MAX_Y and coord[1] >= 0:

            if self.currentmap.boxAt(coord[0], coord[1]) == 0 or \
               self.currentmap.boxAt(coord[0], coord[1]) == 2:
                return True
            return False


    def filter_tile_neighbors_metal_box (self, coord) -> bool:
        """ Filters the neighboring tiles based on which of tiles
            the tank is allowed on, extended to metal boxes 
        """
        if coord[0] <= self.MAX_X and coord[0] >= 0\
             and coord[1] <= self.MAX_Y and coord[1] >= 0:

            if self.currentmap.boxAt(coord[0], coord[1]) == 0 or \
               self.currentmap.boxAt(coord[0], coord[1]) == 2 or \
               self.currentmap.boxAt(coord[0], coord[1]) == 3:
                return True
            return False


SimpleAi = Ai # Legacy