import matplotlib.pyplot as plt
from environment import Environment
from agents import RandomAgent, SimpleReflexAgent, GoalBasedAgent

def run_episode(env, agent, max_steps):
    done = False
    while env.is_done() == False and env.steps < max_steps:
        percept = env.get_percept()
        action = agent.choose_action(percept)
        done = env.step(action)
    return done, env.steps

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

if __name__ == "__main__":
    names =["Random", "Reflex", "Goal-based"]
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
    plt.ylabel("Average number of steps (successful runs only")
    plt.xlabel("Agents")
    plt.savefig("comparing_agents.png")
    plt.show()
