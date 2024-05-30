import polars as pl
from itertools import product
from models.pre_dataframe_structure import PreDataframeStructure

def generate_cross_sectional_dataframe(model: PreDataframeStructure) -> pl.DataFrame:
    """
    Generates a cross-sectional DataFrame from the input data.

    Args:
        model (PreDataframeStructure): A Pydantic model containing data arrays and optional titles.

    Returns:
        pl.DataFrame: A Polars DataFrame with cross-sectional data and an additional 'AI_Output' column.
    """
    data = model.data
    titles = model.titles if model.titles is not None else [f'Feature{i+1}' for i in range(len(data))]

    combinations = list(product(*data))
    data_dict = {titles[i]: [comb[i] for comb in combinations] for i in range(len(titles))}
    data_dict['AI_Output'] = [""] * len(combinations)

    df = pl.DataFrame(data_dict)
    
    
    validate_output_dataframe(df, titles + ['AI_Output'], model.expectedrows)  # Optional validation
    return df


def validate_output_dataframe(df: pl.DataFrame, expected_columns: list, expected_row_count: int):
    """
    Validates the output DataFrame to ensure it meets specific requirements.

    Args:
        df (pl.DataFrame): The DataFrame to validate.
        expected_columns (list): The expected columns in the DataFrame.
        expected_row_count (int): The expected number of rows in the DataFrame.

    Raises:
        ValueError: If the DataFrame does not meet the expected requirements.
    """
    if not all(column in df.columns for column in expected_columns):
        raise ValueError("DataFrame does not contain the expected columns.")
    if 'AI_Output' not in df.columns:
        raise ValueError("DataFrame must contain the 'AI_Output' column.")
    if df.shape[0] != expected_row_count:
        raise ValueError(f"DataFrame has {df.shape[0]} rows; expected {expected_row_count} rows.")
    # Add more validation checks as needed

# Example usage
if __name__ == "__main__":
    data = [["USA", "Canada", "Mexico", "France", "Paraguay"], ["Sunny", "Rainy", "Cloudy"], ["123", "456", "789"]]
    model = PreDataframeStructure(data=data)
    print(model.expectedrows)
    df = generate_cross_sectional_dataframe(model)
    print(df)
