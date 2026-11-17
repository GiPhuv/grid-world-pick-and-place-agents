import random
from search import bfs_distance

class Robot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.holding = False
    
    def move_right(self):
        self.col = self.col + 1
    
    def move_left(self):
        self.col = self.col - 1
    
    def move_down(self):
        self.row = self.row + 1
    
    def move_up(self):
        self.row = self.row - 1
    
    def pick(self):
        self.holding = True
    
    def place(self):
        self.holding = False
    
    def show(self):
        print("Vi tri:", self.row, self.col, "|Dang cam vat:", self.holding)


class Environment:
    def __init__(self, size):
        self.size = size
        self.walls = [(1, 1), (1, 2), (3, 3), (4, 1)]
        free_cells = []
        for row in range(self.size):
            for col in range(self.size):
                if (row, col) not in self.walls and (row, col) != (0, 0):
                    free_cells.append((row, col))
        while True: 
            ob_pos, gl_pos = random.sample(free_cells, 2)
            d1 = bfs_distance(self, (0, 0), ob_pos)
            d2 = bfs_distance(self, ob_pos, gl_pos)
            if d1 is not None and d2 is not None:
                break
        self.object_pos = ob_pos
        self.goal_pos = gl_pos
        self.robot = Robot(0, 0)
        self.steps = 0
    
    def is_wall(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return True
        if (row, col) in self.walls:
            return True
        return False
    
    def is_done(self):
        if self.object_pos == self.goal_pos:
            return True
        return False
    
    def next_position(self, action):
        new_row = self.robot.row
        new_col = self.robot.col
        if action == "right":
            new_col += 1
        elif action == "left":
            new_col -= 1
        elif action == "up":
            new_row -= 1
        elif action == "down":
            new_row += 1
        return new_row, new_col
    
    def step(self, action):
        actions = ["right", "left", "up", "down"]
        self.steps += 1
        if action in actions:
            new_row, new_col = self.next_position(action)
            if not self.is_wall(new_row, new_col):
                self.robot.row = new_row
                self.robot.col = new_col
        elif action == "pick":
            self.pick()
        elif action == "place":
            self.place()
        return self.is_done()
    
    def pick(self):
        if (self.robot.row, self.robot.col) == self.object_pos and self.robot.holding == False:
            self.robot.pick()
            self.object_pos = None
    
    def place(self):
        if self.robot.holding:
            self.robot.place()
            self.object_pos = (self.robot.row, self.robot.col)
    
    def show(self):
        for r in range(self.size):
            line = ""
            for c in range(self.size):
                if (r, c) == (self.robot.row, self.robot.col):
                    line += "R "
                elif (r, c) in self.walls:
                    line += "# "
                elif (r, c) == self.object_pos:
                    line += "O "
                elif (r, c) == self.goal_pos:
                    line += "G "
                else:
                    line += ". "
            print(line)
    
    def get_percept(self):
        on_object = (self.robot.row, self.robot.col) == self.object_pos
        on_goal = (self.robot.row, self.robot.col) == self.goal_pos
        holding = self.robot.holding
        result = {
            "on_object": on_object, "on_goal": on_goal, "holding": holding
        }
        return result