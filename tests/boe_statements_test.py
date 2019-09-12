"""Testing DataExtractor on some test cases"""
import unittest
import warnings

import pandas as pd

from model.data_extraction import DataExtractor

warnings.filterwarnings('ignore')


class TestDataExtraction(unittest.TestCase):
    """Test case for data extraction"""

    def setUp(self):
        self.data = pd.read_csv("test_data/boe_statements_test.csv", index_col=0)
        self.statements = self.data.statement.values.tolist()
        self.rates = [x for x in self.data.rate]
        self.qes = [x for x in self.data.qe]
        self.data_extractor = DataExtractor()

    def test_extractor(self):
        results = self.data_extractor.analyse(self.statements)
        for statement, rate, qe, result in zip(self.statements, self.rates, self.qes, results):
            rate_result = result.get('Bank_Rate', '')
            qe_result = result.get('QE', '')
            assert str(rate) == rate_result and str(qe) == qe_result

        print(f'test cases run successfully!...')
