import pytest
import numpy as np
import pandas as pd
from unittest.mock import patch, MagicMock
import os
import cv2

import cellpose_quantification.quantification as cellpose_quantification

@pytest.fixture
def sample_data():
    return [1, 2, 3, 4, 5]

@pytest.fixture
def sample_image_data():
    return np.random.randint(0, 256, (3, 100, 100), dtype=np.uint16)

@pytest.fixture
def sample_mask_data():
    mask = np.zeros((100, 100), dtype=np.uint16)
    mask[10:30, 10:30] = 1  # First cell
    mask[50:70, 50:70] = 2  # Second cell
    return mask

@pytest.fixture
def sample_channel_names():
    return ["Channel1", "Channel2", "Channel3"]

def test_minmax_normalise(sample_data):
    result = cellpose_quantification.minmax_normalise(sample_data)
    expected = [0.0, 0.25, 0.5, 0.75, 1.0]
    assert result == expected
    assert min(result) == 0.0
    assert max(result) == 1.0

def test_log_normalise(sample_data):
    result = cellpose_quantification.log_normalise(np.array(sample_data))
    expected = np.log10(np.array(sample_data) + 1)
    np.testing.assert_array_almost_equal(result, expected)

def test_get_props(sample_mask_data, sample_image_data):
    # Use the first channel of the sample image data
    props = cellpose_quantification.get_props(sample_mask_data, sample_image_data[0])
    
    assert 'area' in props
    assert 'centroid-0' in props
    assert 'centroid-1' in props
    assert 'perimeter' in props
    assert len(props['area']) == 2  # Should have properties for 2 cells

def test_get_cell_features(sample_mask_data, sample_image_data, sample_channel_names):
    args = (sample_mask_data, sample_image_data, "test_file.tif", False, sample_channel_names)
    result =  cellpose_quantification.get_cell_features(args)
    
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two cells in the sample mask
    assert all(channel in result.columns for channel in sample_channel_names)
    assert "Cell_ID" in result.columns
    assert "Filename" in result.columns

def test_get_cell_features_with_normalisation(sample_mask_data, sample_image_data, sample_channel_names):
    # Test minmax normalisation
    args = (sample_mask_data, sample_image_data, "test_file.tif", "minmax", sample_channel_names)
    result_minmax = cellpose_quantification.get_cell_features(args)
    for channel in sample_channel_names:
        assert min(result_minmax[channel]) >= 0.0
        assert max(result_minmax[channel]) <= 1.0
    
    # Test log normalisation
    args = (sample_mask_data, sample_image_data, "test_file.tif", "log", sample_channel_names)
    result_log = cellpose_quantification.get_cell_features(args)
    for channel in sample_channel_names:
        assert all(result_log[channel] >= 0.0)

@patch('os.walk')
def test_process_directory(mock_walk):
    # Mock the directory structure
    mock_walk.side_effect = [
        [('/img_dir', [], ['img1.tif', 'img2.tif'])],
        [('/mask_dir', [], ['img1.tif', 'img2.png'])]]
    
    img_dict, mask_dict = cellpose_quantification.process_directory('/img_dir', '/mask_dir')
    
    assert len(img_dict) == 2
    assert len(mask_dict) == 2
    assert 'img1.tif' in img_dict
    assert 'img1.tif' in mask_dict
    assert 'img2.tif' in img_dict
    assert 'img2.png' in mask_dict

@patch('os.walk')
def test_process_directory_mismatch(mock_walk, capsys):
    # Test when image and mask counts don't match
    mock_walk.side_effect = [
        [('/img_dir', [], ['img1.tif', 'img2.tif'])],
        [('/mask_dir', [], ['img1.tif'])]]  # Only one mask
    
    with pytest.raises(SystemExit):
        cellpose_quantification.process_directory('/img_dir', '/mask_dir')
    
    captured = capsys.readouterr()
    assert "ERROR" in captured.out

def test_write_to_file(tmp_path, sample_mask_data, sample_image_data, sample_channel_names):
    # Create a sample DataFrame
    data = {
        'Cell_ID': [1, 2],
        'Channel1': [100, 200],
        'Channel2': [150, 250],
        'Filename': ['test1.tif', 'test2.tif']
    }
    df = pd.DataFrame(data)
    
    # Test without normalisation
    output_path = tmp_path / "output.csv"
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        cellpose_quantification.write_to_file(df, False)
        mock_to_csv.assert_called_once()
    
    # Test with normalisation
    with patch('pandas.DataFrame.to_csv') as mock_to_csv:
        cellpose_quantification.write_to_file(df, "minmax")
        mock_to_csv.assert_called_once()

def test_find_files(tmp_path):
    # Create test directory structure
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    
    (test_dir / "file1.tif").touch()
    (test_dir / "file2.txt").touch()
    subdir = test_dir / "subdir"
    subdir.mkdir()
    (subdir / "file3.tif").touch()
    
    results = cellpose_quantification.find_files(str(test_dir), ".tif")
    assert len(results) == 2
    assert any("file1.tif" in path for path in results)
    assert any("file3.tif" in path for path in results)