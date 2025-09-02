"""LLM Model Registry for BroCode.

Manages registration and retrieval of LLM models with persistent storage.
"""
# brocode/llm/registry.py
import yaml              # For YAML file operations
import importlib.util    # For dynamic module importing
import sys              # For system module management
from pathlib import Path # For file path operations
from typing import Dict, Type # For type hints
from brollm import BaseLLM    # Base LLM class

# In-memory registry of LLM classes
LLM_REGISTRY: Dict[str, Type[BaseLLM]] = {}
# Create brosession directory structure
BROSESSION_DIR = Path.cwd() / "brosession"
CONFIG_FILE = BROSESSION_DIR / "brocode_config.yaml"
SESSION_DB = BROSESSION_DIR / "session.db"
PROMPT_HUB_DIR = BROSESSION_DIR / "prompt_hub"

def ensure_brosession_dir():
    """Ensure brosession directory exists."""
    BROSESSION_DIR.mkdir(exist_ok=True)

def copy_prompt_hub():
    """Copy missing files from brocode/prompt_hub to brosession/prompt_hub."""
    import shutil
    
    # Always ensure directory exists
    PROMPT_HUB_DIR.mkdir(exist_ok=True)
    
    # Get source prompt_hub directory from package
    source_dir = Path(__file__).parent / 'prompt_hub'
    
    # Copy only missing files from source to destination
    if source_dir.exists():
        for file_path in source_dir.iterdir():
            if file_path.is_file():  # Only copy files, not directories
                dest_file = PROMPT_HUB_DIR / file_path.name
                # Only copy if file doesn't exist
                if not dest_file.exists():
                    shutil.copy2(file_path, dest_file)
                    print(f"📋 Copied {file_path.name} to brosession/prompt_hub/")
                # Skip if file already exists

def _load_registered_models():
    """Load previously registered models from persistent storage."""
    # Check if config file exists
    if CONFIG_FILE.exists():
        # Load config from YAML file
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {}
        # Get models section from config
        models = config.get('models', {})
        # Import each registered model
        for name, path in models.items():
            _import_model(path)

def _import_model(path: str):
    """Import a model from the given file path.
    
    Args:
        path: File path to the Python module containing the model
    """
    path_obj = Path(path)
    # Only import if file exists
    if path_obj.exists():
        # Create module specification from file
        spec = importlib.util.spec_from_file_location(path_obj.stem, path_obj)
        # Create module object
        module = importlib.util.module_from_spec(spec)
        # Add to system modules
        sys.modules[path_obj.stem] = module
        # Execute module (triggers @register_llm decorator)
        spec.loader.exec_module(module)

def save_model_registration(name: str, path: str):
    """Save model registration to persistent storage.
    
    Args:
        name: Name to register the model under
        path: File path to the model implementation
    """
    ensure_brosession_dir()
    config = {'models': {}}
    # Load existing config if file exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {'models': {}}
    # Ensure models section exists
    if 'models' not in config:
        config['models'] = {}
    # Add new model registration
    config['models'][name] = path
    # Save updated config
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def register_llm(name: str):
    """Decorator to register an LLM class in the registry.
    
    Args:
        name: Name to register the LLM under
        
    Returns:
        Decorator function that registers the class
    """
    def wrapper(cls: Type[BaseLLM]):
        # Add class to registry
        LLM_REGISTRY[name] = cls
        return cls
    return wrapper

def get_llm(name: str, **kwargs) -> BaseLLM:
    """Get an LLM instance by name.
    
    Args:
        name: Name of the registered LLM
        **kwargs: Arguments to pass to LLM constructor
        
    Returns:
        Instantiated LLM object
        
    Raises:
        ValueError: If LLM name is not registered
    """
    # Always load registered models to ensure they're available
    _load_registered_models()
    # Check if LLM exists after loading
    if name not in LLM_REGISTRY:
        raise ValueError(f"Unknown LLM: {name}")
    # Return instantiated LLM
    return LLM_REGISTRY[name](**kwargs)

def list_registered_models() -> Dict[str, str]:
    """Get all registered models from config file.
    
    Returns:
        Dictionary mapping model names to file paths
    """
    # Check if config file exists
    if CONFIG_FILE.exists():
        # Load config from YAML file
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {}
        # Return models section
        return config.get('models', {})
    return {}

def set_default_model(name: str):
    """Set a model as the default.
    
    Args:
        name: Name of the model to set as default
    """
    ensure_brosession_dir()
    config = {'models': {}}
    # Load existing config if file exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {'models': {}}
    # Set default model
    config['default_model'] = name
    # Save updated config
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

def get_default_model() -> str:
    """Get the default model name.
    
    Returns:
        Name of the default model, or None if not set
    """
    # Check if config file exists
    if CONFIG_FILE.exists():
        # Load config from YAML file
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {}
        # Return default model
        return config.get('default_model')
    return None

def remove_model(name: str):
    """Remove a model from the registry.
    
    Args:
        name: Name of the model to remove
    """
    ensure_brosession_dir()
    config = {'models': {}}
    # Load existing config if file exists
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config = yaml.safe_load(f) or {'models': {}}
    
    # Remove model from config
    if 'models' in config and name in config['models']:
        del config['models'][name]
    
    # Clear default if removing default model
    if config.get('default_model') == name:
        config.pop('default_model', None)
    
    # Save updated config
    with open(CONFIG_FILE, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
