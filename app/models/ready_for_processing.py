from pydantic import BaseModel, field_validator
from typing import Any
import polars as pl

class PolarsDataFrame:
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, _) -> pl.DataFrame:
        if not isinstance(v, pl.DataFrame):
            raise TypeError('Polars DataFrame required')
        return v

class ReadyForProcessing(BaseModel):
    dataframe: PolarsDataFrame
    prompt: str

    @field_validator('dataframe')
    def check_dataframe(cls, v):
        # Here you can add any custom validation logic for the DataFrame
        if v.shape[0] == 0:
            raise ValueError('DataFrame cannot be empty')
        return v

# Example usage
df = pl.DataFrame({"a": [1, 2, 3]})
model = ReadyForProcessing(dataframe=df, prompt="example")

print(model)
