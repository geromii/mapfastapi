import unittest
from pydantic import ValidationError
from models.pre_dataframe_structure import PreDataframeStructure
from utils.generate_cross_sectional_dataframe import generate_cross_sectional_dataframe  # Make sure to replace 'your_script' with the actual script name
import polars as pl

class TestGenerateCrossSectionalDataFrame(unittest.TestCase):

    def test_generate_dataframe(self):
        data = [
            ["USA", "Canada", "Mexico"],
            ["Sunny", "Rainy", "Cloudy"],
            ["Jan", "Feb", "Mar"]
        ]

        titles = ["Country", "Weather", "Month"]
        model = PreDataframeStructure(data=data, titles=titles)
        df = generate_cross_sectional_dataframe(model)

        self.assertIsInstance(df, pl.DataFrame)
        self.assertListEqual(df.columns, ["Country", "Weather", "Month", "AI_Output"])
        self.assertEqual(len(df), len(data[0]) * len(data[1]) * len(data[2]))

    def test_missing_titles(self):
        data = [
            ["USA", "Canada", "Mexico"],
            ["Sunny", "Rainy", "Cloudy"],
            ["Jan", "Feb", "Mar", "Apr"]
        ]

        model = PreDataframeStructure(data=data)
        df = generate_cross_sectional_dataframe(model)

        self.assertIsInstance(df, pl.DataFrame)
        self.assertListEqual(df.columns, ["Feature1", "Feature2", "Feature3", "AI_Output"])
        self.assertEqual(len(df), len(data[0]) * len(data[1]) * len(data[2]))

    def test_invalid_data(self):
        invalid_data_cases = [
            ([], "There must be at least one array in data"),
            ([["USA", "Canada"], [], ["Jan", "Feb"]], "None of the arrays in data can be empty"),
            ([["USA", "Canada"], ["Sunny", "Rainy"], [123, "Feb"]], "Input should be a valid string")
        ]

        for data, error_msg in invalid_data_cases:
            with self.assertRaises(ValidationError) as context:
                PreDataframeStructure(data=data)
            self.assertIn(error_msg, str(context.exception))

    def test_invalid_titles(self):
        data = [
            ["USA", "Canada", "Mexico"],
            ["Sunny", "Rainy", "Cloudy"],
            ["Jan", "Feb", "Mar"]
        ]

        invalid_titles_cases = [
            (["Country"], "Number of titles must match number of arrays"),
            (["Country", "Weather", "Weather"], "Titles must not contain duplicates"),
            (["Country", "Weather", "AI_Output"], "Titles must not contain 'AI_Output'")
        ]

        for titles, error_msg in invalid_titles_cases:
            with self.assertRaises(ValidationError) as context:
                PreDataframeStructure(data=data, titles=titles)
            self.assertIn(error_msg, str(context.exception))

if __name__ == '__main__':
    unittest.main()
