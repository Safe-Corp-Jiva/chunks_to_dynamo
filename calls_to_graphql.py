import os
import uuid
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime, timezone

# I didn't knew how to handle this variables using the os package
api_url = 'https://bs64wev465c6dhsrb2k3bftfii.appsync-api.us-east-1.amazonaws.com/graphql'
api_key = 'da2-me7ie5gq4zdjzmhwiuxkg6hmbi'

transport = RequestsHTTPTransport(
    url=api_url,
    headers={'x-api-key': api_key}
)
client = Client(transport=transport, fetch_schema_from_transport=True)


# This is the huge mutation
mutation = gql("""
    mutation CreateCall($id: ID!, $transcript: S3ObjectInput, $audio: S3ObjectInput, $createdAt: AWSDateTime!, $callMetricsId: ID!, $callCallerId: ID!) {
  createCall(
    input: {id: $id, audio: $audio, createdAt: $createdAt, callMetricsId: $callMetricsId, status: STARTED, callCallerId: $callCallerId, transcript: $transcript}
  ) {
    id
    transcript {
      key
      bucketId
    }
    createdAt
    updatedAt
    callCallerId
    callMetricsId
    status
    audio {
      bucketId
      key
    }
    metrics {
      createdAt
      length
      id
      updatedAt
      waittime
    }
    caller {
      createdAt
      id
      phone
      updatedAt
    }
    chunks {
      items {
        callId
        createdAt
        id
        sentiment
        updatedAt
        content {
          role
          text
        }
      }
    }
  }
}

""")

def generateData():
    data = [{
        'callCallerId': str(uuid.uuid4()), # Change to Amazon Connect Data
        'callMetricsId': "b067311f-7504-4254-ae09-c3bdb3be4b3f", # Here we should instantiate the Metrics table and here the id of that one created
        "transcript": { "key": "pruebitaTranscript.txt","bucketId": "7128412912" }, # Here the same as above but with the S3Object
        "audio": { "key": "PruebitaAudio.mp3", "bucketId": "7129382100" }, # Here the same as above but with the S3Object
        "createdAt" : datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), # Idk if you like this format, it was accepted by Amplify
        "updatedAt" : datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    }]
    return data
    

# I managed this data like this but if you want to change let me know
def send_to_amplify(data):
    try:
        for item in data:
            response = client.execute(mutation, variable_values={
                'id': str(uuid.uuid4()),
                'transcript': item['transcript'],
                'audio': item['audio'],
                'createdAt': item['createdAt'],
                'updatedAt': item['updatedAt'],
                'callMetricsId': item['callMetricsId'],
                'callCallerId': item['callCallerId'],
            })
            print("Data sent to Amplify:", response)
    except Exception as e:
        print(f"Failed to send data: {e}")
        
if __name__ == "__main__":
    data_stream = generateData()
    send_to_amplify(data_stream)