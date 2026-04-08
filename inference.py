import os
import yaml
import logging

from env.jarvis_env import JarvisEnv
from agents.baseline_agent import BaselineAgent

# 1. Disable logging to avoid breaking evaluator parsing
logging.disable(logging.CRITICAL)

def load_tasks(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('tasks', [])

def run_task(task_def):
    task_name = task_def['id']
    max_steps = task_def.get('max_steps', 5)
    print(f"[START] task={task_name}")

    env = JarvisEnv(task_name=task_name)
    agent = BaselineAgent(task_name=task_name)

    state = env.reset()
    total_reward = 0.0
    steps_taken = 0

    for step_counter in range(1, max_steps + 1):
        action = agent.act(state)
        # Act with real-time environment
        next_state, reward, done, info = env.step(action)
        
        print(f"[STEP] step={step_counter} action={action.action_type} reward={reward:.2f}")
        
        state = next_state
        total_reward += reward
        steps_taken += 1
        
        # 2. Stop after task completion instead of idle spamming
        if done:
            break

    # 3. Dynamic total reward but cleanly formatted output
    print(f"[END] task={task_name} score={total_reward:.2f} steps={steps_taken}")

    return total_reward

def run_inference():
    config_path = os.path.join(os.path.dirname(__file__), 'openenv.yaml')
    if not os.path.exists(config_path):
        return
        
    tasks = load_tasks(config_path)
    for i, task in enumerate(tasks):
        run_task(task)
        if i < len(tasks) - 1:
            print() # Print newline between tasks

if __name__ == "__main__":
    run_inference()
