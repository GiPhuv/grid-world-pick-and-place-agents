import random
import matplotlib.pyplot as plt

#robot
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

#moi truong
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
    
    #Kiem tra xem vi tri dang kiem co phai tuong hay khong
    def is_wall(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return True
        if (row, col) in self.walls:
            return True
        return False
    
    #Check xem da dua hang den dich hay chua
    def is_done(self):
        if self.object_pos == self.goal_pos:
            return True
        return False
    
    #Vi tri tiep theo dang muon di
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
    
    #Buoc di
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
    
    #Nhat vat len
    def pick(self):
        if (self.robot.row, self.robot.col) == self.object_pos and self.robot.holding == False:
            self.robot.pick()
            self.object_pos = None
    
    #Dat vat xuong
    def place(self):
        if self.robot.holding:
            self.robot.place()
            self.object_pos = (self.robot.row, self.robot.col)
    
    #Hien thi map
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
    
    #Show tinh trang hien tai: da dung tren object chua, da ve dich chua, da cam hang chua
    def get_percept(self):
        on_object = (self.robot.row, self.robot.col) == self.object_pos
        on_goal = (self.robot.row, self.robot.col) == self.goal_pos
        holding = self.robot.holding
        result = {
            "on_object": on_object, "on_goal": on_goal, "holding": holding
        }
        return result

#hanh dong random
class RandomAgent:
    def __init__(self, env):
        pass
    def choose_action(self, percept):
        actions = ["up", "down", "left", "right", "pick", "place"]
        return random.choice(actions)

#chay chuong trinh va check so buoc hop le hay chua
def run_episode(env, agent, max_steps):
    done = False
    while env.is_done() == False and env.steps < max_steps:
        percept = env.get_percept()
        action = agent.choose_action(percept)
        done = env.step(action)
    return done, env.steps

#agent hoat dong tren dieu kien hien tai
class SimpleReflexAgent:
    def __init__(self, env):
        pass
    def choose_action(self, percept):
        choice = ["left", "right", "up", "down"]
        if percept["holding"] and percept["on_goal"]:
            return "place"
        elif not percept["holding"] and percept["on_object"]:
            return "pick"
        else: 
            return random.choice(choice)

#dung de so sanh
def evaluate(agent_class, n_runs, max_steps):
    successes = 0
    total_steps = 0
    for i in range(n_runs):
        env = Environment(6)
        done, steps = run_episode(env, agent_class(env), max_steps)
        if done == True:
            successes += 1
            total_steps += steps
    if successes > 0:
        return (successes/n_runs)*100, total_steps/successes
    else:
        return 0, None

#Cac o xung quanh la gi, co hop le khong
def neighbors(env, row, col):
    direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    result = []
    for dr, dc in direction:
        new_row = row + dr
        new_col = col + dc
        if not env.is_wall(new_row, new_col):
            result.append((new_row, new_col))
    return result

#tim duong bang bfs, de tim duong toi uu nhat
def bfs_distance(env, start, target):
    queue = [(start, 0)]
    visited = [(start)]
    while len(queue) > 0:
        (row, col), dis = queue.pop(0)
        if (row, col) == target:
            return dis
        neighbor = neighbors(env, row, col)
        for (nrow, ncol) in neighbor:
            if (nrow, ncol) not in visited:
                visited.append((nrow, ncol))
                queue.append(((nrow, ncol), dis + 1))
    return None

#tim duong, in ra cac hanh dong can lam
def find_path(env, start, target):
    moves = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1),
    }
    queue = [(start, [])]
    visited = [start]
    while (len(queue)) > 0 :
        (row, col), path = queue.pop(0)
        if (row, col) == target:
            return path
        for action, (dr, dc) in moves.items():
            nrow = row + dr
            ncol = col + dc
            if not env.is_wall(nrow, ncol) and (nrow, ncol) not in visited:
                visited.append((nrow, ncol))
                queue.append(((nrow, ncol), path + [action]))
    return None

#agent len ke hoach de dat duoc muc dich
class GoalBasedAgent:
    def __init__(self, env):
        start = (env.robot.row, env.robot.col)
        path_to_object = find_path(env, start, env.object_pos)
        path_to_goal = find_path(env, env.object_pos, env.goal_pos)
        self.plan = path_to_object + ["pick"] + path_to_goal + ["place"]
    
    def choose_action(self, percept):
        action = self.plan.pop(0)
        return action
    

names =["Random", "Reflex", "Goal_based"]
avg_steps = []
success_rates = []
agent_classes = [RandomAgent, SimpleReflexAgent, GoalBasedAgent]
for cl in agent_classes:
    rate, avg = evaluate(cl, 100, 20000)
    avg_steps.append(avg)
    success_rates.append(rate)

labels = []
for i in range(0, 3):
    name = names[i]
    rate = success_rates[i]
    value = f"{name} ({rate}%)"
    labels.append(value)
bars = plt.bar(
    x = labels,
    height = avg_steps,
)
plt.bar_label(bars)
plt.yscale("log")
plt.title("Comparing agents when running")
plt.ylabel("Comparing average")
plt.xlabel("Agents")
plt.savefig("comparing_agents.png")
plt.show()