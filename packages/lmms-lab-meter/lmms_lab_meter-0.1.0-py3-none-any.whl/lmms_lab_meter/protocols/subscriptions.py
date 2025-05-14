import json
from typing import Dict, Optional, Union

from pydantic import BaseModel


class PlanBasedSubscription(BaseModel):
    """
    Plan-based subscription model.
    """

    alignment: Dict[str, bool]
    metadata: Dict[str, str]
    plan: Dict[str, str]
    name: str
    description: str
    timing: str
    customerId: Optional[str] = None
    customerKey: Optional[str] = None

    def model_dump_json(self, **kwargs):
        json_format = super().model_dump(**kwargs)
        if self.customerId is None and self.customerKey is None:
            raise ValueError("Either customerId or customerKey must be provided.")
        # predencene customerid over customerkey
        # If customerId is provided, remove customerKey from the JSON
        # If customerKey is provided, remove customerId from the JSON
        if self.customerId is not None:
            json_format.pop("customerKey", None)
        if self.customerKey is not None:
            json_format.pop("customerId", None)
        return json.dumps(json_format)


Subscription = Union[PlanBasedSubscription]
