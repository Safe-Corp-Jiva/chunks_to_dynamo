# `api.py`

# Manages AppSync operations (GraphQL API Calls)

# Requires API_URL and API_KEY to be set in the environment
# e.g.
# export API_URL=https://<api-id>.appsync-api.<region>.amazonaws.com/graphql
# export API_KEY=<api-key>

# Alejandro Arouesty, Samuel Acevedo, Joaquín Badillo
# 2024-05-04

import logging
import os

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
_create_metrics_mut = gql("""
  mutation CreateMetric {
    createMetric(input: {}) {
      id
    }
  }"""
)

_create_call_mut = gql("""
  mutation CreateCall($id: ID!, $callMetricsId: ID!) {
    createCall(
      input: {id: $id, callMetricsId: $callMetricsId, status: STARTED}
    ) {
      id
    }
  }"""
)

_create_chunk_mut = gql("""
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
logger = logging.getLogger()

def _create_metrics():
  try:
    response = client.execute(_create_metrics_mut)
    return response['createMetric']['id']
  except Exception as e:
    logger.error(f"Failed to create metrics: {e}")
    return None

def create_call(id):
  try:
    metricsId = _create_metrics()
    if metricsId is None:
      return None
    response = client.execute(_create_call_mut, variable_values={
      'id': id,
      'callMetricsId': metricsId
    })
    return response['createCall']['id']
  except Exception as e:
    logger.error(f"Failed to create call: {e}")
    return None

def create_chunk(contactId, sentiment, content):
  try:
    response = client.execute(_create_chunk_mut, variable_values={
      'sentiment': sentiment,
      'content': content,
      'callId': contactId
    })
    logger.info(f"Created chunk: {response}")
    return response['createChunk']['id']
  except Exception as e:
    logger.error(f"Failed to create chunk: {e}")
    return None
