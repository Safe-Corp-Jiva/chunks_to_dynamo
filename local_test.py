import json
import base64

# Sample data structure that might be coming from Kinesis
sample_data = {
    "EventType": "SEGMENTS",
    "ContactId": "12345",
    "Segments": [
        {
            "Transcript": {
                "ParticipantRole": "CUSTOMER",
                "Content": "Hello, I need help with my account.",
                "Sentiment": "NEUTRAL"
            }
        },
        {
            "Transcript": {
                "ParticipantRole": "AGENT",
                "Content": "Of course, I can help you with that.",
                "Sentiment": "POSITIVE"
            }
        }
    ]
}

# Encoding the sample data as base64, similar to how Kinesis would deliver it
encoded_data = base64.b64encode(json.dumps(sample_data).encode('utf-8')).decode('utf-8')

# Creating the mock event that Lambda would receive from Kinesis
mock_event = [
    {
        'data': encoded_data,
        'eventSource': 'aws:kinesis',
        'eventVersion': '1.0',
        'eventID': 'shardId-000000000000:49590338271490256608559692538361571095921575989136588898',
        'eventName': 'aws:kinesis:record',
        'invokeIdentityArn': 'arn:aws:iam::account-id:role/test-role',
        'awsRegion': 'us-east-1',
        'eventSourceARN': 'arn:aws:kinesis:us-east-1:account-id:stream/test-stream',
        'kinesisSchemaVersion': '1.0',
        'partitionKey': 'partitionKey-3',
        'sequenceNumber': '49590338271490256608559692538361571095921575989136588898',
        'approximateArrivalTimestamp': 1428537600
    }
]

# Example function to simulate the handler being called locally
def local_test():
    context = None  # Context is often not needed for local testing
    from lambda_handler import handler  # Ensure lambda_handler.py has all dependencies and correct imports
    handler(mock_event, context)

# Run the local test function
if __name__ == "__main__":
    local_test()
