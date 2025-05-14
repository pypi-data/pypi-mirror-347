import sys
from unittest.mock import patch, MagicMock
import pytest

from pytreefind.tree import main

def test_main_with_valid_args():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock()  # Mock successful run

        test_args = ["pytreefind", "--level", "2", "/some/directory"]
        with patch.object(sys, "argv", test_args):
            main()

        mock_run.assert_called_once_with([
            "tree",
            "-P", "*.py",
            "-I", "__pycache__|env|venv|.git|node_modules|.pytest_cache|*.egg-info",
            "-L", "2",
            "-a", "/some/directory"
        ], check=True)

def test_main_with_default_args():
    with patch("subprocess.run") as mock_run:
        mock_run.return_value = MagicMock()  # Mock successful run

        test_args = ["pytreefind"]
        with patch.object(sys, "argv", test_args):
            main()

        mock_run.assert_called_once_with([
            "tree",
            "-P", "*.py",
            "-I", "__pycache__|env|venv|.git|node_modules|.pytest_cache|*.egg-info",
            "-L", "3",  # default level
            "-a", "."
        ], check=True)

def test_main_tree_not_found(capsys):
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = FileNotFoundError

        test_args = ["pytreefind", "--level", "2", "/some/directory"]
        with patch.object(sys, "argv", test_args):
            with pytest.raises(SystemExit): 
                main()

    captured = capsys.readouterr()
    assert "Error: 'tree' command not found" in captured.out