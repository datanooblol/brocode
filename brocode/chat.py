"""Chat functionality for BroCode.

Provides interactive chat interface with LLM models.
"""
import click
from brollm import BaseLLM

def start_chat(model: BaseLLM):
    """Start an interactive chat session with the given LLM model.
    
    Args:
        model: The LLM instance to use for generating responses
    """
    # Main chat loop
    while True:
        # Get user input
        user_input = click.prompt("You", prompt_suffix=": ")
        # Set system prompt for the assistant
        system_prompt = "You're a helpful assistant"
        # Check for exit command
        if user_input.lower().startswith("/exit"):
            click.echo("good bye")
            break
        # Generate response using the LLM
        response = model.run(system_prompt=system_prompt, messages=[
            model.UserMessage(user_input)
        ])
        # Display the response
        click.echo(f"Bot: {response}")
        