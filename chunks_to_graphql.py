import os
import random
import uuid
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


api_url = 'https://bs64wev465c6dhsrb2k3bftfii.appsync-api.us-east-1.amazonaws.com/graphql'
api_key = 'da2-me7ie5gq4zdjzmhwiuxkg6hmbi'

transport = RequestsHTTPTransport(
    url=api_url,
    headers={'x-api-key': api_key}
)
client = Client(transport=transport, fetch_schema_from_transport=True)


mutation = gql("""
    mutation CreateChunk($id: ID!, $sentiment: Float, $text: String, $callId: ID!) {
        createChunk(input: {id: $id, sentiment: $sentiment, text: $text, callId: $callId}) {
            id
            sentiment
            text
            callId
        }
    }
""")

def generate_data():

    return {
        'callId': str(uuid.uuid4()), 
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...', 
        'sentiment': random.uniform(0, 1) 
    }

def chunk_data(data, chunk_size):

    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def send_to_amplify(chunks):

    try:
        for chunk in chunks:
            for item in chunk:
                response = client.execute(mutation, variable_values={
                    'id': str(uuid.uuid4()),  
                    'sentiment': item['sentiment'],
                    'text': item['text'], 
                    'callId': item['callId']  
                })
                print("Data sent to Amplify:", response)
    except Exception as e:
        print(f"Failed to send data: {e}")

if __name__ == "__main__":
    data_stream = [generate_data() for _ in range(3)]  
    chunks = list(chunk_data(data_stream, 3)) 
    send_to_amplify(chunks)  
