"""
Data cleaning utilities for preprocessing datasets.
"""
import pandas as pd

class DataCleaner:
    """Class for cleaning and preprocessing data."""
    
    def __init__(self, data=None):
        """Initialize with optional data."""
        self.data = data
    
    def remove_duplicates(self, data=None):
        """Remove duplicate rows from a DataFrame."""
        df = data if data is not None else self.data
        if df is None:
            raise ValueError("No data provided")
        return df.drop_duplicates()
    
    def handle_missing_values(self, data=None, strategy='drop'):
        """
        Handle missing values in data.
        
        Args:
            data: DataFrame to process (uses self.data if None)
            strategy: How to handle missing values ('drop', 'mean', 'median', 'zero')
        """
        df = data if data is not None else self.data
        if df is None:
            raise ValueError("No data provided")
            
        if strategy == 'drop':
            return df.dropna()
        elif strategy == 'mean':
            return df.fillna(df.mean())
        elif strategy == 'median':
            return df.fillna(df.median())
        elif strategy == 'zero':
            return df.fillna(0)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")
