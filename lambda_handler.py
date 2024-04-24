import base64
import json

from events import chunkify

def handler(event, context):
  data = json.loads(base64.b64decode(event[0]['data']).decode('utf-8'))
  event_type = data.get('EventType')
  if event_type == 'STARTED':
    print('Call started')
    return
  elif event_type == 'SEGMENTS':
    c = chunkify(data)
    print(c)
    return
  elif event_type == 'COMPLETED':
    print(event_type)
    return