import os
import shlex
import subprocess
import sys

import typer

from utils.cli import (
    confirm_proceed_or_exit,
    print_patch_outcome,
    recheck_staged_or_exit,
)


def git_add_patch() -> str:
    """
    Runs `git add --patch` interactively to stage changes.

    Uses environment variables `GIT_PAGER=cat` and `LESS=-F -X` to avoid pagers
    and ensure smooth interactive behavior. Inherits `stdin`, `stdout`, and `stderr`
    for interactive patching.

    Returns success message or error string on failure from subprocess.
    """
    try:
        env = {**os.environ, "GIT_PAGER": "cat", "LESS": "-F -X"}
        subprocess.run(
            shlex.split("git add --patch"),
            check=True,
            stdin=sys.stdin,
            stdout=sys.stdout,
            stderr=sys.stderr,
            env=env,
        )
        return "Staged changes successfully."
    except subprocess.CalledProcessError as e:
        return f"Error running git add: {e}"


def ensure_tty_or_autostage() -> str:
    """
    Ensure we can run an interactive patch; otherwise offer to stage all changes.
    Returns a status string from the staging operation.
    """
    if not (sys.stdin.isatty() and sys.stdout.isatty()):
        if typer.confirm(
            "Interactive mode not available. Stage ALL changes automatically?",
            default=False,
        ):
            try:
                subprocess.run(["git", "add", "-A"], check=True)
                return "Staged all changes successfully."
            except subprocess.CalledProcessError as e:
                return f"Error running git add -A: {e}"
        else:
            typer.secho(
                """
                Interactive staging not possible here.
                Please run 'git add -p' in a terminal and retry.
                """,
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)
    else:
        typer.echo("Launching interactive patch (git add -p)...", nl=True)
        return git_add_patch().strip()


def ensure_staged(staged: str) -> str:
    """Ensure there are staged changes, prompting the user to stage if necessary."""
    if staged:
        return staged

    typer.secho("No staged changes found.", fg=typer.colors.RED)

    if not typer.confirm(
        "Do you want to interactively stage changes now?", default=True
    ):
        raise typer.Exit(code=1)

    patch_out = ensure_tty_or_autostage()
    print_patch_outcome(patch_out)
    confirm_proceed_or_exit()
    return recheck_staged_or_exit(patch_out)
