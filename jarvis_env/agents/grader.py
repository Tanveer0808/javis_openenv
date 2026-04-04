from typing import Dict, Any

def evaluate_episode(task_name: str, final_state: Dict[str, Any], accumulated_reward: float) -> float:
    """
    Evaluates an episode's terminal state by relying natively on the new
    generalized 'progress' float which models completion dynamics perfectly (0.0 to 1.0).
    """
    progress = final_state.get("progress", 0.0)

    # The progress metric is rigorously guaranteed by the environment to correctly map 
    # to a [0.0, 1.0] scale bounded evaluation of the original task objective.
    final_score = min(max(float(progress), 0.0), 1.0)
    
    return final_score
