import click
from spinner import spinner
from llm_helper import CommentGenerator
import subprocess
import os
import sys

@click.group(invoke_without_command=True)
@click.option('--style', '-s', type=click.Choice(['professional', 'imperative', 'funny'], case_sensitive=False), 
              help='The style of the git commit message.', required=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help='Provide reasoning behind the commit message.')
@click.option('--length', '-l', type=click.IntRange(min=50, max=80), default='80', 
              help='Specify the max length of the commit message (50 or 80 characters).')
@click.option('--branch', '-b', type=click.STRING, help='The branch name to include in the commit message.')
@click.option('--diff', type=click.STRING, help='The git diff as text to analyze for generating the commit message.')
@click.option('--diff_path', type=click.Path(exists=True), help='The path to a file containing the git diff.')
@click.option('--model', '-m', type=click.Choice(['chat-gpt', 'ollama'], case_sensitive=False), help="The model you'd like to use, defaults to local install of ollama", multiple=True, default=["ollama"])
def create_message(verbose, length, branch, diff, diff_path, style, model):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Create diff_text to contain text from diff.
    diff_text = None

    # Create Generator
    generator = CommentGenerator(model[0])

    click.echo(f"Generating commit message with the following options:")
    click.echo(f"Style: {style}")
    click.echo(f"Max Length: {length} characters")
    
    if branch:
        click.echo(f"Branch: {branch}")
        
    if diff:
        click.echo(f"Diff (text): {diff}")
        # Set diff text to diff_text variable
        diff_text = diff

    if model:
        click.echo(f"Using Model = {model[0]}")
        
    if diff_path:
        click.echo(f"Diff (file): {diff_path}")
        # Get Diff from path location
        try:
            with open(diff_path, mode="r", encoding='utf8') as file:
                diff_text = file.read()
        except Exception as e:
            click.echo(f"Error opening file: {e}")

    # You can add logic here to pass these options to your scripts
    if verbose:
        click.echo(f"\nVerbose mode enabled.")

    # Get prompts
    with open('./prompts/prompt_txt.md', 'r') as prompt:
        prompt_txt = prompt.read()
        prompt.close()

    with open('./prompts/small_prompt.md', 'r') as sp:
        short_prompt = sp.read()
        sp.close()

       

    #Start Spinner
    stop_spinner = spinner()

    try:
        # Connect to llm to get response
        if not diff_text:
            diff_text = subprocess.run(['./get_diffs.sh'], capture_output=True, text=True, shell=True)
            
            click.echo(f"Diff Text: {diff_text}")

        if not diff_text:
            click.echo("No diff detected. Exiting...")
            sys.exit(999)

        verbose_message = generator.generate_verbose_message(diff_text, style, prompt_txt)

        if verbose:
            click.echo(f"Verbose Message: {verbose_message}")

        concise_message = generator.generate_short_message(verbose_message, length, short_prompt, style)
        
        click.echo(concise_message)
        commit_changes(concise_message, verbose_message)
        click.echo('\nTask completed')

    finally:
        stop_spinner.set()


@click.confirmation_option(prompt='Are you ready to commit with this message?')
def commit_changes(message, v_message):
    """Commit changes using message generated"""
    
    message = message if message != '' else os.environ['gitpt_message']
    if message != '':
        click.confirm("Do you want to commit with this message?", abort=True)
        
        # Run Bash Script to commit using message
        subprocess.run(["./commit.sh", message, v_message], text=True, shell=True)
        click.echo(f'Changes commited with message: {message}')


