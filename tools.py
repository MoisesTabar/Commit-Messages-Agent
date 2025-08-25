import os
import shlex
import subprocess
import sys

from langchain_core.tools import tool


@tool(description="Get the diff of the staged changes of the current branch.")
def git_diff() -> str:
    try:
        return subprocess.check_output(shlex.split("git diff --staged")).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error running git diff: {e}"


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
