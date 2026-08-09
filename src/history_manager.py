import json
import os
from datetime import datetime
from typing import List, Dict, Any

def load_history(path: str) -> List[Dict[str, Any]]:
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def add_history(path: str, entry: Dict[str, Any]) -> None:
    history = load_history(path)
    entry["timestamp"] = datetime.now().isoformat()
    history.append(entry)
    
    # Cap history at 50 entries to keep file size reasonable
    if len(history) > 50:
        history = history[-50:]
        
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
    except OSError:
        pass
        
    with open(path, "w", encoding="utf-8") as file:
        json.dump(history, file, indent=2)
