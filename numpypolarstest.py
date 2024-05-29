import polars as pl
from itertools import product

def create_dataframe(data, titles=None):
    # Define default column titles if not provided
    if titles is None:
        titles = [f'Feature{i+1}' for i in range(len(data))]
    
    # Ensure titles length matches data length
    if len(titles) != len(data):
        raise ValueError("Length of titles must match length of data arrays")

    # Generate all combinations of the input arrays
    combinations = list(product(*data))

    # Create dictionary for DataFrame creation
    data_dict = {titles[i]: [comb[i] for comb in combinations] for i in range(len(titles))}
    
    # Add the fourth column for predicted variable
    data_dict['Predicted'] = [None] * len(combinations)

    # Create and return the DataFrame
    df = pl.DataFrame(data_dict)
    return df

# Example usage
data = [
    ["USA", "Canada", "Mexico"],
    ["Sunny", "Rainy", "Cloudy"],
    ["January", "February", "March"]
]

titles = ["Country", "Weather", "Month"]

df = create_dataframe(data, titles)
print(df)
