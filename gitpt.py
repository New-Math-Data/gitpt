import click
from spinner import spinner
import test_git_commit
import subprocess
import os


@click.group(invoke_without_command=True)
@click.option('--style', '-s', type=click.Choice(['professional', 'imperative', 'funny'], case_sensitive=False), 
              help='The style of the git commit message.', required=True)
@click.option('--verbose', '-v', is_flag=True, default=False, help='Provide reasoning behind the commit message.')
@click.option('--length', '-l', type=click.IntRange(min=50, max=80), default='80', 
              help='Specify the max length of the commit message (50 or 80 characters).')
@click.option('--branch', '-b', type=click.STRING, help='The branch name to include in the commit message.')
@click.option('--diff', type=click.STRING, help='The git diff as text to analyze for generating the commit message.')
@click.option('--diff_path', type=click.Path(exists=True), help='The path to a file containing the git diff.')
def create_message(verbose, length, branch, diff, diff_path, style):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Create diff_text to contain text from diff.
    diff_text = None

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
        

    #Start Spinner
    stop_spinner = spinner()

    try:
        # Connect to llm to get response
        if not diff_text:
            diff_text = subprocess.run(['./get_diffs.sh'], capture_output=True, text=True, shell=True)
        
        verbose_message = test_git_commit.generate_verbose_message(diff_text)

        if verbose:
            click.echo(f"Verbose Message: {verbose_message}")

        concise_message = test_git_commit.generate_concise_message(verbose_message, length)
        
    finally:
        stop_spinner.set()
        click.echo(concise_message)
        commit_changes(concise_message)
        click.echo('\nTask completed')


@click.confirmation_option(prompt='Are you ready to commit with this message')
def commit_changes(message):
    """Commit changes using message generated"""
    
    message = message if message != '' else os.environ['gitpt_message']
    if message != '':
        click.confirm("Do you want to commit with this message?", abort=True)
        
        # Run Bash Script to commit using message
        click.echo(f'You have commited with the following message {message}')


