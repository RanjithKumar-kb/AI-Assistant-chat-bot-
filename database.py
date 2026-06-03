import json
import os
import time

DB_FILE = "chat_sessions.json"

def load_all_chats():
    """Loads all chat sessions from the JSON file."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_chat_session(session_id, history):
    """Saves a specific chat session."""
    all_chats = load_all_chats()
    all_chats[session_id] = {
        "title": history[1]["content"][:30] if len(history) > 1 else "New Chat",
        "messages": history,
        "timestamp": time.time()
    }
    with open(DB_FILE, "w") as f:
        json.dump(all_chats, f, indent=4)

def get_chat_history(session_id):
    """Retrieves a specific chat by ID."""
    all_chats = load_all_chats()
    if session_id in all_chats:
        return all_chats[session_id]["messages"]
    return [{"role": "system", "content": "You are Lumina, a local AI assistant."}]

def delete_chat_session(session_id):
    """Removes a specific chat session from the database."""
    all_chats = load_all_chats()
    if session_id in all_chats:
        del all_chats[session_id]
        with open(DB_FILE, "w") as f:
            json.dump(all_chats, f, indent=4)
        return True
    return False