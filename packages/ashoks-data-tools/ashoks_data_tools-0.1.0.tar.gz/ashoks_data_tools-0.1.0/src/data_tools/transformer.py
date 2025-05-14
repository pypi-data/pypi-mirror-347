"""
Data transformation utilities for converting data formats.
"""
import pandas as pd
import numpy as np

class DataTransformer:
    """Class for transforming data between different formats and structures."""
    
    def __init__(self):
        """Initialize the transformer."""
        pass
    
    def normalize(self, data):
        """Normalize numeric columns in the dataframe."""
        numeric_cols = data.select_dtypes(include=[np.number]).columns
        result = data.copy()
        
        for col in numeric_cols:
            min_val = data[col].min()
            max_val = data[col].max()
            result[col] = (data[col] - min_val) / (max_val - min_val)
        
        return result
    
    def one_hot_encode(self, data, categorical_cols=None):
        """One-hot encode categorical columns."""
        if categorical_cols is None:
            categorical_cols = data.select_dtypes(include=['object', 'category']).columns
            
        return pd.get_dummies(data, columns=categorical_cols)


def transform_data(data, transformation_type='normalize'):
    """
    Utility function for quick data transformations.
    
    Args:
        data: DataFrame to transform
        transformation_type: Type of transformation ('normalize', 'one_hot')
    """
    transformer = DataTransformer()
    
    if transformation_type == 'normalize':
        return transformer.normalize(data)
    elif transformation_type == 'one_hot':
        return transformer.one_hot_encode(data)
    else:
        raise ValueError(f"Unknown transformation type: {transformation_type}")
