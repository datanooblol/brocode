"""Command Line Interface for BroCode.

Provides CLI commands for registering LLM models and starting chat sessions.
"""
import click
import importlib.util
import sys
from pathlib import Path
# from brocode.chat import start_chat
from brocode.register import get_llm, save_model_registration, list_registered_models, set_default_model, get_default_model, remove_model
from brocode.flow import get_flow
from brocode.actions import Shared
from brocode.banner import show_banner
from broflow import state

@click.group(epilog="""\b
Examples:
  Register a model and set as default:
    brocode register --path mylocal.py --model mylocal --default
  
  List all registered models:
    brocode model list
  
  Start chat with default model:
    brocode start
  
  Start chat with specific model:
    brocode start --llm mylocal""", invoke_without_command=True)
@click.version_option()
@click.pass_context
def main(ctx):
    """BroCode - CLI tool for managing and running LLM-based chat agents."""
    if ctx.invoked_subcommand is None:
        show_banner()

@main.command()
@click.option('--llm', help='LLM to use (uses default if not specified)')
@click.option('--debug', type=bool, default=False, help='Enable debug mode (True/False)')
def start(llm, debug):
    """Start chat session."""
    from brocode.register import ensure_brosession_dir, SESSION_DB, copy_prompt_hub
    
    # Display banner
    show_banner()
    
    # Setup brosession directory structure
    ensure_brosession_dir()
    copy_prompt_hub()
    SESSION_DB.touch(exist_ok=True)
    
    llm_name = llm or get_default_model() or "echo"
    model = get_llm(llm_name)
    state.set("debug", debug)
    flow = get_flow(model)
    shared = Shared()
    flow.run(shared)

@main.command()
@click.option('--path', required=True, help='Path to Python file containing LLM model class')
@click.option('--model', help='Model name (uses filename if not provided)')
@click.option('--default', is_flag=True, help='Set as default model')
def register(path, model, default):
    """Register a new model."""
    path_obj = Path(path)
    if not path_obj.exists():
        click.echo(f"Error: File {path_obj} not found")
        return
        
    spec = importlib.util.spec_from_file_location(path_obj.stem, path_obj)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path_obj.stem] = module
    spec.loader.exec_module(module)
    
    model_name = model or path_obj.stem
    save_model_registration(model_name, str(path_obj.absolute()))
    
    if default:
        set_default_model(model_name)
        click.echo(f"Registered model '{model_name}' from {path_obj} and set as default")
    else:
        click.echo(f"Registered model '{model_name}' from {path_obj}")

@main.group()
def model():
    """Model management commands."""
    pass

@model.command('list')
def list_models():
    """List all registered models."""
    models = list_registered_models()
    default_model = get_default_model()
    if models:
        click.echo("Registered models:")
        for name, path in models.items():
            default_marker = " (default)" if name == default_model else ""
            click.echo(f"  {name}: {path}{default_marker}")
    else:
        click.echo("No models registered. Use 'brocode register --path <file>' to add models.")

@model.command()
def remove():
    """Remove a registered model."""
    models = list_registered_models()
    if not models:
        click.echo("No models registered.")
        return
    
    click.echo("Select a model to remove:")
    model_list = list(models.keys())
    for i, name in enumerate(model_list, 1):
        click.echo(f"  {i}. {name}")
    
    try:
        choice = click.prompt("Enter number (0 to cancel)", type=int)
        if choice == 0:
            click.echo("Cancelled.")
            return
        if 1 <= choice <= len(model_list):
            model_name = model_list[choice - 1]
            remove_model(model_name)
            click.echo(f"Removed model '{model_name}'")
        else:
            click.echo("Invalid selection.")
    except (click.Abort, KeyboardInterrupt):
        click.echo("\nCancelled.")

@model.command()
def config():
    """Show config file location."""
    from brocode.register import CONFIG_FILE
    click.echo(f"Config file location: {CONFIG_FILE}")
    if CONFIG_FILE.exists():
        click.echo("Config file exists.")
    else:
        click.echo("Config file does not exist yet.")

