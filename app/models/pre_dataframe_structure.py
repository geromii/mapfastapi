from pydantic import BaseModel, Field, field_validator, ValidationError, ValidationInfo
from typing import List, Union, Optional
from math import prod

class PreDataframeStructure(BaseModel):
    """
    A Pydantic model for validating and managing input data for generating a cross-sectional DataFrame.

    Attributes:
        data (List[List[Union[str, int, float]]]): A list of lists containing the data arrays.
        titles (Optional[List[str]]): An optional list of titles for the data arrays.
    """

    data: List[List[Union[str, int, float]]]
    titles: Optional[List[str]] = None
    ai_output_columns: int = 1

    @field_validator('data')
    def check_data(cls, value):
        """
        Validates the 'data' field to ensure it is a list of non-empty arrays
        and all items in each array are of the same data type.

        Args:
            value (list): The input data to validate.

        Returns:
            list: The validated data.

        Raises:
            ValueError: If the data is not a list of arrays, if any array is empty,
                        or if items in any array are not of the same data type.
        """
        if not isinstance(value, list) or not all(isinstance(item, list) for item in value):
            raise ValueError('Data must be a list of arrays')
        if len(value) == 0:
            raise ValueError('There must be at least one array in data')
        
        for array in value:
            if not array:
                raise ValueError('None of the arrays in data can be empty')
            
            first_type = type(array[0])
            if first_type != str:
                accepted_type = Union[int, float]
            else:
                accepted_type = str

            for item in array:
                if not isinstance(item, accepted_type):
                    raise ValueError(f'All items in each array must be all strings or all numbers, but {item} in the array beginning with {array[:3]} is not a {first_type.__name__}')
        
        return value

    @field_validator('titles', mode='before')
    def check_titles(cls, titles: Optional[List[str]], values: ValidationInfo) -> Optional[List[str]]:
        """
        Validates the 'titles' field to ensure it matches the data length and has no duplicates or forbidden values.

        Args:
            titles (Optional[List[str]]): The input titles to validate.
            values (ValidationInfo): Contextual information for validation, including the 'data' field.

        Returns:
            Optional[List[str]]: The validated or default titles.

        Raises:
            ValueError: If the number of titles does not match the number of data arrays, if there are duplicates,
                        or if 'AI_Output' is included (AI_Output is reserved for the prediction column).
        """
        data = values.data.get('data')

        # Skip validation if data returns error
        if data is None:
            return titles

        data_length = len(data)
        if titles is None:
            return [f'Feature{i+1}' for i in range(data_length)]
        if len(titles) != data_length:
            raise ValueError("Number of titles must match number of arrays")
        if len(set(titles)) != len(titles):
            raise ValueError("Titles must not contain duplicates")
        if any(title.startswith("AI_Output") for title in titles):
            raise ValueError("Titles cannot begin with 'AI_Output'")
        return titles

    @property
    def maximumrows(self) -> int:
        """
        Calculates the maximum number of rows in the resulting DataFrame based on the input data.

        Returns:
            int: The maximum number of rows.
        """
        lengths = [len(array) for array in self.data]
        return prod(lengths)

# Example usage:
# data = [["USA", "Canada", "Mexico", "France", "Paraguay"], ["Sunny", "Rainy", "Cloudy"], [123, 456, 789.0]]
# model = PreDataframeStructure(data=data)
# df = generate_cross_sectional_dataframe(model)
# print(df)
