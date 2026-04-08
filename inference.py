import os
import yaml
import logging

from env.jarvis_env import JarvisEnv
from agents.baseline_agent import BaselineAgent
from agents.grader import evaluate_episode

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("Inference")

def load_tasks(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('tasks', [])

def run_task(task_def):
    task_name = task_def['id']
    max_steps = task_def.get('max_steps', 5)
    # Emit structured start tag
    print(f"[START] task={task_name}")

    env = JarvisEnv(task_name=task_name)
    agent = BaselineAgent(task_name=task_name)

    state = env.reset()
    total_reward = 0.0

    for step_counter in range(1, max_steps + 1):
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        print(f"[STEP] step={step_counter} action={action.action_type} reward={reward:.2f}")
        state = next_state
        total_reward += reward

    # Emit structured end tag with cumulative reward and steps
    print(f"[END] task={task_name} score={total_reward:.2f} steps={max_steps}")

    # Return the cumulative reward as the task score
    return total_reward

def run_inference():
    config_path = os.path.join(os.path.dirname(__file__), 'openenv.yaml')
    if not os.path.exists(config_path):
        logger.error(f"Config not found at {config_path}")
        return
        
    tasks = load_tasks(config_path)
    
    scores = {}
    for task in tasks:
        score = run_task(task)
        scores[task['id']] = score
        
    print("=== Final Inference Scores ===")
    for t_id, sc in scores.items():
        print(f"{t_id.ljust(10)}: {sc:.2f}")

if __name__ == "__main__":
    run_inference()
