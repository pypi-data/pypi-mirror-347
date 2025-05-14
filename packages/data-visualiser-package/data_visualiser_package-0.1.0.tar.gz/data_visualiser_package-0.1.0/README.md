# Data Visualiser Package

A Python utility package for data visualization and statistical analysis with Matplotlib and Seaborn. This package provides a simple interface to create common visualizations and statistical tables for exploratory data analysis and reporting.

## Installation

```bash
pip install data-visualiser-package
```

## Features

- Create count plots and distribution plots
- Generate stratified visualizations by categorical variables
- Compute and display statistical tables for numerical and categorical variables
- Save plots and tables to disk (including LaTeX export)
- Handling of missing values

## Quick Start

```python
import pandas as pd
from data_visualiser_package import DataVisualiser

# Create a DataVisualiser instance
dv = DataVisualiser(
    record_unit_name="patient",  # What a single record represents
    figures_dirpath="./figures", # Where to save figures
    tables_dirpath="./tables",   # Where to save tables
    create_dirs=True             # Create directories if they don't exist
)

# Load your data
df = pd.read_csv("your_data.csv")

# Create a count plot
fig, ax = dv.get_count_plot(
    var="diagnosis",          # Categorical variable to plot
    df=df,                   # DataFrame containing the data
    show_nan=True,           # Show NaN values as a separate category
    save_fig=True            # Save the figure to disk
)

# Create a distribution plot
fig, ax = dv.get_dist_plot(
    var="age",              # Numerical variable to plot
    df=df,                  # DataFrame containing the data
    save_fig=True           # Save the figure to disk
)

# Generate statistics tables
stats_df = dv.get_count_stats_df(
    var="diagnosis",        # Categorical variable to analyze
    df=df,                  # DataFrame containing the data
    save_table=True         # Save the table to disk as LaTeX
)

# Create stratified visualizations
fg = dv.get_dist_stratified_plot(
    var="age",              # Numerical variable to plot
    df=df,                  # DataFrame containing the data
    col="gender",           # Categorical variable to stratify by
    save_fig=True           # Save the figure to disk
)
```

## Example

Here's a complete example of how to use the DataVisualiser class:

```python
import pandas as pd
import numpy as np
from data_visualiser_package import DataVisualiser

# Create a sample dataset
np.random.seed(42)
n = 1000

# Generate sample data
data = {
    'age': np.random.normal(50, 15, n),
    'gender': np.random.choice(['Male', 'Female'], n),
    'diagnosis': np.random.choice(['Healthy', 'Condition A', 'Condition B', None], n, p=[0.6, 0.2, 0.15, 0.05]),
    'heart_rate': np.random.normal(80, 10, n),
    'blood_pressure': np.random.normal(120, 15, n)
}

# Create a DataFrame
df = pd.DataFrame(data)

# Initialize the DataVisualiser
dv = DataVisualiser(
    record_unit_name="patient",
    figures_dirpath="./output/figures",
    tables_dirpath="./output/tables",
    create_dirs=True
)

# Create plots
dv.get_count_plot('gender', df, save_fig=True)
dv.get_count_plot('diagnosis', df, save_fig=True)

# Create stratified count plots
dv.get_count_stratified_plot('diagnosis', df, col='gender', save_fig=True)

# Distribution plots
dv.get_dist_plot('age', df, save_fig=True)
dv.get_dist_stratified_plot('age', df, col='gender', save_fig=True)
dv.get_dist_hued_plot('age', df, hue='gender', save_fig=True)

# Generate statistics tables
dv.get_count_stats_df('diagnosis', df, save_table=True)
dv.get_dist_stats_df('age', df, save_table=True)
dv.get_dist_stratified_stats_df('age', df, col='gender', save_table=True)

print("All visualizations and tables have been generated successfully!")
```

## API Reference

### DataVisualiser Class

```python
class DataVisualiser(
    record_unit_name="patient",
    figures_dirpath=None,
    tables_dirpath=None,
    create_dirs=False
)
```

#### Count Visualizations

- `get_count_plot(var, df, show_nan=True, save_fig=False, plot_kwargs={}, xlabels_rotation=None, forced_order=None)`
- `get_count_stratified_plot(var, df, col="gender", show_nan=True, show_nan_col=True, save_fig=False, col_wrap=3, plot_kwargs={}, xlabels_rotation=None, forced_order=None, forced_order_col=None)`
- `get_count_stats_df(var, df, show_nan=True, save_table=False, percentage=True, add_total=False, round_n_digits=1, forced_order=None)`
- `get_count_stratified_stats_df(var, df, col="gender", show_nan=True, show_nan_col=True, save_table=False, percentage=True, round_n_digits=1, forced_order=None, forced_order_col=None)`

#### Distribution Visualizations

- `get_dist_plot(var, df, save_fig=False, plot_kwargs={"kde": True}, xlabels_rotation=None)`
- `get_dist_stratified_plot(var, df, col="gender", show_nan_col=True, save_fig=False, col_wrap=3, plot_kwargs={"kde": True}, xlabels_rotation=None, forced_order_col=None)`
- `get_dist_hued_plot(var, df, hue="gender", show_nan_col=True, save_fig=False, plot_kwargs={"kde": True}, xlabels_rotation=None, forced_order_col=None)`
- `get_dist_stats_df(var, df, save_table=False)`
- `get_dist_stratified_stats_df(var, df, col="gender", show_nan_col=True, save_table=False, forced_order_col=None)`

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.