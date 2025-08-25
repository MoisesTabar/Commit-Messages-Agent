import subprocess
from unittest.mock import patch

from utils.git import ensure_staged, ensure_tty_or_autostage, git_add_patch


@patch("subprocess.run")
def test_git_add_patch_success(mock_run):
    mock_run.return_value.returncode = 0

    result = git_add_patch()

    assert result == "Staged changes successfully."
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0] == ["git", "add", "--patch"]
    assert mock_run.call_args[1]["check"] is True


@patch("subprocess.run")
def test_git_add_patch_error(mock_run):
    mock_run.side_effect = subprocess.CalledProcessError(1, "git add --patch")

    result = git_add_patch()

    assert "Error running git add:" in result


@patch("utils.git.git_add_patch")
@patch("sys.stdin.isatty", return_value=True)
@patch("sys.stdout.isatty", return_value=True)
def test_ensure_tty_or_autostage_interactive(mock_stdout, mock_stdin, mock_git_add):
    mock_git_add.return_value = "Staged changes successfully."

    result = ensure_tty_or_autostage()

    assert result == "Staged changes successfully."
    mock_git_add.assert_called_once()


@patch("subprocess.run")
@patch("sys.stdin.isatty", return_value=False)
@patch("typer.confirm", return_value=True)
def test_ensure_tty_or_autostage_non_interactive(mock_confirm, mock_stdin, mock_run):
    mock_run.return_value.returncode = 0

    result = ensure_tty_or_autostage()

    assert result == "Staged all changes successfully."
    mock_confirm.assert_called_once_with(
        "Interactive mode not available. Stage ALL changes automatically?",
        default=False,
    )
    mock_run.assert_called_once_with(["git", "add", "-A"], check=True)


@patch("typer.secho")
@patch("typer.Exit")
@patch("typer.confirm")
@patch("utils.git.ensure_tty_or_autostage")
@patch("utils.cli.print_patch_outcome")
@patch("utils.cli.confirm_proceed_or_exit")
@patch("utils.cli.recheck_staged_or_exit")
def test_ensure_staged_user_declines_staging(
    mock_recheck,
    mock_confirm_proceed,
    mock_print_outcome,
    mock_ensure_tty,
    mock_confirm,
    mock_exit,
    mock_secho,
):
    mock_confirm.return_value = False
    mock_exit.side_effect = SystemExit(1)

    try:
        ensure_staged("")
        assert False, "Expected SystemExit"
    except SystemExit:
        pass

    mock_secho.assert_called_once_with("No staged changes found.", fg="red")
    mock_confirm.assert_called_once_with(
        "Do you want to interactively stage changes now?", default=True
    )
    mock_ensure_tty.assert_not_called()
    mock_print_outcome.assert_not_called()
    mock_confirm_proceed.assert_not_called()
    mock_recheck.assert_not_called()


def test_ensure_staged_already_staged():
    result = ensure_staged("already staged changes")

    assert result == "already staged changes"
