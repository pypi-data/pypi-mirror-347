"""
DataVisualiser Package Demo

This script demonstrates how to use the DataVisualiser package with a sample dataset.
"""
import os
import pandas as pd
import numpy as np
from data_visualiser_package import DataVisualiser

def main():
    # Create output directories
    os.makedirs("./demo_output/figures", exist_ok=True)
    os.makedirs("./demo_output/tables", exist_ok=True)
    
    # Create a sample dataset
    np.random.seed(42)
    n = 1000
    
    # Generate sample data
    data = {
        'age': np.random.normal(50, 15, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'diagnosis': np.random.choice(['Healthy', 'Condition A', 'Condition B', None], n, p=[0.6, 0.2, 0.15, 0.05]),
        'heart_rate': np.random.normal(80, 10, n),
        'blood_pressure': np.random.normal(120, 15, n),
        'treatment': np.random.choice(['Drug A', 'Drug B', 'Placebo', None], n),
        'response': np.random.choice(['Good', 'Moderate', 'Poor', None], n, p=[0.5, 0.3, 0.15, 0.05]),
    }
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    print("Sample data created:")
    print(df.head())
    print(f"\nDataset shape: {df.shape}")
    print("\nData types:")
    print(df.dtypes)
    print("\nMissing values:")
    print(df.isna().sum())
    
    # Initialize the DataVisualiser
    dv = DataVisualiser(
        record_unit_name="patient",
        figures_dirpath="./demo_output/figures",
        tables_dirpath="./demo_output/tables",
        create_dirs=True
    )
    
    print("\n1. Creating count plots...")
    # Create count plots for categorical variables
    dv.get_count_plot('gender', df, save_fig=True)
    dv.get_count_plot('diagnosis', df, save_fig=True)
    dv.get_count_plot('treatment', df, save_fig=True)
    dv.get_count_plot('response', df, save_fig=True)
    
    print("2. Creating stratified count plots...")
    # Create stratified count plots
    dv.get_count_stratified_plot('diagnosis', df, col='gender', save_fig=True)
    dv.get_count_stratified_plot('response', df, col='treatment', save_fig=True)
    
    print("3. Creating distribution plots...")
    # Distribution plots for numerical variables
    dv.get_dist_plot('age', df, save_fig=True)
    dv.get_dist_plot('heart_rate', df, save_fig=True)
    dv.get_dist_plot('blood_pressure', df, save_fig=True)
    
    print("4. Creating stratified distribution plots...")
    # Create stratified distribution plots
    dv.get_dist_stratified_plot('age', df, col='gender', save_fig=True)
    dv.get_dist_stratified_plot('heart_rate', df, col='diagnosis', save_fig=True)
    
    print("5. Creating hued distribution plots...")
    # Create hued distribution plots
    dv.get_dist_hued_plot('blood_pressure', df, hue='gender', save_fig=True)
    
    print("6. Generating statistics tables...")
    # Generate statistics tables
    count_stats = dv.get_count_stats_df('diagnosis', df, save_table=True)
    print("\nCount statistics for diagnosis:")
    print(count_stats)
    
    dist_stats = dv.get_dist_stats_df('age', df, save_table=True)
    print("\nDistribution statistics for age:")
    print(dist_stats)
    
    strat_dist_stats = dv.get_dist_stratified_stats_df('heart_rate', df, col='gender', save_table=True)
    print("\nStratified distribution statistics for heart_rate by gender:")
    print(strat_dist_stats)
    
    print("\nAll visualizations and tables have been generated successfully!")
    print(f"Check the demo_output directory for the generated files.")

if __name__ == "__main__":
    main()
