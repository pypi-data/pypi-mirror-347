import unittest

from lmms_lab_meter.api.client import LMMsLabMeterClient
from lmms_lab_meter.protocols import Customer, Event, Meter


class TestEvents(unittest.TestCase):
    def test_events(self):
        client = LMMsLabMeterClient()
        # Create a meter first
        meter = Meter(
            aggregation="SUM",
            eventType="prompt",
            slug="tokens_total",
            windowSize="MINUTE",
            description="AI Token Usage",
            groupBy={"model": "$.model", "type": "$.type"},
            id="1234",
            valueProperty="$.tokens",
        )

        client.create_meter(meter)

        payload = {
            "specversion": "1.0",
            "type": "prompt",
            "id": "00002",
            "time": "2025-05-12T07:28:11.557Z",
            "source": "my-app",
            "subject": "customer-1",
            "data": {"tokens": "1000", "model": "gpt-4-1106-preview", "type": "input"},
        }
        event = Event(**payload)

        # Create an event
        response = client.ingest_event(event)
        print(response)

        client.close()


if __name__ == "__main__":
    unittest.main()
