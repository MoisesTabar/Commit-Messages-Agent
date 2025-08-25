from unittest.mock import patch

import pytest
from typer import Exit

from utils.cli import (
    confirm_proceed_or_exit,
    print_patch_outcome,
    recheck_staged_or_exit,
)


def test_print_patch_outcome_success(capsys):
    print_patch_outcome("Success message")
    captured = capsys.readouterr()
    assert "Success message" in captured.out


def test_print_patch_outcome_error(capsys):
    print_patch_outcome("Error message")
    captured = capsys.readouterr()
    assert "Error message" in captured.out


def test_confirm_proceed_or_exit_confirmed():
    with patch("typer.confirm", return_value=True):
        confirm_proceed_or_exit()


def test_confirm_proceed_or_exit_cancelled():
    with (
        patch("typer.confirm", return_value=False),
        patch("typer.secho") as mock_secho,
        pytest.raises(Exit) as exc_info,
    ):
        confirm_proceed_or_exit()

    assert exc_info.value.exit_code == 1
    mock_secho.assert_called_with("Aborted by user.", fg="red")


def test_recheck_staged_or_exit_with_staged():
    result = recheck_staged_or_exit("staged changes")
    assert result == "staged changes"


def test_recheck_staged_or_exit_without_staged():
    with patch("typer.secho") as mock_secho, pytest.raises(Exit) as exc_info:
        recheck_staged_or_exit("")

    assert exc_info.value.exit_code == 1
    mock_secho.assert_called_with("No staged changes after patch. Exiting.", fg="red")
