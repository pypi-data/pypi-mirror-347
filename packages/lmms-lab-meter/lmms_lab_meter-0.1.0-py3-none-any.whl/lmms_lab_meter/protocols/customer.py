import json
from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class Customer(BaseModel):
    """
    # JSON input template you can fill out and use as your body input.
    body = {
        "id": {},  # A unique identifier for the customer. Required.
        "name": "str",  # Human-readable name for the resource. Between 1 and 256
            characters. Required.
        "usageAttribution": {
            "subjectKeys": [
                "str"  # The subjects that are attributed to the customer.
                    Required.
            ]
        },
        "archivedAt": {},  # Optional. Timestamp of when the resource was archived.
        "billingAddress": {
            "city": "str",  # Optional. The billing address of the customer. Used
                for tax and invoicing.
            "country": "str",  # Optional. `ISO 3166-1
                <https://www.iso.org/iso-3166-country-codes.html>`_ alpha-2 country code.
                Custom two-letter country codes are also supported for convenience.
            "line1": "str",  # Optional. The billing address of the customer.
                Used for tax and invoicing.
            "line2": "str",  # Optional. The billing address of the customer.
                Used for tax and invoicing.
            "phoneNumber": "str",  # Optional. The billing address of the
                customer. Used for tax and invoicing.
            "postalCode": "str",  # Optional. The billing address of the
                customer. Used for tax and invoicing.
            "state": "str"  # Optional. The billing address of the customer. Used
                for tax and invoicing.
        },
        "createdAt": {},  # Optional. Timestamp of when the resource was created.
        "currency": {},  # Optional. Currency of the customer. Used for billing, tax
            and invoicing.
        "deletedAt": {},  # Optional. Timestamp of when the resource was permanently
            deleted.
        "description": "str",  # Optional. Optional description of the resource.
            Maximum 1024 characters.
        "external": {
            "stripeCustomerId": "str"  # Optional. The Stripe customer ID.
                Mapping to a Stripe Customer object. Required to use Stripe as an invocing
                provider.
        },
        "metadata": {},
        "primaryEmail": "str",  # Optional. The primary email address of the
            customer.
        "timezone": "str",  # Optional. Timezone of the customer.
        "updatedAt": {}  # Optional. Timestamp of when the resource was last updated.
    }

    """

    id: str  # A unique identifier for the customer. Required.
    name: str  # Human-readable name for the resource. Between 1 and 256 characters. Required.
    usageAttribution: Dict[
        str, List[str]
    ]  # The subjects that are attributed to the customer. Required.
    archivedAt: Union[
        str, None
    ] = None  # Optional. Timestamp of when the resource was archived.
    billingAddress: Dict[
        str, str
    ] = None  # Optional. The billing address of the customer. Used for tax and invoicing.
    createdAt: Union[
        str, None
    ] = None  # Optional. Timestamp of when the resource was created.
    currency: Union[
        str, None
    ] = None  # Optional. Currency of the customer. Used for billing, tax and invoicing.
    deletedAt: Union[
        str, None
    ] = None  # Optional. Timestamp of when the resource was permanently deleted.
    description: Union[
        str, None
    ] = None  # Optional. Optional description of the resource. Maximum 1024 characters.
    external: Union[
        Dict[str, str], None
    ] = None  # Optional. The Stripe customer ID. Mapping to a Stripe Customer object. Required to use Stripe as an invocing provider.
    metadata: Union[str, Dict[str, str]] = None
    primaryEmail: Union[
        str, None
    ] = None  # Optional. The primary email address of the customer.
    timezone: Union[str, None] = None  # Optional. Timezone of the customer.
    updatedAt: Union[
        str, None
    ] = None  # Optional. Timestamp of when the resource was last updated.
    # Add any additional fields or methods as needed
    key: Optional[str] = None  # Optional. The key of the customer. Used for lookup.

    def model_dump_json(self, **kwargs):
        json_format = super().model_dump(**kwargs)
        if self.key is None:
            json_format.pop("key", None)
        return json.dumps(json_format)
