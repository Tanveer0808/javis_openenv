import os
import yaml
import logging

from env.jarvis_env import JarvisEnv
from agents.baseline_agent import BaselineAgent
from agents.grader import evaluate_episode

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("RunBaseline")

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
        # Dynamic evaluation loop
        next_state, reward, done, info = env.step(action)
        
        # Logging structural outputs per user specification
        logger.info(f"Action Mapped: [{action.action_type}] | Params: {action.parameters}")
        logger.info(f"  => Env Transitioning | Progress Delta Reward: {reward:.2f}")
        logger.debug(f"  => State Context: {next_state}")
        
        state = next_state
        total_reward += reward

    final_score = evaluate_episode(task_name, state, total_reward)
    
    logger.info(f"Task {task_name.upper()} Termination Condition Hit.")
    logger.info(f"Final Execution 'Progress' Value: {state.get('progress')}")
    logger.info(f"Final Academic Score Grade: {final_score:.2f} / 1.00\n")
    return final_score

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), '..', 'openenv.yaml')
    tasks = load_tasks(config_path)
    
    scores = {}
    for task in tasks:
        score = run_task(task)
        scores[task['id']] = score
        
    logger.info("=== Final Progress Goal Scores ===")
    for t_id, sc in scores.items():
        logger.info(f"{t_id.ljust(10)}: {sc:.2f}")
