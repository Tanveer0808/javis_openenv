import os
import yaml
import time
import logging
import webbrowser
import urllib.parse

from env.jarvis_env import JarvisEnv, Action
from agents.baseline_agent import BaselineAgent

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger("RealWorldActuator")

def execute_in_real_world(action: Action):
    """
    Translates abstract RL Environment actions into real-world OS/Browser commands.
    """
    time.sleep(2) # Add natural delay to watch execution natively
    
    if action.action_type == "open_browser":
        url = action.parameters.get("url", "https://google.com")
        if not url.startswith("http"):
            url = f"https://{url}"
        logger.info(f"REAL WORLD ACTUATOR: Opening browser tab to {url}")
        webbrowser.open(url)
        
    elif action.action_type == "search_query":
        query = action.parameters.get("query", "")
        encoded_query = urllib.parse.quote(query)
        # Assuming youtube context based on task design
        search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
        logger.info(f"REAL WORLD ACTUATOR: Searching YouTube for '{query}'")
        webbrowser.open(search_url)

    elif action.action_type == "play_video":
        video = action.parameters.get("video", "")
        logger.info(f"REAL WORLD ACTUATOR: Executing click target video -> {video}")
        # Real-world playing would require Selenium/PyAutoGUI for a specific target element click.
        # We will log the intended click execution for browser focus.
        
    elif action.action_type == "send_email":
        to = action.parameters.get("to", "unknown@mail.com")
        logger.info(f"REAL WORLD ACTUATOR: Triggering mailto client to {to}")
        webbrowser.open(f"mailto:{to}")
        
    elif action.action_type == "idle":
        logger.info("REAL WORLD ACTUATOR: System is idling...")


def run_realworld_task(task_name: str):
    logger.info(f"\n--- Booting JARVIS Actuator for {task_name.upper()} ---")
    
    env = JarvisEnv(task_name=task_name)
    agent = BaselineAgent(task_name=task_name)
    
    state = env.reset()
    done = False
    
    while not done:
        # 1. Agent determines next action
        action = agent.act(state)
        
        # 2. Trigger real world execution wrapper
        logger.info(f">> Agent Action Selected: {action.action_type}")
        execute_in_real_world(action)
        
        # 3. Environment updates logical state
        state, reward, done, info = env.step(action)
        
    logger.info(f"Task {task_name.upper()} Automation Simulation Complete.\n")

if __name__ == "__main__":
    logger.info("WARNING: This will open active tabs on your local desktop!\n")
    
    # We will simulate the "hard" task logic track to see it dynamically execute!
    run_realworld_task("hard")
