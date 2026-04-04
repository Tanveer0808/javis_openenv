# Jarvis Virtual Assistant RL Environment

This project implements a complete, submission-ready Reinforcement Learning environment mapped to an explicit Virtual Assistant logic track. It incorporates the precision-required OpenEnv specifications, grading protocols, and nested dataclasses modeled strictly for AI agent interaction.

## Project Structure

```
jarvis_env/
├── agents/             
│   ├── baseline_agent.py   # Baseline Agent acting exactly on State -> Action logic
│   └── grader.py           # Evaluation pipeline rating terminal states natively (0.0 to 1.0)
├── config/             
│   └── openenv.yaml        # OpenEnv strict configuration metrics
├── env/                
│   ├── jarvis_env.py       # Core Environment executing State & Action DataClasses
│   └── __init__.py 
├── scripts/            
│   └── run_baseline.py     # Reproducible inference loop tracking episodic evaluation scores
├── tasks/            
│   └── task_definitions.py # Declarative configuration dicts for strict evaluation tracks
├── static/                 # Front-end UI implementation dependencies
├── app.py                  # API bridge for dynamic UI interaction testing
├── Dockerfile              # Container architecture mapped for Hugging Face integration
├── requirements.txt
└── README.md
```

## Architecture: Spaces & Design

The environment encapsulates a real-world task design prioritizing web integration.

### Observational Space (State Dataclass)
The internal `State` is rigidly tracked by standard string typing, returning:
- `user_command` *(string)*: The requested task (e.g. "Search and play a video").
- `system_status` *(string)*: Deeply scoped internal simulation tracking (e.g. "browser opened: youtube.com").
- `current_step` *(int)*: The incremental time-metric preventing infinite looping.

### Action Space (Action Dataclass)
Any agent traversing the space must provide an `Action` dictating:
- `action_type` *(string enum)*: Enforced strictly to -> `open_browser`, `search_query`, `play_video`, `send_email`, `idle`.
- `parameters` *(Dict)*: Flexible parameter injection correlating to the executed type.

### Task Specifications
The module provides dense verification coverage across 3 tracks incrementally testing reasoning:
1. **Easy**: Open YouTube.
2. **Medium**: Search and play an arbitrary video.
3. **Hard**: Execute multi-step logical progression to strictly filter and play the latest IPL highlights.

### Normalized Reward Framework
Dense modeling pushes AI structures explicitly through local maximums by applying:
- `-0.1` deductions if hallucinatory sequential logic is flagged (e.g., executing a search query before navigating).
- `+0.2` intermediate verification benchmarks granting partial mapping success.
- `+1.0` explicit boundary score when the terminal goal verification evaluates True.

---

## Execution Instructions

Ensure you maintain your active Python environment:
```bash
pip install -r requirements.txt
export PYTHONPATH="$(pwd)"
```

### Reproducible Terminal Evaluation (Strict Protocol)
To execute the strict, text-based log evaluation directly on the unrolled environment sequences:
```bash
python scripts/run_baseline.py
```

### Dashboard UI Deployment
To execute the visual "Front-end" bridging the RL logs sequentially onto a Jarvis styled interaction UI panel:
```bash
python app.py
# -> Navigate to http://localhost:7860/
```

### Hugging Face Deployment
Use Docker to package the whole environment dynamically mapping internal ports:
```bash
docker build -t jarvis-env .
docker run -p 7860:7860 jarvis-env
```
