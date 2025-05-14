"""
Data visualization utilities for creating plots and charts.
"""
import matplotlib.pyplot as plt

def plot_histogram(data, column, bins=10, title=None, figsize=(8, 6)):
    """
    Create a histogram of a data column.
    
    Args:
        data: DataFrame containing the data
        column: Column name to plot
        bins: Number of histogram bins
        title: Plot title
        figsize: Figure size tuple (width, height)
    """
    plt.figure(figsize=figsize)
    plt.hist(data[column], bins=bins)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.title(title or f'Histogram of {column}')
    plt.tight_layout()
    plt.show()
    return plt.gcf()

def plot_scatter(data, x_col, y_col, title=None, figsize=(8, 6)):
    """
    Create a scatter plot of two data columns.
    
    Args:
        data: DataFrame containing the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Plot title
        figsize: Figure size tuple (width, height)
    """
    plt.figure(figsize=figsize)
    plt.scatter(data[x_col], data[y_col])
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(title or f'Scatter plot of {y_col} vs {x_col}')
    plt.tight_layout()
    return plt.gcf()
