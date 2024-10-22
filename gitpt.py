import click
from spinner import spinner
from test_git_commit import generate_commit_message
import time


@click.command()
@click.option('--style', '-s', type=click.Choice(['professional', 'imperative', 'funny'], case_sensitive=False), 
              help='The style of the git commit message.', required=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help='Provide reasoning behind the commit message.')
@click.option('--length', '-l', type=click.IntRange(min=50, max=80), default='80', 
              help='Specify the max length of the commit message (50 or 80 characters).')
@click.option('--branch', '-b', type=str, help='The branch name to include in the commit message.')
@click.option('--diff', type=str, help='The git diff as text to analyze for generating the commit message.')
@click.option('--diff_path', type=click.Path(exists=True), help='The path to a file containing the git diff.')
def commit(verbose, length, branch, diff, diff_path, style):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Predefined Python/bash scripts can be called here
    # For demonstration purposes, we will just print out the options
    
    click.echo(f"Generating commit message with the following options:")
    click.echo(f"Style: {style}")
    click.echo(f"Max Length: {length} characters")
    
    if branch:
        click.echo(f"Branch: {branch}")
        
    if diff:
        click.echo(f"Diff (text): {diff}")
        # Set diff text to diff_text variable
        diff_text = diff
        
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

    # Placeholder for calling the bash or Python scripts for generating the message
    # e.g., subprocess.call(["bash_script.sh", style, length, branch, diff_path])
    
    #Start Spinner
    stop_spinner = spinner()

    try:
        time.sleep(5)
    finally:
        stop_spinner.set()
        click.echo('\nTask completed')


