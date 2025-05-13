from cellpose_quantification.cli import cli, validate_args
import os
import argparse
import pytest
from unittest.mock import patch

# Test directories and files
test_image_directory = "src/tests/img"
test_mask_directory = "src/tests/mask"
test_marker_path = "src/tests/markers.csv"

@pytest.fixture
def parser():
    # A fixture that creates an argparse ojbect for validate_args function
    return argparse.ArgumentParser(description="Test parser")

def test_validate_args_success(parser):
    # Optimal path for validate_args function
    result = validate_args(
        parser,
        test_image_directory,
        test_mask_directory,
        test_marker_path,
        "log"
    )
    assert result == (
        os.path.abspath(test_image_directory),
        os.path.abspath(test_mask_directory),
        os.path.abspath(test_marker_path),
        "log"
    )

def test_validate_args_missing_image_dir(parser):
    # Test invalid img dir
    with pytest.raises(FileNotFoundError):
        validate_args(
            parser,
            "invalid_img_dir",
            test_mask_directory,
            test_marker_path,
            None
        )

def test_validate_args_missing_mask_dir(parser):
    # Test invalid mask dir
    with pytest.raises(FileNotFoundError):
        validate_args(
            parser,
            test_image_directory,
            "invalid_mask_dir",
            test_marker_path,
            None
        )

def test_validate_args_missing_marker_file(parser):
    # Test invalid marker file
    # Both SystemExit (from parser.error) and FileNotFoundError are required
    with pytest.raises((SystemExit, FileNotFoundError)):
        validate_args(
            parser,
            test_image_directory,
            test_mask_directory,
            "invalid_markers.csv",
            None
        )

def test_validate_args_invalid_normalisation(parser):
    #Test invalid normalisation method
    with pytest.raises(ValueError):
        validate_args(
            parser,
            test_image_directory,
            test_mask_directory,
            test_marker_path,
            "invalid_norm"
        )

@patch('cellpose_quantification.cli.quantification.run') # Creates a mock function to purely test CLI functionality :)
def test_cli_success(mock_run):
    #Test successful CLI execution
    test_args = [
        "cli.py",
        test_image_directory,
        test_mask_directory,
        test_marker_path,
        "--norm", "log"
    ]
    
    with patch('sys.argv', test_args):
        cli()
    
    mock_run.assert_called_once_with(
        os.path.abspath(test_image_directory),
        os.path.abspath(test_mask_directory),
        os.path.abspath(test_marker_path),
        "log"
    )

def test_cli_missing_args(capsys):
    #Test CLI with missing required arguments
    test_args = ["cli.py"]  # Missing required args
    
    with patch('sys.argv', test_args), pytest.raises(SystemExit):
        cli()
    
    captured = capsys.readouterr()
    assert "error: the following arguments are required" in captured.err

def test_cli_invalid_normalisation():
    #Test CLI with invalid normalisation
    test_args = [
        "script_name",
        test_image_directory,
        test_mask_directory,
        test_marker_path,
        "--norm", "invalid_norm"
    ]
    
    # Accepts either ValueError (from validate_args) or SystemExit (from parser)
    with patch('sys.argv', test_args), pytest.raises((ValueError, SystemExit)):
        cli()