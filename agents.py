import random
from search import find_path

class RandomAgent:
    def __init__(self, env):
        pass
    def choose_action(self, percept):
        actions = ["up", "down", "left", "right", "pick", "place"]
        return random.choice(actions)

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

class GoalBasedAgent:
    def __init__(self, env):
        start = (env.robot.row, env.robot.col)
        path_to_object = find_path(env, start, env.object_pos)
        path_to_goal = find_path(env, env.object_pos, env.goal_pos)
        self.plan = path_to_object + ["pick"] + path_to_goal + ["place"]
    
    def choose_action(self, percept):
        action = self.plan.pop(0)
        return action
