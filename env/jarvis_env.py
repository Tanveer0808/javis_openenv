import logging
from dataclasses import dataclass, asdict
from typing import Dict, Any

from tasks.task_definitions import get_goal_evaluator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("JarvisEnv")

@dataclass
class State:
    user_command: str
    system_status: str
    current_step: int
    progress: float

@dataclass
class Action:
    action_type: str
    parameters: dict

class JarvisEnv:
    """
    Simulation-based Virtual Assistant RL Environment with dynamic goal progressions.
    """
    
    def __init__(self, task_name: str = "easy"):
        self.task_name = task_name.lower()
        self.max_steps = 10
        self.goal_evaluator = get_goal_evaluator(self.task_name)
        self.reset()

    def _get_task_command(self) -> str:
        if self.task_name == "easy":
            return "Open YouTube"
        elif self.task_name == "medium":
            return "Search and play a video"
        elif self.task_name == "hard":
            return "Play latest IPL highlights"
        return "Unknown task"

    def reset(self) -> Dict[str, Any]:
        """Resets the environment"""
        self.state_data = State(
            user_command=self._get_task_command(),
            system_status="idle",
            current_step=0,
            progress=0.0
        )
        logger.info(f"JarvisEnv reset for task: {self.task_name}")
        return self.state()

    def state(self) -> Dict[str, Any]:
        """Returns observation space represented as a dictionary"""
        return asdict(self.state_data)

    def step(self, action: Action) -> tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Dynamically executes action, calculates partial progress against the
        task goal, and returns standardized RL payload.
        """
        self.state_data.current_step += 1
        reward = 0.0
        done = False
        info = {}

        action_type = action.action_type
        params = action.parameters

        logger.debug(f"Executing: {action_type} with parameters {params}")

        # Store previous progress to calculate delta
        previous_progress = self.state_data.progress

        # 1. Dynamic Environment Transition
        if action_type == "open_browser":
            if "browser:open" in self.state_data.system_status:
                self.state_data.system_status = "error: browser already open"
                reward -= 0.05
            else:
                target = params.get('url', 'google.com')
                self.state_data.system_status = f"browser:open | url:{target}"
                
        elif action_type == "search_query":
            if "browser:open" not in self.state_data.system_status:
                self.state_data.system_status = "error: cannot search without browser"
                reward -= 0.1
            else:
                query = params.get('query', 'unknown')
                self.state_data.system_status = f"browser:open | search_results: '{query}'"
                
        elif action_type == "play_video":
            if "browser:open" not in self.state_data.system_status:
                self.state_data.system_status = "error: cannot play video, no browser"
                reward -= 0.1
            else:
                video = params.get('video', 'unknown')
                self.state_data.system_status = f"browser:open | playing_video: '{video}'"
                
        elif action_type == "fetch_trending":
            if "browser:open" not in self.state_data.system_status:
                self.state_data.system_status = "error: cannot fetch trending without browser"
                reward -= 0.05
            else:
                self.state_data.system_status = "browser:open | trending_page_loaded"

        elif action_type == "idle":
            self.state_data.system_status = "idle"
            reward -= 0.01

        else:
            self.state_data.system_status = f"error: unrecognized native action {action_type}"
            reward -= 0.1

        # 2. Dynamic Goal Evaluation
        new_progress = self.goal_evaluator(self.state_data.system_status)
        self.state_data.progress = float(new_progress)
        
        # 3. Progressive Reward Assignment
        progress_delta = self.state_data.progress - previous_progress
        if progress_delta > 0:
            reward += progress_delta * 0.8  # Partial reward scaling
            
        # 4. Termination Logic
        if self.state_data.current_step >= self.max_steps:
            done = True
            info["reason"] = "max_steps"

        if self.state_data.progress >= 1.0:
            done = True
            info["reason"] = "goal_achieved"
            reward += 0.15  # Final completion scaling to keep total score strictly < 1.0 (approx 0.95)

        return self.state(), reward, done, info
