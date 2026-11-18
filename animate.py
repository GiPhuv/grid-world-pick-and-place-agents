from environment import Environment
from agents import GoalBasedAgent
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.animation import FuncAnimation, PillowWriter

def get_frame(env):
    robot_pos = (env.robot.row, env.robot.col)
    holding = env.robot.holding
    object_pos = env.object_pos
    frame = {"robot": robot_pos, "holding": holding, "object": object_pos}
    return frame

def run_episode_with_frames(env, agent, max_steps):
    frames = []
    frames.append(get_frame(env))
    done = False
    while env.is_done() == False and env.steps < max_steps:
        percept = env.get_percept()
        action = agent.choose_action(percept)
        done = env.step(action)
        frames.append(get_frame(env))
    return frames, done

def frame_to_grid(env, frame):
    grid = np.zeros((env.size, env.size), dtype = int)
    for row, col in env.walls:
        grid[row, col] = 1
    goal_row, goal_col = env.goal_pos
    grid[goal_row, goal_col] = 2
    if frame["object"] is not None:
        object_row, object_col = frame["object"]
        grid[object_row, object_col] = 3
    robot_row, robot_col = frame["robot"]
    if frame["holding"] == True:
        grid[robot_row, robot_col] = 5
    else:
        grid[robot_row, robot_col] = 4
    grid = np.pad(grid, 1, constant_values = 1)
    return grid

def play(env, frames):
    colors = ["white", "black", "Limegreen", "Orange", "Dodgerblue", "Red"]
    cmap = ListedColormap(colors)
    for i in range(len(frames)):
        plt.clf()
        grid = frame_to_grid(env, frames[i])
        plt.imshow(grid, cmap = cmap, vmin = 0, vmax = 5)
        plt.axis("off")
        plt.title(f"Buoc {i}")
        plt.pause(0.4)
    plt.show()

def save_gif(env, frames, filename):
    colors = ["white", "black", "limegreen", "orange", "dodgerblue", "red"]
    cmap = ListedColormap(colors)
    fig, ax = plt.subplots(figsize=(4, 4))

    def update(i):
        ax.clear()
        grid = frame_to_grid(env, frames[i])
        ax.imshow(grid, cmap = cmap, vmin = 0, vmax = 5)
        ax.axis("off")
        ax.set_title(f"{i}")
    
    anim = FuncAnimation(fig, update, frames = len(frames), interval = 400)
    anim.save(filename, writer=PillowWriter(fps=2))
    plt.close(fig)

if __name__ == "__main__":
    env = Environment(6)
    agent = GoalBasedAgent(env)
    frames, done = run_episode_with_frames(env, agent, 200)
    save_gif(env, frames, "demo.gif")
