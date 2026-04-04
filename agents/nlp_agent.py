import re
from typing import Dict, Any
from env.jarvis_env import Action

class NLPAgent:
    """
    A lightweight Natural Language Processing pseudo-agent.
    Translates raw english user inputs natively into structured strict OpenEnv Actions.
    """
    def __init__(self):
        pass

    def parse_intent(self, text: str) -> Action:
        text = text.lower().strip()

        # 1. Open Browser Intent
        if "open" in text and ("browser" in text or "youtube" in text or "google" in text):
            url = "youtube.com" if "youtube" in text else "google.com"
            return Action(action_type="open_browser", parameters={"url": url})

        # 2. Search Query Intent
        if "search" in text or "find" in text or "look up" in text:
            # Extract query payload heuristically (everything after 'search for' or 'search')
            query = text
            if "search for " in text:
                query = text.split("search for ")[1]
            elif "search " in text:
                query = text.split("search ")[1]
            return Action(action_type="search_query", parameters={"query": query})

        # 3. Play Video Intent
        if "play" in text or "watch" in text:
            video = text
            if "play " in text:
                video = text.split("play ")[1]
            elif "watch " in text:
                video = text.split("watch ")[1]
            
            # Catch IPL highlights specific mapping
            if "ipl" in text:
                video = "IPL highlights"
                
            return Action(action_type="play_video", parameters={"video": video})

        # 4. Fetch Trending Intent
        if "trending" in text or "popular" in text:
            return Action(action_type="fetch_trending", parameters={})

        # 5. Fallback Default
        return Action(action_type="idle", parameters={"reason": "NLP Confidence Low"})

