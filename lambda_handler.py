# Entrypoint

# This file contains is the main entrypoint for the lambda function (the handler).
# It receives events from a Contact Lens Kinesis Stream through an Event Brdige Pipe.
# Depending on the `EventType` of the event, it will call different functions to process the data.
# The `handleStart` function will create a call in the database.
# The `handleSegments` function will process the segments of the call and create chunks in the database.
# The `handleCompleted` function will mark the call as completed in the database (pending).

# Alejandro Arouesty, Samuel Acevedo, Joaquín Badillo
# 2024-05-04

import base64
import json
import logging

import api
from events import chunkify

logger = logging.getLogger()

def handleStart(data):
  res = api.create_call(data.get('ContactId'))
  if res is None:
    logger.error('Failed to create call')

def handleSegments(data):
  chunks = chunkify(data)
  for chunk in chunks:
    res = api.create_chunk(
      chunk['callId'],
      chunk.get('sentiment', 'UNDEFINED'), 
      chunk['content'],
    )

    if res is None:
      logger.error('Failed to send data')

def handleCompleted(data):
  pass

def handler(event, context):
  for record in event:
    payload = base64.b64decode(record['data']).decode('utf-8')
    data = json.loads(payload)
    print(data)
    event_type = data.get('EventType')

    if event_type == 'STARTED':
      handleStart(data)
    elif event_type == 'SEGMENTS':
      handleSegments(data)
    elif event_type == 'COMPLETED':
      handleCompleted(data)