import threading
import uuid
import os # Import os for environment variables
import logging # Import logging
import functools
from contextlib import contextmanager
import requests # Added for monkey-patching
from urllib.parse import urlparse # Added for URL parsing

# Define thread-local
_thread_local = threading.local()

# Global dictionary to store cross-thread sessions by name
# This will allow us to maintain session continuity between threads
_global_sessions_by_name = {}

# Global parent thread tracker
_parent_thread_sessions = {}

# Store original requests.Session.send method
_original_requests_session_send = requests.Session.send

# Initialize thread-local storage
def _init_thread_local():
    if not hasattr(_thread_local, 'session_stack'):
        _thread_local.session_stack = []
    if not hasattr(_thread_local, 'named_sessions'):
        _thread_local.named_sessions = {}
    if not hasattr(_thread_local, 'session_id'):
        _thread_local.session_id = None
    if not hasattr(_thread_local, 'current_session_name'):
        _thread_local.current_session_name = None
    if not hasattr(_thread_local, 'patch_count'): # Added patch_count
        _thread_local.patch_count = 0

def _patched_requests_session_send(session_instance, request, **kwargs):
    """
    Patched version of requests.Session.send that adds Tropir session headers.
    """
    # Add Session ID header if available
    session_id = get_session_id()
    if session_id:
        request.headers["X-Session-ID"] = str(session_id)
        logging.debug(f"Tropir Session: Added X-Session-ID to headers: {session_id}")
    else:
        logging.debug("Tropir Session: No active session ID found, X-Session-ID header not added.")

    # Add Session Name header if available
    session_name = get_session_name()
    if session_name:
        request.headers["X-Session-Name"] = str(session_name)
        logging.debug(f"Tropir Session: Added X-Session-Name to headers: {session_name}")
    else:
        logging.debug("Tropir Session: No active session name found, X-Session-Name header not added.")

    # Add Tropir API key if available and URL matches
    tropir_api_key = os.environ.get("TROPIR_API_KEY")
    if tropir_api_key:
        parsed_url = urlparse(request.url)
        hostname = parsed_url.hostname
        port = parsed_url.port
        
        if (hostname == "api.tropir.com") or \
           (hostname == "localhost" and port == 8080) or \
           (hostname == "host.docker.internal" and port == 8080): # Added host.docker.internal for Dockerized dev
            request.headers["X-TROPIR-API-KEY"] = tropir_api_key
            logging.debug("Tropir Session: Added X-TROPIR-API-KEY to headers for URL: %s", request.url)
        else:
            logging.debug("Tropir Session: TROPIR_API_KEY found, but URL %s does not match target hosts (api.tropir.com, localhost:8080, host.docker.internal:8080). Skipping header.", request.url)
    else:
        logging.debug("Tropir Session: TROPIR_API_KEY not found in environment variables, skipping header.")
        
    return _original_requests_session_send(session_instance, request, **kwargs)

def _apply_requests_patch_if_needed():
    _init_thread_local() # Ensure patch_count is initialized
    if _thread_local.patch_count == 0:
        requests.Session.send = _patched_requests_session_send
        logging.debug("Tropir Session: Patched requests.Session.send.")
    _thread_local.patch_count += 1

def _revert_requests_patch_if_needed():
    _init_thread_local() # Ensure patch_count is available
    if hasattr(_thread_local, 'patch_count') and _thread_local.patch_count > 0:
        _thread_local.patch_count -= 1
        if _thread_local.patch_count == 0:
            requests.Session.send = _original_requests_session_send
            logging.debug("Tropir Session: Reverted requests.Session.send to original.")
    elif hasattr(_thread_local, 'patch_count') and _thread_local.patch_count == 0 :
        # This case can happen if revert is called more times than apply.
        # Ensure the original send is still set if patch_count is 0.
        if requests.Session.send != _original_requests_session_send:
             requests.Session.send = _original_requests_session_send
             logging.warning("Tropir Session: patch_count was already 0 but requests.Session.send was not original. Reverted.")

def _inherit_parent_session():
    """Inherit session from parent thread if available."""
    current_thread = threading.current_thread()
    
    # Skip for MainThread since it has no parent
    if current_thread.name == 'MainThread':
        return
    
    # Check if there's a parent session we can inherit
    if 'MainThread' in _parent_thread_sessions:
        parent_session = _parent_thread_sessions['MainThread']
        if parent_session:
            session_id, session_name = parent_session
            set_session_id(session_id, session_name)
            logging.debug(f"Thread {current_thread.name} inherited session {session_name} ({session_id}) from MainThread")

def get_session_id():
    """Get the current session ID.
    
    First checks thread-local storage, then tries to inherit from parent thread if needed.
    
    Returns:
        str or None: The current session ID if one exists, otherwise None.
    """
    _init_thread_local()
    
    # Check thread-local stack first
    if _thread_local.session_stack:
        return _thread_local.session_stack[-1]
    
    # Then check thread-local session ID
    if _thread_local.session_id:
        return _thread_local.session_id
    
    # Try to inherit from parent if we don't have a session yet
    _inherit_parent_session()
    
    # Check again after potential inheritance
    if _thread_local.session_stack:
        return _thread_local.session_stack[-1]
    if _thread_local.session_id:
        return _thread_local.session_id
    
    # No session found
    return None

def get_session_name():
    """Get the current session name, if any."""
    _init_thread_local()
    
    # Try to inherit from parent if we don't have a session yet
    if not hasattr(_thread_local, 'current_session_name') or not _thread_local.current_session_name:
        _inherit_parent_session()
        
    return getattr(_thread_local, 'current_session_name', None)

def set_session_id(session_id, session_name=None):
    """Set the session ID for the current thread.
    
    Also registers the session ID globally for cross-thread usage.
    
    Args:
        session_id: The session ID to set
        session_name: Optional name to associate with this session
    """
    _init_thread_local()
    _thread_local.session_id = session_id
    
    # Register in global sessions for inheritance by child threads
    current_thread = threading.current_thread().name
    _parent_thread_sessions[current_thread] = (session_id, session_name)
    
    if session_name:
        _thread_local.current_session_name = session_name
        if not hasattr(_thread_local, 'named_sessions'):
            _thread_local.named_sessions = {}
        _thread_local.named_sessions[session_name] = session_id
        
        # Store in global sessions by name
        _global_sessions_by_name[session_name] = session_id

def clear_session_id():
    """Clear the session ID for the current thread."""
    _init_thread_local()
    _thread_local.session_id = None
    _thread_local.session_stack = []
    
    # Don't clear named sessions dictionary - we want persistence
    # But do clear current session name
    _thread_local.current_session_name = None
    
    # Remove from parent thread register
    current_thread = threading.current_thread().name
    if current_thread in _parent_thread_sessions:
        del _parent_thread_sessions[current_thread]

@contextmanager
def session(session_name=None):
    """Context manager for defining session boundaries.
    
    Args:
        session_name: Optional name for the session. If provided and this
                     session has been used before, the same session ID will be reused.
    """
    _init_thread_local()
    previous_stack = list(_thread_local.session_stack)  # Create a copy of the stack
    previous_session_name = _thread_local.current_session_name
    
    # Generate or retrieve session ID
    # First check thread-local named sessions
    if session_name and session_name in _thread_local.named_sessions:
        session_id = _thread_local.named_sessions[session_name]
    # Then check global sessions by name
    elif session_name and session_name in _global_sessions_by_name:
        session_id = _global_sessions_by_name[session_name]
        # Copy to thread-local too
        _thread_local.named_sessions[session_name] = session_id
    else:
        session_id = str(uuid.uuid4())
        if session_name:
            _thread_local.named_sessions[session_name] = session_id
            _global_sessions_by_name[session_name] = session_id
    
    # Push session ID to the stack and set current session name
    _thread_local.session_stack.append(session_id)
    _thread_local.current_session_name = session_name
    
    # Register in parent thread sessions for inheritance by child threads
    current_thread = threading.current_thread().name
    _parent_thread_sessions[current_thread] = (session_id, session_name)
    
    _apply_requests_patch_if_needed() # Apply patch
    logging.debug(f"Started session: {session_name or 'unnamed'} with ID: {session_id} on thread {current_thread}")
    
    try:
        yield session_id
    finally:
        # Restore previous stack state and session name
        _thread_local.session_stack = previous_stack
        _thread_local.current_session_name = previous_session_name
        
        # Update parent thread sessions register with previous state
        if previous_session_name:
            prev_id = _thread_local.named_sessions.get(previous_session_name)
            if prev_id:
                _parent_thread_sessions[current_thread] = (prev_id, previous_session_name)
        elif not previous_stack and not previous_session_name:
            # If we're ending all sessions, remove from parent thread register
            if current_thread in _parent_thread_sessions:
                del _parent_thread_sessions[current_thread]
        
        _revert_requests_patch_if_needed() # Revert patch       
        logging.debug(f"Ended session: {session_name or 'unnamed'} on thread {current_thread}")

def begin_session(session_name=None):
    """Decorator or function to begin a session.
    
    This can be used as a decorator around a function or as a function call
    to mark the beginning of a session.
    
    Args:
        session_name: Optional name for the session. If provided and this
                     session has been used before, the same session ID will be reused.
    """
    _init_thread_local()
    
    # When used as a decorator
    if callable(session_name):
        func = session_name
        session_name = func.__name__  # Use function name as session name if not provided
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Use the context manager to handle sessions properly
            with session(session_name):
                return func(*args, **kwargs)
        return wrapper
    
    # When used as a function or decorator with name
    else:
        # When used as a decorator with a name
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                # Use the context manager to handle sessions properly
                with session(session_name):
                    return func(*args, **kwargs)
            return wrapper
        
        # When used as a function call
        if session_name is not None:
            # Generate or retrieve session ID
            # First check thread-local named sessions
            if session_name in _thread_local.named_sessions:
                session_id = _thread_local.named_sessions[session_name]
            # Then check global sessions by name
            elif session_name in _global_sessions_by_name:
                session_id = _global_sessions_by_name[session_name]
                # Copy to thread-local too
                _thread_local.named_sessions[session_name] = session_id
            else:
                session_id = str(uuid.uuid4())
                _thread_local.named_sessions[session_name] = session_id
                _global_sessions_by_name[session_name] = session_id
            
            # Push session ID to the stack and set current session name
            _thread_local.session_stack.append(session_id)
            _thread_local.current_session_name = session_name
            
            # Register in parent thread sessions for inheritance by child threads
            current_thread = threading.current_thread().name
            _parent_thread_sessions[current_thread] = (session_id, session_name)
            
            _apply_requests_patch_if_needed() # Apply patch
            logging.debug(f"Started session: {session_name} with ID: {session_id} on thread {current_thread}")
        
        return decorator

def end_session(session_name=None):
    """Function to end a session.
    
    Args:
        session_name: Optional name of the session to end. If not provided,
                     the most recent session will be ended.
    """
    _init_thread_local()
    
    current_thread = threading.current_thread().name
    
    if _thread_local.session_stack:
        session_id = _thread_local.session_stack.pop()
        # Clear current session name if it matches the ended session
        if _thread_local.current_session_name == session_name:
            _thread_local.current_session_name = None
            # Remove from parent thread sessions if no more sessions
            if not _thread_local.session_stack:
                if current_thread in _parent_thread_sessions:
                    del _parent_thread_sessions[current_thread]
        
        _revert_requests_patch_if_needed() # Revert patch
        logging.debug(f"Ended session: {session_name or 'unnamed'} with ID: {session_id} on thread {current_thread}")
    else:
        logging.warning(f"Attempted to end session {session_name or 'unnamed'} but no active sessions found on thread {current_thread}")

# Monkey-patch threading.Thread to enable automatic session inheritance
_original_thread_init = threading.Thread.__init__

def _thread_init_with_session_inheritance(self, *args, **kwargs):
    # Call the original __init__
    _original_thread_init(self, *args, **kwargs)
    
    # Store the current thread's session info for inheritance
    if threading.current_thread().name in _parent_thread_sessions:
        self._parent_session = _parent_thread_sessions[threading.current_thread().name]
    else:
        self._parent_session = None

threading.Thread.__init__ = _thread_init_with_session_inheritance

# Monkey-patch threading.Thread.run to inherit session on start
_original_thread_run = threading.Thread.run

def _thread_run_with_session_inheritance(self):
    # Set up session inheritance if we have parent session info
    if hasattr(self, '_parent_session') and self._parent_session:
        session_id, session_name = self._parent_session
        if session_id and session_name:
            set_session_id(session_id, session_name)
            logging.debug(f"Thread {self.name} inherited session {session_name} ({session_id})")
    
    # Call the original run method
    _original_thread_run(self)

threading.Thread.run = _thread_run_with_session_inheritance 