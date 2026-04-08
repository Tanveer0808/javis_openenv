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
    logger.info(f"--- Starting Goal-Driven Task: {task_name.upper()} ---")
    
    env = JarvisEnv(task_name=task_name)
    agent = BaselineAgent(task_name=task_name)
    
    state = env.reset()
    done = False
    total_reward = 0.0
    
    while not done:
        action = agent.act(state)
        next_state, reward, done, info = env.step(action)
        
        logger.info(f"Action Mapped: [{action.action_type}] | Params: {action.parameters}")
        logger.info(f"  => Env Transitioning | Progress Delta Reward: {reward:.2f}")
        
        state = next_state
        total_reward += reward

    final_score = evaluate_episode(task_name, state, total_reward)
    logger.info(f"Task {task_name.upper()} Termination Condition Hit.")
    logger.info(f"Final Academic Score Grade: {final_score:.2f} / 1.00\n")
    return final_score

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
        
    logger.info("=== Final Inference Scores ===")
    for t_id, sc in scores.items():
        logger.info(f"{t_id.ljust(10)}: {sc:.2f}")

if __name__ == "__main__":
    run_inference()
