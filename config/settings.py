import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default application settings
DEFAULT_SETTINGS = {
    "app": {
        "theme": "system",  # system, light, dark
        "font_size": "medium",  # small, medium, large
        "save_history": True
    },
    "transcription": {
        "default_type": "cleaned",  # verbatim, cleaned
        "proofreading": True,
        "auto_transcribe": False
    },
    "chat": {
        "summary": True,
        "action_points": True,
        "topic_grouping": True,
        "default_template": "Meeting Summary"
    },
    "document": {
        "default_format": "pdf",  # pdf, docx
        "auto_export": False,
        "branding": {
            "enabled": False,
            "header": "",
            "footer": "",
            "logo_path": ""
        }
    },
    "storage": {
        "local_path": os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
        "max_history": 50
    }
}

# API settings
API_SETTINGS = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "whisper_model": "whisper-1",
        "gpt_model": "gpt-4"
    }
}

# File paths
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), "app_settings.json")
PRESETS_FILE = os.path.join(os.path.dirname(__file__), "presets.json")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.json")

def load_settings():
    """
    Load application settings from file
    
    Returns:
        dict: Application settings
    """
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {str(e)}")
    
    # Return default settings if file doesn't exist or error occurs
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    """
    Save application settings to file
    
    Args:
        settings (dict): Application settings
        
    Returns:
        bool: Success status
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)
        
        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving settings: {str(e)}")
        return False

def load_presets():
    """
    Load saved presets from file
    
    Returns:
        dict: Saved presets
    """
    if os.path.exists(PRESETS_FILE):
        try:
            with open(PRESETS_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading presets: {str(e)}")
    
    # Return empty dict if file doesn't exist or error occurs
    return {}

def save_preset(name, preset_data):
    """
    Save a preset to file
    
    Args:
        name (str): Preset name
        preset_data (dict): Preset data
        
    Returns:
        bool: Success status
    """
    try:
        # Load existing presets
        presets = load_presets()
        
        # Add or update preset
        presets[name] = preset_data
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(PRESETS_FILE), exist_ok=True)
        
        # Save presets
        with open(PRESETS_FILE, "w") as f:
            json.dump(presets, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving preset: {str(e)}")
        return False

def delete_preset(name):
    """
    Delete a preset
    
    Args:
        name (str): Preset name
        
    Returns:
        bool: Success status
    """
    try:
        # Load existing presets
        presets = load_presets()
        
        # Remove preset if it exists
        if name in presets:
            del presets[name]
            
            # Save presets
            with open(PRESETS_FILE, "w") as f:
                json.dump(presets, f, indent=4)
            return True
        return False
    except Exception as e:
        print(f"Error deleting preset: {str(e)}")
        return False

def load_history():
    """
    Load export history from file
    
    Returns:
        list: Export history
    """
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading history: {str(e)}")
    
    # Return empty list if file doesn't exist or error occurs
    return []

def add_to_history(history_item):
    """
    Add an item to export history
    
    Args:
        history_item (dict): History item with file_path, type, and date
        
    Returns:
        bool: Success status
    """
    try:
        # Load existing history
        history = load_history()
        
        # Add new item
        history.append(history_item)
        
        # Limit history size
        settings = load_settings()
        max_history = settings["storage"].get("max_history", 50)
        if len(history) > max_history:
            history = history[-max_history:]
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        
        # Save history
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=4)
        return True
    except Exception as e:
        print(f"Error adding to history: {str(e)}")
        return False