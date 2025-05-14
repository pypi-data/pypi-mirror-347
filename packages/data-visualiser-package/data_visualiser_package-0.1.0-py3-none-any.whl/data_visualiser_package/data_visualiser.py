"""
Data Visualiser Package

A utility package for visualizing and analyzing data with Matplotlib and Seaborn.
Creates plots and statistics tables for data exploration and presentation.

Quick import example:
```python
from data_visualiser_package import DataVisualiser
dv = DataVisualiser()


```
"""
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from .export_latex_tables import get_latex_table_bold_col_header, get_n_decimals_to_include

# Constants
RECORD_UNIT_NAME = "patient"  # What a single record represents (e.g., patient in clinical data)
NAN_REPLACEMENT_STR = "NaN"   # String to use when replacing NaN values for display
HEIGHT = 4                    # Default plot height in inches


def uncategorise(col: pd.Series) -> pd.Series:
    """
    Convert categorical columns back to their original data types.
    
    Args:
        col: The pandas Series to convert
        
    Returns:
        The uncategorized pandas Series
    """
    if col.dtype.name == "category":
        try:
            return col.astype(col.cat.categories.dtype)
        except:
            # In case there is pd.NA (pandas >= 1.0), Int64 should be used instead of int64
            return col.astype(col.cat.categories.dtype.name.title())
    else:
        return col


def categorise_variable_in_df(
    var: str, 
    df: pd.DataFrame, 
    forced_order: Optional[List[str]] = None, 
    nan_replacement_str: str = NAN_REPLACEMENT_STR
) -> None:
    """
    Categorize a variable in a DataFrame, handling NaN values and custom ordering.
    
    Args:
        var: Variable name to categorize
        df: DataFrame containing the variable
        forced_order: Optional custom ordering of categories
        nan_replacement_str: String used to replace NaN values
        
    Note:
        This function modifies the DataFrame in-place.
    """
    if (df[var] == nan_replacement_str).any():
        if forced_order is not None:
            assert (set(df[var]) - {nan_replacement_str}).issubset(
                forced_order
            ), f"forced_order for var {var} is incomplete: {(set(df[var]) - set([nan_replacement_str])) - set(forced_order)}"
            categories = forced_order + [nan_replacement_str]
        else:
            categories = sorted(set(df[var].unique()) - {nan_replacement_str}) + [
                nan_replacement_str
            ]
    else:
        if forced_order is not None:
            assert (set(df[var]) - {np.nan}).issubset(
                forced_order
            ), f"forced_order for var {var} is incomplete: {(set(df[var]) - set([np.nan])) - set(forced_order)}"
            categories = forced_order
        else:
            categories = sorted(set(df[var]) - {np.nan})

    df[var] = pd.Categorical(df[var], categories=categories)


class DataVisualiser:
    """
    A class for creating and saving data visualizations and statistics tables.
    
    This class provides methods to generate common statistical visualizations and tables,
    including count plots, distribution plots, and their stratified versions.
    
    Attributes:
        record_unit_name: Name of what a single record represents (e.g., "patient")
        count_colname: Column name used for count statistics
        figures_dirpath: Directory path for saving figures
        tables_dirpath: Directory path for saving tables
    """
    
    def __init__(
        self,
        record_unit_name: str = RECORD_UNIT_NAME,
        figures_dirpath: Optional[str] = None,
        tables_dirpath: Optional[str] = None,
        create_dirs: bool = False,
    ):
        """
        Initialize DataVisualiser with paths and record unit information.
        
        Args:
            record_unit_name: Name of what a single record represents (e.g., "patient")
            figures_dirpath: Directory path for saving figures
            tables_dirpath: Directory path for saving tables
            create_dirs: Whether to create the figures and tables directories if they don't exist
        """
        self.record_unit_name = record_unit_name
        self.count_colname = f"# {record_unit_name}s"
        self.figures_dirpath = figures_dirpath
        self.tables_dirpath = tables_dirpath

        if create_dirs and figures_dirpath and tables_dirpath:
            Path(figures_dirpath).mkdir(parents=True, exist_ok=True)
            Path(tables_dirpath).mkdir(parents=True, exist_ok=True)

    def get_count_plot(
        self,
        var: str,
        df: pd.DataFrame,
        show_nan: bool = True,
        save_fig: bool = False,
        plot_kwargs: Dict = {},
        xlabels_rotation: Optional[int] = None,
        forced_order: Optional[List[str]] = None,
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a count plot for a categorical variable.
        
        Args:
            var: Variable to plot
            df: DataFrame containing the data
            show_nan: Whether to show NaN values as a separate category
            save_fig: Whether to save the figure to disk
            plot_kwargs: Additional keyword arguments to pass to seaborn's countplot
            xlabels_rotation: Rotation angle for x-axis labels
            forced_order: Optional custom ordering of categories
            
        Returns:
            Tuple of (figure, axes)
        """
        # Preprocess df
        df = df[var].astype(str).to_frame().copy()
        if show_nan:
            df = df[var].fillna(NAN_REPLACEMENT_STR).to_frame().copy()
        # Order variables alphabetically
        categorise_variable_in_df(var, df, forced_order=forced_order)

        fig, ax = plt.subplots()
        sns.countplot(y=var, data=df, **plot_kwargs)
        ax.set_title(f"Number of {self.record_unit_name}s separated by {var}")

        if xlabels_rotation:
            plt.xticks(rotation=xlabels_rotation)

        if save_fig and self.figures_dirpath:
            plt.savefig(
                os.path.join(self.figures_dirpath, f"count_plot_{var}.png"),
                bbox_inches="tight",
            )
            plt.close()

        return fig, ax

    def get_count_stratified_plot(
        self,
        var: str,
        df: pd.DataFrame,
        col: str = "sexe_desc",
        show_nan: bool = True,
        show_nan_col: bool = True,
        save_fig: bool = False,
        col_wrap: int = 3,
        plot_kwargs: Dict = {},
        xlabels_rotation: Optional[int] = None,
        forced_order: Optional[List[str]] = None,
        forced_order_col: Optional[List[str]] = None,
    ) -> sns.FacetGrid:
        """
        Create stratified count plots for a categorical variable.
        
        Args:
            var: Variable to plot
            df: DataFrame containing the data
            col: Column to stratify by
            show_nan: Whether to show NaN values in var as a separate category
            show_nan_col: Whether to show NaN values in col as a separate category
            save_fig: Whether to save the figure to disk
            col_wrap: Number of facets per row
            plot_kwargs: Additional keyword arguments to pass to seaborn's catplot
            xlabels_rotation: Rotation angle for x-axis labels
            forced_order: Optional custom ordering of categories for var
            forced_order_col: Optional custom ordering of categories for col
            
        Returns:
            Seaborn FacetGrid object
        """
        # Preprocess df
        df = df[[var, col]].astype(str).copy()
        if show_nan:
            df[var] = df[var].fillna(NAN_REPLACEMENT_STR)
        if show_nan_col:
            df[col] = df[col].fillna(NAN_REPLACEMENT_STR)
        # Order variables alphabetically
        categorise_variable_in_df(var, df, forced_order=forced_order)
        categorise_variable_in_df(col, df, forced_order=forced_order_col)

        # Use height from plot_kwargs if specified, otherwise use HEIGHT
        if plot_kwargs.get("height") is None:
            plot_kwargs["height"] = HEIGHT

        fg = sns.catplot(
            y=var, col=col, col_wrap=col_wrap, kind="count", data=df, **plot_kwargs
        )
        fg.fig.suptitle(
            f"Number of {self.record_unit_name}s separated by {var} in each {col}",
            y=1.02,
        )

        if xlabels_rotation:
            fg.tick_params(axis="x", rotation=xlabels_rotation)

        if save_fig and self.figures_dirpath:
            plt.savefig(
                os.path.join(
                    self.figures_dirpath, f"count_plot_{var}_for_each_{col}.png"
                ),
                bbox_inches="tight",
            )
            plt.close()

        return fg

    def get_count_stats_df(
        self,
        var: str,
        df: pd.DataFrame,
        show_nan: bool = True,
        save_table: bool = False,
        percentage: bool = True,
        add_total: bool = False,
        round_n_digits: int = 1,
        forced_order: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Create a DataFrame with count statistics for a categorical variable.
        
        Args:
            var: Variable to analyze
            df: DataFrame containing the data
            show_nan: Whether to include NaN values as a separate category
            save_table: Whether to save the statistics as a LaTeX table
            percentage: Whether to include percentage column
            add_total: Whether to add a "Total" row
            round_n_digits: Number of decimal places to round to
            forced_order: Optional custom ordering of categories
            
        Returns:
            DataFrame with count statistics
        """
        # Preprocess df
        df = df[var].astype(str).to_frame().copy()
        if show_nan:
            df = df[var].fillna(NAN_REPLACEMENT_STR).to_frame().copy()
        # Order variables alphabetically
        categorise_variable_in_df(var, df, forced_order=forced_order)

        # Compute stats df
        stats_df = df.groupby(var).size().rename(self.count_colname).to_frame()

        if percentage:
            stats_df = pd.concat(
                [
                    stats_df,
                    (100 * stats_df / stats_df.sum()).rename(
                        columns={self.count_colname: "%"}
                    ),
                ],
                axis=1,
            )

        if add_total:
            stats_df = pd.concat(
                [
                    stats_df,
                    stats_df.sum(axis=0).rename("Total").to_frame().transpose(),
                ],
                axis=0,
            )
            # Convert count_colname back to int type
            stats_df[self.count_colname] = stats_df[self.count_colname].astype(int)

        if save_table and self.tables_dirpath:
            filepath = os.path.join(self.tables_dirpath, f"count_stats_table_{var}.tex")
            with open(filepath, "w") as f:
                f.write(stats_df.round(round_n_digits).to_latex())

        return stats_df

    def get_count_stratified_stats_df(
        self,
        var: str,
        df: pd.DataFrame,
        col: str = "sexe_desc",
        show_nan: bool = True,
        show_nan_col: bool = True,
        save_table: bool = False,
        percentage: bool = True,
        round_n_digits: int = 1,
        forced_order: Optional[List[str]] = None,
        forced_order_col: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Create a DataFrame with stratified count statistics for a categorical variable.
        
        Args:
            var: Variable to analyze
            df: DataFrame containing the data
            col: Column to stratify by
            show_nan: Whether to include NaN values in var as a separate category
            show_nan_col: Whether to include NaN values in col as a separate category
            save_table: Whether to save the statistics as a LaTeX table
            percentage: Whether to include percentage column
            round_n_digits: Number of decimal places to round to
            forced_order: Optional custom ordering of categories for var
            forced_order_col: Optional custom ordering of categories for col
            
        Returns:
            DataFrame with stratified count statistics
        """
        # Preprocess df
        df = df[[var, col]].astype(str).copy()
        if show_nan:
            df[var] = df[var].fillna(NAN_REPLACEMENT_STR)
        if show_nan_col:
            df[col] = df[col].fillna(NAN_REPLACEMENT_STR)
        # Order variables alphabetically
        categorise_variable_in_df(var, df, forced_order=forced_order)
        categorise_variable_in_df(col, df, forced_order=forced_order_col)

        # Compute stats df
        stratified_stats_df = pd.DataFrame(
            df.groupby([col, var]).size(), columns=[self.count_colname]
        )

        if percentage:
            stratified_stats_df = pd.concat(
                [
                    stratified_stats_df,
                    (
                        100
                        * stratified_stats_df
                        / stratified_stats_df.groupby(level=0).sum()
                    ).rename(columns={self.count_colname: "%"}),
                ],
                axis=1,
            )

        if save_table and self.tables_dirpath:
            filepath = os.path.join(
                self.tables_dirpath,
                f"count_stats_table_{var}_for_each_{col}.tex",
            )
            with open(filepath, "w") as f:
                f.write(stratified_stats_df.round(round_n_digits).to_latex())

        return stratified_stats_df

    def get_dist_plot(
        self, 
        var: str, 
        df: pd.DataFrame, 
        save_fig: bool = False, 
        plot_kwargs: Dict = {"kde": True}, 
        xlabels_rotation: Optional[int] = None
    ) -> Tuple[plt.Figure, plt.Axes]:
        """
        Create a distribution plot for a numerical variable.
        
        Args:
            var: Variable to plot
            df: DataFrame containing the data
            save_fig: Whether to save the figure to disk
            plot_kwargs: Additional keyword arguments to pass to seaborn's histplot
            xlabels_rotation: Rotation angle for x-axis labels
            
        Returns:
            Tuple of (figure, axes)
        """
        fig, ax = plt.subplots()
        sns.histplot(data=df, x=var, ax=ax, **plot_kwargs)
        ax.set_title(f"Distribution of {var}")

        if xlabels_rotation:
            plt.xticks(rotation=xlabels_rotation)

        if save_fig and self.figures_dirpath:
            plt.savefig(
                os.path.join(self.figures_dirpath, f"dist_plot_{var}.png"),
                bbox_inches="tight",
            )
            plt.close()

        return fig, ax

    def get_dist_stratified_plot(
        self,
        var: str,
        df: pd.DataFrame,
        col: str = "sexe_desc",
        show_nan_col: bool = True,
        save_fig: bool = False,
        col_wrap: int = 3,
        plot_kwargs: Dict = {"kde": True},
        xlabels_rotation: Optional[int] = None,
        forced_order_col: Optional[List[str]] = None,
    ) -> sns.FacetGrid:
        """
        Create stratified distribution plots for a numerical variable.
        
        Args:
            var: Variable to plot
            df: DataFrame containing the data
            col: Column to stratify by
            show_nan_col: Whether to show NaN values in col as a separate category
            save_fig: Whether to save the figure to disk
            col_wrap: Number of facets per row
            plot_kwargs: Additional keyword arguments to pass to seaborn's displot
            xlabels_rotation: Rotation angle for x-axis labels
            forced_order_col: Optional custom ordering of categories for col
            
        Returns:
            Seaborn FacetGrid object
        """
        # Preprocess df
        df = df[[var, col]].copy()
        df[col] = df[col].astype(str)
        if show_nan_col:
            df[col] = df[col].fillna(NAN_REPLACEMENT_STR)
        # Order variables alphabetically
        categorise_variable_in_df(col, df, forced_order=forced_order_col)

        # Use height from plot_kwargs if specified, otherwise use HEIGHT
        if plot_kwargs.get("height") is None:
            plot_kwargs["height"] = HEIGHT

        fg = sns.displot(data=df, x=var, col=col, col_wrap=col_wrap, **plot_kwargs)
        fg.fig.suptitle(f"Distribution of {var} for each {col}", y=1.02)

        if xlabels_rotation:
            fg.set_xticklabels(rotation=xlabels_rotation)

        if save_fig and self.figures_dirpath:
            plt.savefig(
                os.path.join(
                    self.figures_dirpath, f"dist_plot_{var}_for_each_{col}.png"
                ),
                bbox_inches="tight",
            )
            plt.close()

        return fg

    def get_dist_hued_plot(
        self,
        var: str,
        df: pd.DataFrame,
        hue: str = "sexe_desc",
        show_nan_col: bool = True,
        save_fig: bool = False,
        plot_kwargs: Dict = {"kde": True},
        xlabels_rotation: Optional[int] = None,
        forced_order_col: Optional[List[str]] = None,
    ) -> sns.FacetGrid:
        """
        Create a distribution plot for a numerical variable with hue for categories.
        
        Args:
            var: Variable to plot
            df: DataFrame containing the data
            hue: Column to use for color encoding
            show_nan_col: Whether to show NaN values in hue as a separate category
            save_fig: Whether to save the figure to disk
            plot_kwargs: Additional keyword arguments to pass to seaborn's displot
            xlabels_rotation: Rotation angle for x-axis labels
            forced_order_col: Optional custom ordering of categories for hue
            
        Returns:
            Seaborn FacetGrid object
        """
        # Preprocess df
        df = df[[var, hue]].copy()
        df[hue] = df[hue].astype(str)
        if show_nan_col:
            df[hue] = df[hue].fillna(NAN_REPLACEMENT_STR)
        # Order variables alphabetically
        categorise_variable_in_df(hue, df, forced_order=forced_order_col)

        # Use height from plot_kwargs if specified, otherwise use HEIGHT
        if plot_kwargs.get("height") is None:
            plot_kwargs["height"] = HEIGHT

        fg = sns.displot(data=df, x=var, hue=hue, **plot_kwargs)
        fg.fig.suptitle(f"Distribution of {var} for each {hue}", y=1.02)

        if xlabels_rotation:
            fg.set_xticklabels(rotation=xlabels_rotation)

        if save_fig and self.figures_dirpath:
            plt.savefig(
                os.path.join(
                    self.figures_dirpath, f"dist_plot_{var}_for_hue_{hue}.png"
                ),
                bbox_inches="tight",
            )
            plt.close()

        return fg

    def get_dist_stats_df(
        self,
        var: str,
        df: pd.DataFrame,
        save_table: bool = False
    ) -> pd.DataFrame:
        """
        Create a DataFrame with distribution statistics for a numerical variable.
        
        Args:
            var: Variable to analyze
            df: DataFrame containing the data
            save_table: Whether to save the statistics as a LaTeX table
            
        Returns:
            DataFrame with distribution statistics
        """
        stats_df = pd.DataFrame(df[var].describe()).transpose()

        # Convert 'count' column into 'int' type
        stats_df["count"] = stats_df["count"].astype(int)

        # Add number and percentage of NaNs
        stats_df.insert(1, "nan_perc", value=100 * df[var].isna().mean())
        stats_df.insert(1, "n_nan", value=df[var].isna().sum())

        if save_table and self.tables_dirpath:
            # Get number of decimals to include
            std = stats_df.squeeze()["std"]
            round_n_digits = get_n_decimals_to_include(std)

            filepath = os.path.join(self.tables_dirpath, f"dist_stats_table_{var}.tex")
            with open(filepath, "w") as f:
                f.write(
                    get_latex_table_bold_col_header(
                        stats_df, round_n_digits=round_n_digits
                    )
                )

        return stats_df

    def get_dist_stratified_stats_df(
        self,
        var: str,
        df: pd.DataFrame,
        col: str = "sexe_desc",
        show_nan_col: bool = True,
        save_table: bool = False,
        forced_order_col: Optional[List[str]] = None,
    ) -> pd.DataFrame:
        """
        Create a DataFrame with stratified distribution statistics for a numerical variable.
        
        Args:
            var: Variable to analyze
            df: DataFrame containing the data
            col: Column to stratify by
            show_nan_col: Whether to show NaN values in col as a separate category
            save_table: Whether to save the statistics as a LaTeX table
            forced_order_col: Optional custom ordering of categories for col
            
        Returns:
            DataFrame with stratified distribution statistics
        """
        # Preprocess df
        df = df[[var, col]].copy()
        df[col] = df[col].astype(str)
        if show_nan_col:
            df[col] = df[col].fillna(NAN_REPLACEMENT_STR)
        # Order variables alphabetically
        categorise_variable_in_df(col, df, forced_order=forced_order_col)

        stratified_stats_df = pd.DataFrame(df.groupby(col)[var].describe())

        # Convert 'count' column into 'int' type
        stratified_stats_df["count"] = stratified_stats_df["count"].astype(int)

        # Add number and percentage of NaNs
        stratified_stats_df.insert(
            1,
            "nan_perc",
            value=100 * df.groupby(col)[var].apply(lambda x: x.isna().mean()),
        )
        stratified_stats_df.insert(
            1, "n_nan", value=df.groupby(col)[var].apply(lambda x: x.isna().sum())
        )

        if save_table and self.tables_dirpath:
            # Get number of decimals to include
            std = stratified_stats_df["std"].min()
            round_n_digits = get_n_decimals_to_include(std)

            filepath = os.path.join(
                self.tables_dirpath,
                f"dist_stats_table_{var}_for_each_{col}.tex",
            )
            with open(filepath, "w") as f:
                f.write(
                    get_latex_table_bold_col_header(
                        stratified_stats_df, round_n_digits=round_n_digits
                    )
                )

        return stratified_stats_df


if __name__ == '__main__':
    print("DataVisualiser: A tool for data visualization and analysis")
    print("Import this module to use the functionality")
    print("Example: from data_visualiser_package import DataVisualiser")