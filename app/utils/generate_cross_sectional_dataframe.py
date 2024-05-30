import polars as pl
from itertools import product
from app.models.pre_dataframe_structure import PreDataframeStructure

def generate_cross_sectional_dataframe(model: PreDataframeStructure) -> pl.DataFrame:
    """
    Generates a cross-sectional DataFrame from the input data.

    Args:
        model (PreDataframeStructure): A Pydantic model containing data arrays and optional titles.

    Returns:
        pl.DataFrame: A Polars DataFrame with cross-sectional data and an additional 'AI_Output' column.
    """
    ai_output_columns = model.ai_output_columns
    data = model.data
    titles = model.titles if model.titles is not None else [f'Feature{i+1}' for i in range(len(data))]

    combinations = list(product(*data))
    data_dict = {titles[i]: [comb[i] for comb in combinations] for i in range(len(titles))}

    df = pl.DataFrame(data_dict)
    df = append_ai_columns(df, ai_output_columns)
    
    
    validate_output_dataframe(df, len(data) + ai_output_columns, model.maximumrows)  # Optional validation
    return df


def validate_output_dataframe(df: pl.DataFrame, expected_columns: int, expected_row_count: int):
    """
    Validates the output DataFrame to ensure it meets specific requirements.

    Args:
        df (pl.DataFrame): The DataFrame to validate.
        expected_columns (list): The expected columns in the DataFrame.
        expected_row_count (int): The expected number of rows in the DataFrame.

    Raises:
        ValueError: If the DataFrame does not meet the expected requirements.
    """
    if len(df.columns) != expected_columns:
        raise ValueError(f"DataFrame has {len(df.columns)} columns; expected {expected_columns} columns.")
    if 'AI_Output_1' not in df.columns:
        raise ValueError("DataFrame must contain the 'AI_Output_1' column.")
    if df.shape[0] != expected_row_count:
        raise ValueError(f"DataFrame has {df.shape[0]} rows; expected {expected_row_count} rows.")
    # Add more validation checks as needed


def append_ai_columns(df: pl.DataFrame, ai_columns: int) -> pl.DataFrame:

    for i in range(ai_columns):
        df = df.with_columns(pl.lit("").alias(f'AI_Output_{i+1}'))  # Add empty string columns
    return df

# Example usage
if __name__ == "__main__":
    data = [["USA", "Canada", "Mexico", "France", "Paraguay"], ["Sunny", "Rainy", "Cloudy", "Snowy"], [1,2, 4.3]]
    titles = ["Country", "Weather", "Month"]
    model = PreDataframeStructure(data=data, titles=titles)
    print(model.maximumrows)
    df = generate_cross_sectional_dataframe(model)
    print(df)
