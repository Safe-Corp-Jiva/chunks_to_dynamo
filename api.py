import os

from datetime import datetime, timezone
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

if not API_URL or not API_KEY:
  raise Exception('API_URL and API_KEY must be set in the environment')

transport = RequestsHTTPTransport(
  url=API_URL,
  headers={'x-api-key': API_KEY}
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Mutations & Queries
_create_metrics = gql("""
  mutation CreateMetric($createdAt: AWSDateTime!, $updatedAt: AWSDateTime!) {
    createMetrics(input: {id: $id, createdAt: $createdAt, updatedAt: $updatedAt}) {
      id
    }
  }"""
)

_create_call = gql("""
  mutation CreateCall($id: ID!, $createdAt: AWSDateTime!, $callMetricsId: ID!) {
    createCall(
      input: {id: $id, createdAt: $createdAt, callMetricsId: $callMetricsId, status: STARTED}
    ) {
      id
    }
  }"""
)

_create_chunk = gql("""
  mutation CreateChunk($sentiment: Sentiment, $content: ChunkContentInput, $callId: ID!) {
    createChunk(input: {sentiment: $sentiment, content: $content, callId: $callId}) {
      id
      sentiment
      content {
        role
        text
      }
      callId
    }
  }"""
)

# Executions
def create_metrics():
  try:
    response = client.execute(_create_metrics, variable_values={
      'createdAt': datetime.now(timezone.utc).isoformat(),
      'updatedAt': datetime.now(timezone.utc).isoformat()
    })
    return response['createMetrics']['id']
  except Exception as e:
    print(e)
    return None

def create_call(id):
  try:
    response = client.execute(_create_call, variable_values={
      'id': id,
      'createdAt': datetime.now(timezone.utc).isoformat(),
      'callMetricsId': create_metrics()
    })
    return response['createCall']['id']
  except Exception as e:
    print(e)
    return None

def create_chunk(contactId, sentiment, content):
  try:
    response = client.execute(_create_chunk, variable_values={
      'id': id,
      'sentiment': sentiment,
      'content': content,
      'callId': create_call(contactId)
    })
    return response['createChunk']['id']
  except Exception as e:
    print(e)
    return None
