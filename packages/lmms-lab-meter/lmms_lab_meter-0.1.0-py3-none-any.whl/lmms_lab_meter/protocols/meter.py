from typing import Dict, Literal, Union

from pydantic import BaseModel


class Meter(BaseModel):
    """
    # JSON input template you can fill out and use as your body input.
    body = {
        "aggregation": "str",  # The aggregation type to use for the meter. Required.
            Known values are: "SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", and "MAX".
        "eventType": "str",  # The event type to aggregate. Required.
        "slug": "str",  # A unique, human-readable identifier for the meter. Must
            consist only alphanumeric and underscore characters. Required.
        "windowSize": "str",  # Aggregation window size. Required. Known values are:
            "MINUTE", "HOUR", and "DAY".
        "description": "str",  # Optional. A description of the meter.
        "groupBy": {
            "str": "str"  # Optional. Named JSONPath expressions to extract the
                group by values from the event data. Keys must be unique and consist only
                alphanumeric and underscore characters.
        },
        "id": "str",  # Optional. A unique identifier for the meter.
        "valueProperty": "str"  # Optional. JSONPath expression to extract the value
            from the ingested event's data property. The ingested value for SUM, AVG, MIN,
            and MAX aggregations is a number or a string that can be parsed to a number. For
            UNIQUE_COUNT aggregation, the ingested value must be a string. For COUNT
            aggregation the valueProperty is ignored.
    }
    """

    aggregation: Literal[
        "SUM", "COUNT", "UNIQUE_COUNT", "AVG", "MIN", "MAX"
    ]  # The aggregation type to use for the meter. Required.
    eventType: str  # The event type to aggregate. Required.
    slug: str  # A unique, human-readable identifier for the meter. Must
    # consist only alphanumeric and underscore characters. Required.
    windowSize: Literal["MINUTE", "HOUR", "DAY"]  # Aggregation window size. Required.
    description: Union[str, None] = None  # Optional. A description of the meter.
    groupBy: Union[
        Dict[str, str], None
    ] = None  # Optional. Named JSONPath expressions to extract the group by values from the event data. Keys must be unique and consist only alphanumeric and underscore characters.
    id: Union[str, None] = None  # Optional. A unique identifier for the meter.
    valueProperty: Union[
        str, None
    ] = None  # Optional. JSONPath expression to extract the value from the ingested event's data property.
