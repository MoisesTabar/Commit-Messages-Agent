import typer


def print_patch_outcome(patch_out: str) -> None:
    if "error" in patch_out.lower():
        typer.secho(patch_out, fg=typer.colors.RED)
    else:
        typer.secho(patch_out or "Finished interactive patch.", fg=typer.colors.GREEN)


def confirm_proceed_or_exit() -> None:
    if not typer.confirm("Proceed to generate the commit message now?", default=True):
        typer.secho("Aborted by user.", fg=typer.colors.RED)
        raise typer.Exit(code=1)


def recheck_staged_or_exit(staged: str) -> str:
    if not staged:
        typer.secho("No staged changes after patch. Exiting.", fg=typer.colors.RED)
        raise typer.Exit(code=1)
    return staged
