import click
import json
import os
import subprocess
import sys
from gitpt.utils.spinner import spinner
from gitpt.utils.llm_helper import CommentGenerator

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def load_config(config):
    """Pre Load config file with default values, or new values if set was run in past.

    Args:
        config (PATH): path to config file

    Returns:
        Config: List of values in config file
    """
    with open(os.path.join(__location__,config), 'r') as f:
        return json.load(f)
    

@click.group()
@click.option('--config-file', default='./config.json', help='Path to config file')
@click.pass_context
def cli(ctx, config_file):
    # Load config file and store in context object
    ctx.ensure_object(dict)
    ctx.obj['config'] = load_config(config_file)


## Function to show current config values set   
@cli.command('show_config')
@click.pass_context
def show_config(ctx):
    """Shows current config values set in file i.e. The Defaults"""
    config = ctx.obj['config']
    click.echo(f"Load config: {config}")


## Function to Set Config Values if you want them different from current
@cli.command('set')
@click.pass_context
@click.option('--style', type=click.Choice(['professional', 'funny', 'intrinsic'], case_sensitive=False), prompt=True, default=lambda: load_config('./config.json').get('style', ''))
@click.option('--length', prompt=True, type=click.IntRange(min=50, max=72), default=lambda: load_config('./config.json').get('length', ''))
@click.option('--llm', prompt=True, type=click.Choice(['ollama', 'openai', 'claude']), default=lambda: load_config('./config.json').get('llm', ''), help="LLM to use, (OpenAI, Ollama, Claude)")
@click.option('--model', prompt=True, default=lambda: load_config('./config.json').get('model', ''), help="LLM model to use (gemma2 for Ollama, gpt-4o for OpenAI)")
@click.option('--verbose', prompt=True, default=lambda: load_config('./config.json').get('verbose', ''))
@click.option('--open_ai_api', prompt=True, default=lambda: load_config('./config.json').get('open_ai_api', ''), help="API key for OpenAI account")
@click.option('--claude_ai_api', prompt=True, default=lambda: load_config('./config.json').get('claude_ai_api', ''), help="API key for Claude AI")
def set_config_values(ctx, **kwargs):
    """Allows user to set common values into a config file for use later. Entering without updating text
    saves values already in file. Adding new values overwrites previous values."
    """
    config = ctx.obj['config']
    
    for arg in kwargs:
        config[arg] = kwargs.get(arg)

    with open(os.path.join(__location__,'./config.json'), 'w') as f:
        json.dump(config, f, indent=4)
    
    click.echo(f"Load config: {config}")
    


@cli.command('commit')
@click.pass_context
@click.option('--style', '-s', type=click.Choice(['professional', 'imperative', 'funny'], case_sensitive=False), 
              help='The style of the git commit message.', required=True, default=lambda: load_config('./config.json').get('style', ''))
@click.option('--verbose', '-v', is_flag=True, help='Provide reasoning behind the commit message.')
@click.option('--length', '-l', type=click.IntRange(min=50, max=72), default=lambda: load_config('./config.json').get('length', ''),
              help='Specify the max length of the commit message (50 or 80 characters).')
@click.option('--branch', '-b', type=click.STRING, help='The branch name to include in the commit message.', default=lambda: load_config('./config.json').get('branch', ''))
@click.option('--diff', type=click.STRING, help='The git diff as text to analyze for generating the commit message.', default='')
@click.option('--diff_path', type=click.Path(exists=True), help='The path to a file containing the git diff.')
@click.option('--llm', type=click.Choice(['openai', 'ollama', 'claude'], case_sensitive=False), default=lambda: load_config('./config.json').get('llm', ''), help="The model you'd like to use, defaults to local install of ollama")
@click.option('--model', '-m', type=click.STRING, default=lambda: load_config('./config.json').get('model', ''), help='The model to use for the choosen llm')
def create_message(ctx, style, verbose, length, branch, diff, diff_path, llm, model):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Create diff_text to contain text from diff.
    diff_text = f""

    click.echo(f"Generating commit message with the following options:")
    click.echo(f"Style: {style}")
    click.echo(f"Max Length: {length} characters")
    click.echo(f"Verbose setting: {verbose}")
    
    if branch:
        click.echo(f"Branch: {branch}")
        
    if diff:
        click.echo(f"Diff (text): {diff}")
        # Set diff text to diff_text variable
        diff_text = diff

    if model:
        click.echo(f"Using LLM = {llm}, with model:{model}")
        
    if diff_path:
        click.echo(f"Diff (file): {diff_path}")
        # Get Diff from path location
        try:
            with open(diff_path, mode="r", encoding='utf8') as file:
                diff_text = file.read()
        except Exception as e:
            click.echo(f"Error opening file: {e}")

    if verbose:
        click.echo(f"Verbose mode enabled.")

    # Create LLM Generator
    api_key = ctx.obj['config']['claude_ai_api'] if llm == 'claude' else ctx.obj['config']['open_ai_api'] if llm == 'openai' else ''
    generator = CommentGenerator(llm, model, api_key)

    #Start Spinner
    stop_spinner = spinner()
    message = ""
    try:
        # Connect to llm to get response
        exit = False
        if not diff_text.strip():
            diff_text = subprocess.run(["git diff --staged"], check=True, capture_output=True, text=True, shell=True).stdout

        if not diff_text.strip():
            click.echo("No diff detected. Be sure you stage your files with 'git add' before running this process. Exiting...")
            exit = True
            sys.exit(999)

        if verbose:
            pass
        else:
            click.echo('Using verbose method')
            with open(os.path.join(__location__, './prompts/prompt_summary.md'), 'r') as sp:
                summary_prompt = sp.read()
                sp.close()
            with open(os.path.join(__location__, "./prompts/prompt_message.md"), 'r') as mp:
                message_prompt = mp.read()
                mp.close()
            message = generator.generate_message(diff_text, style, summary_prompt, message_prompt, length)
        

    finally:
        stop_spinner.set()
        if not exit:
            try:
                commit_changes(message)
            except Exception as e:
                click.echo(f'Task Aborted: {e}')


def commit_changes(message):
    """Commit changes using message generated"""
    
    if message != '':
        message = message.replace('"', '\\"').strip()
        
        click.echo(f"Committing with message: {message}")
        click.confirm("Do you want to commit with this message?", abort=True)
        # Run Bash Script to commit using message
        subprocess.run(["git", "commit", "-m", message], check=True)