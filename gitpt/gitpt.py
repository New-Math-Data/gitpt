import click
import os
import subprocess
import sys
from gitpt.utils.spinner import spinner
from gitpt.utils.llm_helper import CommentGenerator

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@click.group()
@click.option(
    "--style",
    type=click.Choice(["professional", "funny", "intrinsic"], case_sensitive=False),
    default="professional",
)
@click.option(
    "--length",
    type=click.IntRange(min=50, max=72),
    default=72,
)
@click.option(
    "--llm",
    type=click.Choice(["ollama", "openai", "claude", "google"]),
    default="ollama",
    help="LLM to use, (OpenAI, Ollama, Claude)",
)
@click.option(
    "--model",
    default="gemma2",
    help="LLM model to use (gemma2 for Ollama, gpt-4o for OpenAI, etc)",
)
@click.option("--verbose", default=False)
@click.option(
    "--openai-api-key",
    help="API key for OpenAI account",
)
@click.option(
    "--claude-api-key",
    help="API key for Claude AI",
)
@click.option(
    "--google-api-key",
    help="API key for Google AI"
)
@click.pass_context
def cli(ctx, style, length, llm, model, verbose, openai_api_key, claude_api_key, google_api_key):
    # Load config file and store in context object
    ctx.ensure_object(dict)

    config = {
        "style": style,
        "length": length,
        "llm": llm,
        "model": model,
        "verbose": verbose,
        "open_ai_api": openai_api_key,
        "claude_ai_api": claude_api_key,
        "google_ai_api": google_api_key
    }

    ctx.obj["config"] = config
    pass
    # ctx.obj["config"] = load_config(config_file)


@cli.command("commit")
@click.pass_context
@click.option(
    "--branch",
    "-b",
    type=click.STRING,
    help="The branch name to include in the commit message.",
    default=None,
)
@click.option(
    "--diff",
    type=click.STRING,
    help="The git diff as text to analyze for generating the commit message.",
    default=None,
)
@click.option(
    "--diff-path",
    type=click.Path(exists=True),
    help="The path to a file containing the git diff.",
)
def create_message(ctx, branch, diff, diff_path):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Create diff_text to contain text from diff.
    diff_text = ""

    click.echo("Generating commit message with the following options:")
    click.echo(f"Style: {ctx.obj['config']['style']}")
    click.echo(f"Max Length: {ctx.obj['config']['length']} characters")
    click.echo(f"Verbose setting: {ctx.obj['config']['verbose']}")

    if branch:
        click.echo(f"Branch: {branch}")

    if diff:
        click.echo(f"Diff (text): {diff}")
        # Set diff text to diff_text variable
        diff_text = diff

    if ctx.obj["config"]["model"]:
        click.echo(
            f"Using LLM = {ctx.obj['config']['llm']}, with model:{ctx.obj['config']['model']}"
        )

    if diff_path:
        click.echo(f"Diff (file): {diff_path}")
        # Get Diff from path location
        try:
            with open(diff_path, mode="r", encoding="utf8") as file:
                diff_text = file.read()
        except Exception as e:
            click.echo(f"Error opening file: {e}")

    if ctx.obj["config"]["verbose"]:
        click.echo("Verbose mode enabled.")

    # Create LLM Generator
    api_key = (
        ctx.obj["config"]["claude_ai_api"]
        if ctx.obj["config"]["llm"] == "claude"
        else (
            ctx.obj["config"]["open_ai_api"]
            if ctx.obj["config"]["llm"] == "openai"
        else (
            ctx.obj["config"]["google_ai_api"]
            if ctx.obj["config"]["llm"] == "google"
        else
        ""
        ))
    )
    generator = CommentGenerator(
        ctx.obj["config"]["llm"],
        ctx.obj["config"]["model"],
        api_key,
    )

    # Start Spinner
    stop_spinner = spinner()
    message = ""
    try:
        # Connect to llm to get response
        exit = False
        if not diff_text.strip():
            diff_text = subprocess.run(
                ["git diff --staged"],
                check=True,
                capture_output=True,
                text=True,
                shell=True,
            ).stdout

        if not diff_text.strip():
            click.echo(
                "No diff detected. Be sure you stage your files with 'git add' before running this process. Exiting..."
            )
            exit = True
            sys.exit(999)
        message = generator.generate_verbose_message(diff_text, style, prompt_txt)
        if verbose:
            click.echo(f"Verbose Message: {message}")
        else:
            message = generator.generate_short_message(
                message, length, short_prompt, style
            )

    finally:
        stop_spinner.set()
        if not exit:
            try:
                commit_changes(message)
            except Exception as e:
                click.echo(f"Task Aborted: {e}")


def commit_changes(message):
    """Commit changes using message generated"""

    if message != "":
        message = message.replace('"', '\\"').strip()

        click.echo(f"Committing with message: {message}")
        click.confirm("Do you want to commit with this message?", abort=True)
        # Run Bash Script to commit using message
        subprocess.run(["git", "commit", "-m", message], check=True)


def main():
    cli(auto_envvar_prefix="GITPT_")
