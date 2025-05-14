"""
Advanced data processing utilities.
"""
import pandas as pd

def process_time_series(df, date_column, value_column, freq='D'):
    """
    Process time series data for analysis.
    
    Args:
        df: DataFrame with time series data
        date_column: Name of the date column
        value_column: Name of the value column
        freq: Frequency for resampling ('D' for daily, 'M' for monthly, etc.)
    """
    df = df.copy()
    df[date_column] = pd.to_datetime(df[date_column])
    df = df.set_index(date_column)
    return df[value_column].resample(freq).mean()
