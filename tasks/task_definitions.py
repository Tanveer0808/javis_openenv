from typing import Dict, Any

def evaluate_easy_goal(system_status: str) -> float:
    """Goal: Open YouTube"""
    if "youtube" in system_status.lower() and "browser:open" in system_status.lower():
        return 1.0
    elif "browser:open" in system_status.lower():
        return 0.5
    return 0.0

def evaluate_medium_goal(system_status: str) -> float:
    """Goal: Search and play a video"""
    progress = 0.0
    status = system_status.lower()
    
    if "browser:open" in status:
        progress = max(progress, 0.3)
    if "search_results:" in status:
        progress = max(progress, 0.6)
    if "playing_video:" in status:
        progress = max(progress, 1.0)
    return progress

def evaluate_hard_goal(system_status: str) -> float:
    """Goal: Play latest IPL highlights"""
    progress = 0.0
    status = system_status.lower()
    
    if "browser:open" in status:
        progress = max(progress, 0.2)
    if "search_results:" in status and "ipl" in status:
        progress = max(progress, 0.5)
    if "playing_video:" in status and "ipl" in status:
        progress = max(progress, 1.0)
    return progress

def get_goal_evaluator(task_name: str):
    task_name = task_name.lower()
    if task_name == "easy":
        return evaluate_easy_goal
    elif task_name == "medium":
        return evaluate_medium_goal
    elif task_name == "hard":
        return evaluate_hard_goal
    else:
        return lambda s: 0.0
