import datetime

import pydantic
from src.utilities.formatters.datetime_formatter import format_datetime_into_isoformat


class BaseSchemaModel(pydantic.BaseModel):
    class Config(pydantic.BaseConfig):
        from_attributes: bool = True
        validate_assignment: bool = True
        populate_by_name: bool = True
        json_encoders: dict = {datetime.datetime: format_datetime_into_isoformat}
        # alias_generator: typing.Any = format_dict_key_to_camel_case
