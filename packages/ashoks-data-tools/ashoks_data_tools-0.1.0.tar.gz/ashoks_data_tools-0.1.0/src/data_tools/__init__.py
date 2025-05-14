"""
Data Tools package for data processing and analysis.

This package provides utilities for:
- Data cleaning
- Data transformation
- Data visualization
"""

# Import and expose key classes/functions from submodules
from .cleaner import DataCleaner
from .transformer import DataTransformer, transform_data
from .visualizer import plot_histogram, plot_scatter

# Define what should be available when someone does "from ashoks_data_tools import *"
__all__ = ['DataCleaner', 'DataTransformer', 'transform_data', 'plot_histogram', 'plot_scatter']

# Package metadata
__version__ = '0.1.0'
__author__ = 'Ashok Neupane'
