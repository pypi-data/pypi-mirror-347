import unittest

from lmms_lab_meter.api.client import LMMsLabMeterClient
from lmms_lab_meter.protocols import Customer


class TestCustomers(unittest.TestCase):
    def test_customers(self):
        client = LMMsLabMeterClient()
        customer = Customer(
            id="test_customer_id",
            name="Test Customer",
            usageAttribution={"subjectKeys": ["test_subject_key"]},
            archivedAt=None,
            billingAddress={
                "city": "Test City",
                "country": "US",
                "line1": "123 Test St",
                "line2": "Apt 4B",
                "phoneNumber": "+1234567890",
                "postalCode": "12345",
                "state": "CA",
            },
            createdAt=None,
            currency="USD",
            deletedAt=None,
            description="This is a test customer.",
            external={"stripeCustomerId": "test_stripe_customer_id"},
            metadata={},
            primaryEmail="test@xyz.com",
            timezone="UTC",
            updatedAt=None,
        )
        response = client.create_customer(customer)
        print(response)
        self.assertIn("id", response)
        self.assertIn("name", response)

        # Clean up by deleting the created customer
        customer_id = response["id"]
        delete_response = client.delete_customer(customer_id)
        print(delete_response)
        client.close()


if __name__ == "__main__":
    unittest.main()
