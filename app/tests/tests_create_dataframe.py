import unittest
from pydantic import ValidationError
from app.models.pre_dataframe_structure import PreDataframeStructure
from app.utils.generate_cross_sectional_dataframe import generate_cross_sectional_dataframe 
import polars as pl

class TestGenerateCrossSectionalDataFrame(unittest.TestCase):

    def test_generate_dataframe(self):
        data = [
            ["USA", "Canada", "Mexico"],
            ["Sunny", "Rainy", "Cloudy"],
            [1, 2, 3]
        ]

        titles = ["Country", "Weather", "Month"]
        model = PreDataframeStructure(data=data, titles=titles, ai_output_columns=2)
        df = generate_cross_sectional_dataframe(model)

        self.assertIsInstance(df, pl.DataFrame)
        self.assertListEqual(df.columns, ["Country", "Weather", "Month", "AI_Output_1", "AI_Output_2"])
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
        self.assertListEqual(df.columns, ["Feature1", "Feature2", "Feature3", "AI_Output_1"])
        self.assertEqual(len(df), len(data[0]) * len(data[1]) * len(data[2]))

    def test_invalid_data(self):
        invalid_data_cases = [
            ([], "There must be at least one array in data"),
            ([["USA", "Canada"], [], ["Jan", "Feb"]], "None of the arrays in data can be empty"),
            ([["USA", "Canada"], ["Sunny", "Rainy"], [123, "Feb"]], "All items in each array must be all strings or all numbers")
        ]

        for data, error_msg in invalid_data_cases:
            with self.subTest(data=data, error_msg=error_msg):
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
            (["Country", "Weather", "AI_Output2"], "Titles cannot begin with 'AI_Output'")
        ]

        for titles, error_msg in invalid_titles_cases:
            with self.assertRaises(ValidationError) as context:
                PreDataframeStructure(data=data, titles=titles)
            self.assertIn(error_msg, str(context.exception))

if __name__ == '__main__':
    unittest.main()
