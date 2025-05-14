import unittest
import pandas as pd
import numpy as np
from ashoks_data_tools import DataCleaner, plot_histogram
from ashoks_data_tools.subpackage import process_time_series

class TestDataCleaner(unittest.TestCase):
    
    def setUp(self):
        # Create test data
        self.test_data = pd.DataFrame({
            'A': [5, 2, np.nan, 2, 5],
            'B': [5, 6, 7, np.nan, 5]
        })
        self.cleaner = DataCleaner(self.test_data)
    
    def test_remove_duplicates(self):
        result = self.cleaner.remove_duplicates()
        self.assertEqual(len(result), 4)  # One duplicate removed
    
    def test_handle_missing_drop(self):
        result = self.cleaner.handle_missing_values(strategy='drop')
        self.assertEqual(len(result), 3)  # Two rows with NaN dropped
    
    def test_handle_missing_mean(self):
        result = self.cleaner.handle_missing_values(strategy='mean')
        self.assertFalse(result.isna().any().any())  # No NaN values
        self.assertEqual(float(result.loc[2, 'A']), 3.5)  # Mean of A is 2.5

    # def test_plot_historgram(self):
    #     clean_data = self.cleaner.handle_missing_values(strategy='mean')
    #     plot_histogram(clean_data, "A")
    #     print("ploted")


if __name__ == '__main__':
    unittest.main()
