# Entrypoint

# This file contains the main entrypoint for the lambda (the `handler` function).
# It receives events from a Contact Lens Kinesis Stream through an Event Brdige Pipe.
# Depending on the `EventType`, it will call different functions to process the data.
# The `handleStart` function will create a call in the database.
# The `handleSegments` function will process the segments of the call and create chunks in the database.
# The `handleCompleted` function will mark the call as completed in the database (pending).

# Alejandro Arouesty, Samuel Acevedo, Joaquín Badillo
# 2024-05-16

import base64, json, logging, os, requests, threading

import api
from events import chunkify

logger = logging.getLogger()

def handleStart(data):
  res = api.create_call(data.get('ContactId'), data.get('InstanceId'))
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

def fireAndForget(data):
  requests.post(url=os.environ.get("PROCESS_RESULTS"), json={
    "callId": data.get('ContactId'),
  })

def handleCompleted(data):
  threading.Thread(target=fireAndForget, args=(data,)).start()
  res = api.update_call(data.get('ContactId'), 'FINALIZED')
  if res is None:
    logger.error('Failed to update call status')

def handler(event, context):
  print("Got event:")
  print(event, end="\n\n")

  records = event.get('Records', [])
  for record in records:
    payload = record.get('kinesis', dict()).get('data')
    if payload is None:
      logger.error('No kinesis payload')
      continue
    payload = base64.b64decode(payload).decode('utf-8')
    data = json.loads(payload)
    event_type = data.get('EventType')

    if event_type == 'STARTED':
      handleStart(data)
    elif event_type == 'SEGMENTS':
      handleSegments(data)
    elif event_type == 'COMPLETED':
      handleCompleted(data)