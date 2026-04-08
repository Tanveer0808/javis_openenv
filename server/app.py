import os
import sys
import yaml
import uuid
import logging
from dataclasses import asdict
from flask import Flask, jsonify, send_from_directory, request

# Add project root to sys.path to allow imports from env and agents
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from env.jarvis_env import JarvisEnv, Action
from agents.baseline_agent import BaselineAgent
from agents.nlp_agent import NLPAgent
from agents.grader import evaluate_episode
from agents.realworld_actuator import execute_in_real_world

app = Flask(__name__, static_folder='static')
app.logger.setLevel(logging.INFO)

# In-memory session tracking for interactive UI environments
ACTIVE_SESSIONS = {}
nlp_agent = NLPAgent()

def load_tasks(config_path: str):
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config.get('tasks', [])

@app.route('/reset', methods=['POST'])
def openenv_reset():
    """Provides a standard /reset POST endpoint for OpenEnv integration."""
    data = request.get_json(silent=True) or {}
    task_name = data.get('task_name', data.get('task', 'easy')).lower()
    
    env = JarvisEnv(task_name=task_name)
    ACTIVE_SESSIONS['openenv_master'] = {
        "env": env,
        "task": task_name,
        "accumulated_reward": 0.0,
        "step_count": 0
    }
    
    state = env.reset()
    return jsonify(state)

@app.route('/step', methods=['POST'])
def openenv_step():
    """Provides a standard /step POST endpoint for OpenEnv integration."""
    data = request.get_json(silent=True) or {}
    
    session_data = ACTIVE_SESSIONS.get('openenv_master')
    if not session_data:
        env = JarvisEnv()
        ACTIVE_SESSIONS['openenv_master'] = {
            "env": env,
            "task": "easy",
            "accumulated_reward": 0.0,
            "step_count": 0
        }
        session_data = ACTIVE_SESSIONS['openenv_master']
        
    env = session_data["env"]
    
    # Handle action whether wrapped in "action" key or direct
    action_dict = data.get('action', data)
    action_type = action_dict.get('action_type', 'idle')
    parameters = action_dict.get('parameters', {})
    
    action = Action(action_type=action_type, parameters=parameters)
    next_state, reward, done, info = env.step(action)
    
    session_data["accumulated_reward"] += reward
    session_data["step_count"] += 1
    
    if done and "final_score" not in info:
        info["final_score"] = evaluate_episode(session_data["task"], next_state, session_data["accumulated_reward"])
        
    # Send both observation and state keys just to be safe with standard formats
    return jsonify({
        "observation": next_state,
        "obs": next_state,
        "state": next_state,
        "reward": float(reward),
        "done": bool(done),
        "info": info
    })

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/env/start', methods=['POST'])
def start_interactive_session():
    """Initializes a new interactive RL session based on task"""
    data = request.json
    task_name = data.get('task', 'easy').lower()
    
    session_id = str(uuid.uuid4())
    env = JarvisEnv(task_name=task_name)
    initial_state = env.state()
    
    ACTIVE_SESSIONS[session_id] = {
        "env": env,
        "task": task_name,
        "accumulated_reward": 0.0,
        "step_count": 0
    }
    
    return jsonify({
        "session_id": session_id,
        "state": initial_state
    })

@app.route('/api/env/nlp_step', methods=['POST'])
def handle_nlp_step():
    """Takes user NLP commands, steps the env, AND ACTUATES in the real world physical layer"""
    data = request.json
    session_id = data.get('session_id')
    user_input = data.get('input', '')
    
    session_data = ACTIVE_SESSIONS.get(session_id)
    if not session_data:
        return jsonify({"error": "Invalid or expired session"}), 400
        
    env = session_data["env"]
    
    # 1. Parse string through NLP to abstract Action
    action = nlp_agent.parse_intent(user_input)
    
    # 2. TRIGGER REAL WORLD PHYSICAL ACTUATOR
    # This simulates actual physical action on the host machine running the server
    execute_in_real_world(action)
    
    # 3. Step Abstract OpenEnv state execution mapping progression logic
    next_state, reward, done, info = env.step(action)
    
    session_data["accumulated_reward"] += reward
    session_data["step_count"] += 1
    
    payload = {
        "action_parsed": asdict(action),
        "reward": round(reward, 2),
        "next_state": next_state,
        "done": done,
        "info": info
    }
    
    if done:
        final_score = evaluate_episode(session_data["task"], next_state, session_data["accumulated_reward"])
        payload["final_score"] = final_score
        
    return jsonify(payload)

def main():
    port = int(os.environ.get("PORT", 7860))
    # Using threaded logic for smooth local execution and actution
    app.run(host='0.0.0.0', port=port, debug=True, threaded=True)

if __name__ == '__main__':
    main()
