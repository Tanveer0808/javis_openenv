from typing import Dict, Any

class BaselineAgent:
    """
    A rule-based baseline agent mapping tasks to explicit sequential actions, 
    but now interacting cleanly with the dynamic generalized state mapping.
    """
    from env.jarvis_env import Action
    
    def __init__(self, task_name: str):
        self.task_name = task_name.lower()
        self.step_idx = 0
        from env.jarvis_env import Action
        self.plan = self._create_scripted_plan()

    def _create_scripted_plan(self) -> list:
        from env.jarvis_env import Action
        if self.task_name == "easy":
            return [
                Action(action_type="open_browser", parameters={"url": "youtube.com"})
            ]
        elif self.task_name == "medium":
            return [
                Action(action_type="open_browser", parameters={"url": "youtube.com"}),
                Action(action_type="search_query", parameters={"query": "cute cats"}),
                Action(action_type="play_video", parameters={"video": "cute cats compilation"})
            ]
        elif self.task_name == "hard":
            return [
                Action(action_type="open_browser", parameters={"url": "youtube.com"}),
                Action(action_type="search_query", parameters={"query": "IPL highlights 2024 final match"}),
                Action(action_type="play_video", parameters={"video": "IPL highlights"})
            ]
        else:
            return []

    def act(self, state: Dict[str, Any]):
        """
        Returns the next Action based on the internal unrolled script.
        """
        from env.jarvis_env import Action
        if self.step_idx < len(self.plan):
            action = self.plan[self.step_idx]
            self.step_idx += 1
            return action
        else:
            return Action(action_type="idle", parameters={})

    def reset(self):
        self.step_idx = 0
