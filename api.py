# `api.py`

# Manages AppSync operations (GraphQL API Calls)

# Requires API_URL, API_KEY and AWS Credentials to be set in the environment
# e.g.
# export API_URL=https://<api-id>.appsync-api.<region>.amazonaws.com/graphql
# export API_KEY=<api-key>
# export AWS_ACCESS_KEY=<access-key>
# export AWS_SECRET_ACCESS_KEY=<secret-access-key>

# Alejandro Arouesty, Samuel Acevedo, Joaquín Badillo
# 2024-05-16

import boto3
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

connect = boto3.client(
  'connect',
  region_name='us-east-1',
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

# Mutations & Queries
_create_metrics_mut = gql("""
  mutation CreateMetric {
    createMetric(input: {}) {
      id
    }
  }"""
)

_create_call_mut = gql("""
  mutation CreateCall($id: ID!, $callMetricsId: ID!, $callAgentId: ID!, $callQueueId: ID!, $callCallerId: ID!) {
    createCall(
      input: {id: $id, callMetricsId: $callMetricsId, status: STARTED, callAgentId: $callAgentId, callQueueId: $callQueueId, callCallerId: $callCallerId}
    ) {
      id
      createdAt
      status
      updatedAt
      metrics {
        id
        length
        waittime
        createdAt
        updatedAt
      }
      agent {
        username
      }
      queue {
        name
      }
      caller {
        id
        name
      }
    }
  }"""
)

_update_call_mut = gql("""
  mutation UpdateCall($id: ID!, $status: CallStatus!) {
    updateCall(
      input: {id: $id, status: $status}
    ) {
      id
      createdAt
      status
      updatedAt
      metrics {
        id
        length
        waittime
        createdAt
        updatedAt
      }
      agent {
        username
      }
      queue {
        name
      }
      caller {
        id
      }
    }
  }"""
)
                       

_create_chunk_mut = gql("""
  mutation CreateChunk($sentiment: Sentiment, $content: ChunkContentInput, $callId: ID!) {
    createChunk(
      input: {sentiment: $sentiment, content: $content, callId: $callId}
    ) {
      id
      content {
        role
        text
      }
      callId
      sentiment
      createdAt
      updatedAt
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

def create_call(contactId, instanceId):
  try:
    metricsId = _create_metrics()
    if metricsId is None:
      return None
    
    contactData = connect.describe_contact(
      InstanceId=instanceId,
      ContactId=contactId
    )

    agentId = contactData['Contact']['AgentInfo']['Id']
    queueId = contactData['Contact']['QueueInfo']['Id']

    response = client.execute(_create_call_mut, variable_values={
      'id': contactId,
      'callMetricsId': metricsId,
      'callAgentId': agentId,
      'callQueueId': queueId,
      'callCallerId': '+525513888043'
    })

    return response['createCall']['id']
  except Exception as e:
    logger.error(f"Failed to create call: {e}")
    return None
  
def update_call(id, status):
  try:
    response = client.execute(_update_call_mut, variable_values={
      'id': id,
      'status': status
    })
    return response['updateCall']['id']
  except Exception as e:
    logger.error(f"Failed to update call: {e}")
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
