# flet_functions.py
# Flet version of functions.py - provides state management for Flet app

from loguru import logger

# Global app state reference
_app_state = None

def set_app_state(app_state):
    """Set the global app state reference"""
    global _app_state
    _app_state = app_state

def state(key):
    """Get a value from app state (equivalent to st.session_state access in Streamlit)"""
    global _app_state
    if _app_state is None:
        return None
    return _app_state.get(key)

def set_state(key, value):
    """Set a value in app state"""
    global _app_state
    if _app_state is not None:
        _app_state[key] = value

def trace(level=0):
    """Trace function for debugging (equivalent to original f.trace)"""
    if _app_state and _app_state.get('logger'):
        import inspect
        frame = inspect.currentframe().f_back
        func_name = frame.f_code.co_name
        line_num = frame.f_lineno
        file_name = frame.f_code.co_filename.split('/')[-1]
        _app_state['logger'].trace(f"TRACE {level}: {file_name}:{func_name}():{line_num}")

def get_app_state():
    """Get the entire app state dictionary"""
    global _app_state
    return _app_state if _app_state is not None else {}

def clear_state():
    """Clear all app state"""
    global _app_state
    if _app_state is not None:
        _app_state.clear()

# Additional utility functions that might be needed
def log_info(message):
    """Log an info message"""
    if _app_state and _app_state.get('logger'):
        _app_state['logger'].info(message)

def log_error(message):
    """Log an error message"""
    if _app_state and _app_state.get('logger'):
        _app_state['logger'].error(message)

def log_warning(message):
    """Log a warning message"""
    if _app_state and _app_state.get('logger'):
        _app_state['logger'].warning(message)