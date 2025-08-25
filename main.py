import os

import typer
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import chat_agent_executor

from prompts import SYSTEM_PROMPT, USER_PROMPT
from tools import git_diff

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def main() -> None:
    """
    Generate a commit message for the staged changes. \n
    Must have staged changes to generate a commit message. \n
    If no staged changes are found, the agent will return an error message.
    """

    model = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0,
    )

    agent = chat_agent_executor.create_tool_calling_executor(
        model=model, tools=[git_diff]
    )

    result = agent.invoke(
        {"messages": [("system", SYSTEM_PROMPT), ("user", USER_PROMPT)]}
    )

    typer.secho(result["messages"][-1].content.strip(), fg=typer.colors.GREEN)


if __name__ == "__main__":
    typer.run(main)
