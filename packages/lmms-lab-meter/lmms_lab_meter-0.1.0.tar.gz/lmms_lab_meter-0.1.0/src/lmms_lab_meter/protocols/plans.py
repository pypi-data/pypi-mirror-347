from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel


class BaseEntitlementTemplate(BaseModel):
    """
    Entitlement templates are used to define the entitlements of a plan.
    Features are omitted from the entitlement template, as they are defined in the rate card.
    """

    type: Literal["metered", "static", "boolean"]
    metadata: Optional[Dict[str, str]] = None


class MeteredEntitlementTemplate(BaseEntitlementTemplate):
    usagePeriod: str = None
    issueAfterReset: Union[float, None] = None
    issueAfterResetPriority: Union[int, None] = None
    isSoftLimit: bool = False
    preserveOverageAtReset: bool = False


class StaticEntitlementTemplate(BaseEntitlementTemplate):
    config: str  # The JSON parsable config of the entitlement. This value is also returned when checking entitlement access and it is useful for configuring fine-grained access settings to the feature, implemented in your own system. Has to be an object.


EntitlementTemplate = Union[
    MeteredEntitlementTemplate, StaticEntitlementTemplate, BaseEntitlementTemplate
]


class RateCard(BaseModel):
    """
    A rate card defines the pricing and entitlement of a feature or service.
    """

    type: str
    key: str
    name: str
    billingCadence: str
    price: Dict[str, str]
    description: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None
    featureKey: Optional[str] = None
    entitlementTemplate: Optional[EntitlementTemplate] = None
    taxConfig: Union[Dict[str, str], None] = {}
    discount: Union[Dict[str, str], None] = None


class Phase(BaseModel):
    """
    The plan phase or pricing ramp allows changing a plan's rate cards over time as a subscription progresses. A phase switch occurs only at the end of a billing period, ensuring that a single subscription invoice will not include charges from different phase prices.
    """

    key: str
    name: str
    duration: Union[str, None]
    rateCards: List[RateCard]
    description: Optional[str] = None
    metadata: Optional[Dict[str, str]] = None


class Plan(BaseModel):
    """
    Plans are the core building blocks of your product catalog.
    They are a collection of rate cards that define the price and access of a feature.
    Plans can be assigned to customers by starting a subscription.
    """

    name: str
    description: str
    key: str
    currency: str
    phases: List[Phase]
    alignment: Optional[Dict[str, bool]] = {}
    metadata: Optional[Dict[str, str]] = None
