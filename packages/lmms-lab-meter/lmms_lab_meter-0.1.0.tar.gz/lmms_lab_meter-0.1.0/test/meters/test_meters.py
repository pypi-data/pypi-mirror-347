import unittest

from lmms_lab_meter.api.client import LMMsLabMeterClient
from lmms_lab_meter.protocols import Meter


class TestMeters(unittest.TestCase):
    def test_meters(self):
        client = LMMsLabMeterClient()
        meter = Meter(
            aggregation="SUM",
            eventType="test_event",
            slug="test_meter",
            windowSize="MINUTE",
            description="This is a test meter.",
            groupBy={"group": "$.group"},
            valueProperty="$.value",
        )
        response = client.create_meter(meter)
        print(response)
        self.assertIn("id", response)
        self.assertIn("slug", response)

        # Clean up by deleting the created meter
        meter_id = response["id"]
        delete_response = client.delete_meter(meter_id)
        print(delete_response)
        client.close()


if __name__ == "__main__":
    unittest.main()
