from pydantic import BaseModel, Field, field_validator, ValidationError, ValidationInfo
from typing import List, Optional
from math import prod


class PreDataframeStructure(BaseModel):
    data: List[List[str]]
    titles: Optional[List[str]] = None

    @field_validator('data')
    def check_data(cls, value):
        if not isinstance(value, list) or not all(isinstance(item, list) for item in value):
            raise ValueError('Data must be a list of arrays')
        if len(value) == 0:
            raise ValueError('There must be at least one array in data')
        for array in value:
            if not array:
                raise ValueError('None of the arrays in data can be empty')
        
        return value

    @field_validator('titles', mode='before')
    def check_titles(cls, titles: Optional[List[str]], values: ValidationInfo) -> Optional[List[str]]:
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
        if "AI_Output" in titles:
            raise ValueError("Titles must not contain 'AI_Output'")
        return titles

    @property
    def expectedrows(self) -> int:
        lengths = [len(array) for array in self.data]
        return prod(lengths)