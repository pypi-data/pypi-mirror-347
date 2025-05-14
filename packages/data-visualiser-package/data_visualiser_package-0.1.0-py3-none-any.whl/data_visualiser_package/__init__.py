"""
Data Visualiser Package

A utility package for visualizing and analyzing data with Matplotlib and Seaborn.
Creates plots and statistics tables for data exploration and presentation.
"""

__version__ = "0.1.0"

from .data_visualiser import DataVisualiser, categorise_variable_in_df, uncategorise

__all__ = ["DataVisualiser", "categorise_variable_in_df", "uncategorise"]
