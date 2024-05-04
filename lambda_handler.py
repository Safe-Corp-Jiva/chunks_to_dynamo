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