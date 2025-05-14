"""
Unit tests for the DataVisualiser package
"""
import os
import tempfile
import pandas as pd
import numpy as np
import pytest
from data_visualiser_package import DataVisualiser

@pytest.fixture
def sample_df():
    """Create a sample DataFrame for testing"""
    np.random.seed(42)
    n = 100
    
    # Generate sample data
    data = {
        'age': np.random.normal(50, 15, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'diagnosis': np.random.choice(['Healthy', 'Condition A', 'Condition B', None], n),
    }
    
    return pd.DataFrame(data)

@pytest.fixture
def temp_dirs():
    """Create temporary directories for figures and tables"""
    with tempfile.TemporaryDirectory() as figures_dir, tempfile.TemporaryDirectory() as tables_dir:
        yield figures_dir, tables_dir

def test_init():
    """Test DataVisualiser initialization"""
    dv = DataVisualiser()
    assert dv.record_unit_name == "patient"
    assert dv.count_colname == "# patients"
    
    # Test with custom record_unit_name
    dv = DataVisualiser(record_unit_name="sample")
    assert dv.record_unit_name == "sample"
    assert dv.count_colname == "# samples"

def test_get_count_plot(sample_df, temp_dirs):
    """Test get_count_plot functionality"""
    figures_dir, tables_dir = temp_dirs
    dv = DataVisualiser(figures_dirpath=figures_dir, tables_dirpath=tables_dir)
    
    # Test basic functionality
    fig, ax = dv.get_count_plot('gender', sample_df)
    assert fig is not None
    assert ax is not None
    
    # Test save functionality
    fig, ax = dv.get_count_plot('gender', sample_df, save_fig=True)
    assert os.path.exists(os.path.join(figures_dir, "count_plot_gender.png"))

def test_get_dist_plot(sample_df, temp_dirs):
    """Test get_dist_plot functionality"""
    figures_dir, tables_dir = temp_dirs
    dv = DataVisualiser(figures_dirpath=figures_dir, tables_dirpath=tables_dir)
    
    # Test basic functionality
    fig, ax = dv.get_dist_plot('age', sample_df)
    assert fig is not None
    assert ax is not None
    
    # Test save functionality
    fig, ax = dv.get_dist_plot('age', sample_df, save_fig=True)
    assert os.path.exists(os.path.join(figures_dir, "dist_plot_age.png"))

def test_get_count_stats_df(sample_df, temp_dirs):
    """Test get_count_stats_df functionality"""
    figures_dir, tables_dir = temp_dirs
    dv = DataVisualiser(figures_dirpath=figures_dir, tables_dirpath=tables_dir)
    
    # Test basic functionality
    stats_df = dv.get_count_stats_df('gender', sample_df)
    assert isinstance(stats_df, pd.DataFrame)
    assert "# patients" in stats_df.columns
    if "%" in stats_df.columns:
        assert abs(stats_df["%"].sum() - 100.0) < 0.01  # Sum should be 100%
    
    # Test save functionality
    stats_df = dv.get_count_stats_df('gender', sample_df, save_table=True)
    assert os.path.exists(os.path.join(tables_dir, "count_stats_table_gender.tex"))

def test_get_dist_stats_df(sample_df, temp_dirs):
    """Test get_dist_stats_df functionality"""
    figures_dir, tables_dir = temp_dirs
    dv = DataVisualiser(figures_dirpath=figures_dir, tables_dirpath=tables_dir)
    
    # Test basic functionality
    stats_df = dv.get_dist_stats_df('age', sample_df)
    assert isinstance(stats_df, pd.DataFrame)
    for stat in ['count', 'mean', 'std', 'min', 'max']:
        assert stat in stats_df.columns
    
    # Test save functionality
    stats_df = dv.get_dist_stats_df('age', sample_df, save_table=True)
    assert os.path.exists(os.path.join(tables_dir, "dist_stats_table_age.tex"))
