from typing import Dict, Optional, Union

from pydantic import BaseModel


class Feature(BaseModel):
    """
    Features are either metered or static.
    A feature is metered if meterSlug is provided at creation.
    For metered features you can pass additional filters that will be applied when calculating feature usage,
    based on the meter's groupBy fields.
    Only meters with SUM and COUNT aggregation are supported for features.
    Features cannot be updated later, only archived.
    """

    key: str
    name: str
    meterSlug: Optional[str] = None
    meterGroupByFilters: Optional[Dict[str, str]] = None
    metadata: Optional[Dict[str, str]] = {}
