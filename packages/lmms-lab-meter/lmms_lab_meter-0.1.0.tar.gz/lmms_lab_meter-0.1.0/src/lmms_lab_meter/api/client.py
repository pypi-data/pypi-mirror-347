import http.client
import json
import os

from ..protocols import (
    Customer,
    EntitlementTemplate,
    Event,
    Feature,
    Meter,
    Plan,
    Subscription,
)


class LMMsLabMeterClient:
    """
    A client for interacting with the LMMS LabMeter API.
    """

    def __init__(self, api_key: str = None, base_url: str = None):
        """
        Initializes the client with the given API key.

        Args:
            api_key (str): The API key for authenticating with the LabMeter API.
        """
        if api_key is None:
            self.api_key = os.getenv("OPENMETER_API_KEY", "YOUR_API_KEY")
        else:
            self.api_key = api_key

        if base_url is None:
            self.base_url = os.getenv("OPENMETER_ENDPOINT", "openmeter.cloud")
        else:
            self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        self.conn = http.client.HTTPSConnection(self.base_url)

    @property
    def meter_endpoint(self) -> str:
        """
        Returns the endpoint for creating a meter.
        """
        return f"/api/v1/meters"

    @property
    def customer_endpoint(self) -> str:
        """
        Returns the endpoint for creating a customer.
        """
        return f"/api/v1/customers"

    @property
    def event_endpoint(self) -> str:
        """
        Returns the endpoint for creating an event.
        """
        return f"/api/v1/events"

    @property
    def plan_endpoint(self) -> str:
        """
        Returns the endpoint for creating a plan.
        """
        return f"/api/v1/plans"

    @property
    def feature_endpoint(self) -> str:
        """
        Returns the endpoint for creating a feature.
        """
        return f"/api/v1/features"

    @property
    def subject_endpoint(self) -> str:
        """
        Returns the endpoint for creating a subject.
        """
        return f"/api/v1/subjects"

    @property
    def subscription_endpoint(self) -> str:
        """
        Returns the endpoint for creating a subscription.
        """
        return f"/api/v1/subscriptions"

    def handle_response(self) -> dict:
        """
        Handles the response from the API.

        Returns:
            dict: The response from the API.
        """
        response = self.conn.getresponse()
        data = response.read()
        return json.loads(data.decode("utf-8")) if len(data) > 0 else {}

    def create_meter(self, meter: Meter) -> dict:
        """
        Creates a new meter.

        Args:
            meter (Meter): The meter to create.

        Returns:
            dict: The response from the API.
        """
        body = meter.model_dump_json()
        self.conn.request("POST", self.meter_endpoint, body, self.headers)

        return self.handle_response()

    def delete_meter(self, meter_id_or_slug: str) -> dict:
        """
        Deletes a meter by its ID or slug.
        Args:
            meter_id_or_slug (str): The ID or slug of the meter to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.meter_endpoint}/{meter_id_or_slug}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def create_customer(self, customer: Customer) -> dict:
        """
        Creates a new customer.

        Args:
            customer (Customer): The customer to create.

        Returns:
            dict: The response from the API.
        """
        body = customer.model_dump_json()
        self.conn.request("POST", self.customer_endpoint, body, self.headers)

        return self.handle_response()

    def delete_customer(self, customer_id_or_key: str) -> dict:
        """
        Deletes a customer by its ID.
        Args:
            customer_id_or_key (str): The ID of the customer to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.customer_endpoint}/{customer_id_or_key}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def ingest_event(self, event: Event) -> dict:
        """
        Ingests an event.

        Args:
            event (Even): The event to ingest.

        Returns:
            dict: The response from the API.
        """
        body = event.model_dump_json()
        self.conn.request("POST", self.event_endpoint, body, self.headers)

        return self.handle_response()

    def create_plan(self, plan: Plan) -> dict:
        """
        Creates a new plan.

        Args:
            plan (Plan): The plan to create.

        Returns:
            dict: The response from the API.
        """
        body = plan.model_dump_json()
        self.conn.request("POST", self.plan_endpoint, body, self.headers)

        return self.handle_response()

    def publish_plan(self, plan_id_or_key: str) -> dict:
        """
        Publishes a plan by its ID or key.
        Args:
            plan_id_or_key (str): The ID or key of the plan to publish.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.plan_endpoint}/{plan_id_or_key}/publish"
        self.conn.request("POST", endpoint, None, self.headers)

        return self.handle_response()

    def delete_plan(self, plan_id_or_key: str) -> dict:
        """
        Deletes a plan by its ID or key.
        Args:
            plan_id_or_key (str): The ID or key of the plan to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.plan_endpoint}/{plan_id_or_key}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def create_feature(self, feature: Feature) -> dict:
        """
        Creates a new feature.

        Args:
            feature (Feature): The feature to create.

        Returns:
            dict: The response from the API.
        """
        body = feature.model_dump_json()
        self.conn.request("POST", self.feature_endpoint, body, self.headers)

        return self.handle_response()

    def delete_feature(self, feature_id_or_key: str) -> dict:
        """
        Deletes a feature by its ID or key.
        Args:
            feature_id_or_key (str): The ID or key of the feature to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.feature_endpoint}/{feature_id_or_key}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def create_entitlement(
        self, entitlement_template: EntitlementTemplate, customer_id_or_key: str
    ) -> dict:
        """
        Creates a new entitlement template.

        Args:
            entitlement_template (EntitlementTemplate): The entitlement template to create.

        Returns:
            dict: The response from the API.
        """
        body = entitlement_template.model_dump_json()
        self.conn.request(
            "POST",
            f"{self.subject_endpoint}/{customer_id_or_key}/entitlements",
            body,
            self.headers,
        )

        return self.handle_response()

    def delete_entitlement(
        self, entitlement_id_or_key: str, customer_id_or_key: str
    ) -> dict:
        """
        Deletes an entitlement by its ID or key.
        Args:
            entitlement_id_or_key (str): The ID or key of the entitlement to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.subject_endpoint}/{customer_id_or_key}/entitlements/{entitlement_id_or_key}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def create_subscription(self, subscription: Subscription) -> dict:
        """
        Creates a new subscription.

        Args:
            subscription (Subscription): The subscription to create.

        Returns:
            dict: The response from the API.
        """
        body = subscription.model_dump_json()
        self.conn.request("POST", self.subscription_endpoint, body, self.headers)
        return self.handle_response()

    def delete_subscription(self, subscription_id_or_key: str) -> dict:
        """
        Deletes a subscription by its ID or key.
        Args:
            subscription_id_or_key (str): The ID or key of the subscription to delete.
        Returns:
            dict: The response from the API.
        """
        endpoint = f"{self.subscription_endpoint}/{subscription_id_or_key}"
        self.conn.request("DELETE", endpoint, None, self.headers)

        return self.handle_response()

    def close(self):
        """
        Closes the connection to the API.
        """
        self.conn.close()
