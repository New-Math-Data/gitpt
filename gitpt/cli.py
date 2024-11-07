import os
import subprocess
import sys

import click

from gitpt.generators.comments import (
    BaseCommentGenerator,
    OpenAICommentGenerator,
    ClaudeCommentGenerator,
    GeminiCommentGenerator,
)
from gitpt.utils.spinner import spinner
from gitpt.utils.config import read_toml_file


if os.path.exists("logging.conf"):
    import logging.config

    logging.config.fileConfig("logging.conf")
    log = logging.getLogger()
else:
    import logging

    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    log.addHandler(handler)

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@click.group()
@click.option(
    "--style",
    type=click.Choice(["professional", "funny", "intrinsic"], case_sensitive=False),
    default="professional",
)
@click.option(
    "--prefix",
    default=None,
    help="Optional prefix for the commit message (bugfix, feature, etc)",
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
@click.option("--google-api-key", help="API key for Google AI")
@click.pass_context
def cli(
    ctx,
    style,
    prefix,
    length,
    llm,
    model,
    verbose,
    openai_api_key,
    claude_api_key,
    google_api_key,
):
    # Load config file and store in context object
    ctx.ensure_object(dict)

    config = {
        "style": style,
        "prefix": prefix,
        "length": length,
        "llm": llm,
        "model": model,
        "verbose": verbose,
        "open_ai_api": openai_api_key,
        "claude_ai_api": claude_api_key,
        "google_ai_api": google_api_key,
    }

    toml_config = read_toml_file("tool.gitpt.config")

    log.debug(toml_config)

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
@click.option(
    "--auto-confirm",
    "-y",
    is_flag=True,
    help="Automatically confirm the commit message without prompting.",
)
def create_message(ctx, branch, diff, diff_path, auto_confirm):
    """
    CLI tool for generating meaningful git commit messages based on the provided options.
    """
    # Create diff_text to contain text from diff.
    diff_text = ""

    click.echo("Generating commit message with the following options:")
    click.echo(f"Style: {ctx.obj['config']['style']}")
    click.echo(f"Max Length: {ctx.obj['config']['length']} characters")
    click.echo(f"Verbose setting: {ctx.obj['config']['verbose']}")

    if ctx.obj["config"]["prefix"]:
        click.echo(f"Prefix: {ctx.obj['config']['prefix']}")

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
                else ""
            )
        )
    )
    if ctx.obj["config"]["llm"] == "claude":
        generator = ClaudeCommentGenerator(ctx.obj["config"]["model"], api_key)
    elif ctx.obj["config"]["llm"] == "openai":
        generator = OpenAICommentGenerator(ctx.obj["config"]["model"], api_key)
    elif ctx.obj["config"]["llm"] == "google":
        generator = GeminiCommentGenerator(ctx.obj["config"]["model"], api_key)
    else:
        generator = BaseCommentGenerator(ctx.obj["config"]["model"])

    # generator = CommentGenerator(
    #     ctx.obj["config"]["llm"],
    #     ctx.obj["config"]["model"],
    #     api_key,
    # )

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

        if ctx.obj["config"]["verbose"]:
            pass
        else:
            click.echo("Using verbose method")
            with open(
                os.path.join(__location__, "./prompts/prompt_summary.md"), "r"
            ) as sp:
                summary_prompt = sp.read()
                sp.close()
            if ctx.obj["config"]["prefix"]:
                with open(
                    os.path.join(__location__, "./prompts/prompt_message_no_prefix.md"), "r"
                ) as mp:
                    message_prompt = mp.read()
                    mp.close()
            else:
                with open(
                    os.path.join(__location__, "./prompts/prompt_message.md"), "r"
                ) as mp:
                    message_prompt = mp.read()
                    mp.close()
            message = generator.generate_message(
                diff_text,
                ctx.obj["config"]["style"],
                summary_prompt,
                message_prompt,
                ctx.obj["config"]["length"],
            )

    finally:
        stop_spinner.set()
        if not exit:
            try:
                commit_changes(ctx,message, auto_confirm=auto_confirm)
            except Exception as e:
                click.echo(f"Task Aborted: {e}")


def commit_changes(ctx,message, auto_confirm=False):
    """Commit changes using message generated"""

    if message != "":
        message = message.replace('"', '\\"').strip()
        if ctx.obj["config"]["prefix"]:
            message = f"{ctx.obj["config"]["prefix"]}:{message}"

        click.echo(f"Committing with message: {message}")
        if not auto_confirm:
            click.confirm("Do you want to commit with this message?", abort=True)
        # Run Bash Script to commit using message
        subprocess.run(["git", "commit", "-m", message], check=True)


def main():
    cli(auto_envvar_prefix="GITPT_")
