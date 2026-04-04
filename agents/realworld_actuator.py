import time
import logging
import webbrowser
import urllib.parse
from env.jarvis_env import Action

logger = logging.getLogger("RealWorldActuator")

def execute_in_real_world(action: Action):
    """
    Translates abstract structured RL Environment actions directly into real-world OS/Browser commands.
    """
    if action.action_type == "open_browser":
        url = action.parameters.get("url", "https://google.com")
        if not url.startswith("http"):
            url = f"https://{url}"
        logger.info(f"REAL WORLD ACTUATOR: Opening browser tab to {url}")
        webbrowser.open(url)
        
    elif action.action_type == "search_query":
        query = action.parameters.get("query", "")
        if query:
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.youtube.com/results?search_query={encoded_query}"
            logger.info(f"REAL WORLD ACTUATOR: Searching YouTube for '{query}'")
            webbrowser.open(search_url)

    elif action.action_type == "play_video":
        video = action.parameters.get("video", "")
        logger.info(f"REAL WORLD ACTUATOR: Target click video '{video}'")
        # In a generic browser environment, navigating to a video requires selenium or direct links.
        # As an actuator simulation placeholder, we log intent.
        
    elif action.action_type == "fetch_trending":
        logger.info(f"REAL WORLD ACTUATOR: Fetching trending page")
        webbrowser.open("https://www.youtube.com/feed/trending")
        
    elif action.action_type == "send_email":
        to = action.parameters.get("to", "unknown@mail.com")
        logger.info(f"REAL WORLD ACTUATOR: Triggering mailto client to {to}")
        webbrowser.open(f"mailto:{to}")
        
    elif action.action_type == "idle":
        pass
