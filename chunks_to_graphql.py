import os
import random
import uuid
import json
import base64
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL API setup
api_url = 'https://bs64wev465c6dhsrb2k3bftfii.appsync-api.us-east-1.amazonaws.com/graphql'
api_key = 'da2-me7ie5gq4zdjzmhwiuxkg6hmbi'

transport = RequestsHTTPTransport(
    url=api_url,
    headers={'x-api-key': api_key}
)
client = Client(transport=transport, fetch_schema_from_transport=True)

# GraphQL Mutation for creating chunks
mutation = gql("""
    mutation CreateChunk($id: ID!, $sentiment: Sentiment, $content: ChunkContentInput, $callId: ID!) {
        createChunk(input: {id: $id, sentiment: $sentiment, content: $content, callId: $callId}) {
            id
            sentiment
            content {
                role
                text
            }
            callId
        }
    }
""")

# Function to process segment data into the required format
def chunkify(data):
    segments = data.get('Segments', [])
    def process_segment(segment):
        if segment.get('Transcript'):
            content = segment['Transcript']
            return {
                'callId': data.get('ContactId'),
                'content': {
                    'role': content.get('ParticipantRole'),
                    'text': content.get('Content')
                },
                'sentiment': content.get('Sentiment')
            }
    return [process_segment(seg) for seg in segments if seg.get('Transcript')]

# Function to send chunk data to the API
def send_to_amplify(chunks):
    try:
        for chunk in chunks:
            response = client.execute(mutation, variable_values={
                'id': str(uuid.uuid4()),
                'sentiment': chunk['sentiment'],
                'content': chunk['content'],
                'callId': chunk['callId']
            })
            print("Data sent to Amplify:", response)
    except Exception as e:
        print(f"Failed to send data: {e}")

# AWS Lambda handler function
def handler(event, context):
    data = json.loads(base64.b64decode(event[0]['data']).decode('utf-8'))
    event_type = data.get('EventType')
    if event_type == 'STARTED':
        print('Call started')
    elif event_type == 'SEGMENTS':
        chunks = chunkify(data)
        send_to_amplify(chunks)
    elif event_type == 'COMPLETED':
        print('Call completed')
