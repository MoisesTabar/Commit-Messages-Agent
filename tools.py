import shlex
import subprocess

from langchain_core.tools import tool


@tool(description="Get the diff of the staged changes of the current branch.")
def git_diff() -> str:
    try:
        return subprocess.check_output(shlex.split("git diff --staged")).decode("utf-8")
    except subprocess.CalledProcessError as e:
        return f"Error running git diff: {e}"
