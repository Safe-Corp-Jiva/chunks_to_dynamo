import uuid
import base64
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from events import chunkify

# GraphQL client
api_url = 'https://bs64wev465c6dhsrb2k3bftfii.appsync-api.us-east-1.amazonaws.com/graphql'
api_key = 'da2-me7ie5gq4zdjzmhwiuxkg6hmbi'
transport = RequestsHTTPTransport(url=api_url, headers={'x-api-key': api_key})
client = Client(transport=transport, fetch_schema_from_transport=True)

# GraphQL mutation
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

def send_to_amplify(chunks):
    for chunk in chunks:
        response = client.execute(mutation, variable_values={
            'id': str(uuid.uuid4()),
            'sentiment': chunk['sentiment'],
            'content': chunk['content'],
            'callId': chunk['callId']
        })
        print("Data sent to Amplify:", response)

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

