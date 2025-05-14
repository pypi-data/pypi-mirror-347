from typing import Dict, Union

from pydantic import BaseModel


class Event(BaseModel):
    """
    # JSON input template you can fill out and use as your body input.
    body = {
        "id": "str",  # Identifies the event. Required.
        "source": "str",  # Identifies the context in which an event happened.
            Required.
        "specversion": "str",  # The version of the CloudEvents specification which
            the event uses. Required.
        "subject": "str",  # Describes the subject of the event in the context of the
            event producer (identified by source). Required.
        "type": "str",  # Describes the type of event related to the originating
            occurrence. Required.
        "data": {
            "str": {}  # Optional. The event payload.
        },
        "datacontenttype": "str",  # Optional. Content type of the data value. Must
            adhere to RFC 2046 format. "application/json"
        "dataschema": "str",  # Optional. Identifies the schema that data adheres to.
        "time": "2020-02-20 00:00:00"  # Optional. Timestamp of when the occurrence
            happened. Must adhere to RFC 3339.
    }
    """

    id: str
    source: str
    specversion: str
    subject: str
    type: str
    data: Union[Dict, None] = None
    datacontenttype: Union[str, None] = None
    dataschema: Union[str, None] = None
    time: Union[str, None] = None
