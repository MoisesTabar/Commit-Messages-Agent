import subprocess
from unittest.mock import patch

from tools import git_diff


def test_git_diff_returns_string_on_success():
    diff_text = "diff --git a/x b/x\n+added"
    with patch(
        "tools.subprocess.check_output", return_value=diff_text.encode("utf-8")
    ) as mock_co:
        result = git_diff.func()

    assert result == diff_text
    mock_co.assert_called_once_with(["git", "diff", "--staged"])


def test_git_diff_handles_subprocess_error():
    with patch(
        "tools.subprocess.check_output",
        side_effect=subprocess.CalledProcessError(1, ["git", "diff", "--staged"]),
    ):
        result = git_diff.func()

    assert "Error running git diff:" in result
