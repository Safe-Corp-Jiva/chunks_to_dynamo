# `events.py`

# Contains utilities to process decoded data from the Kinesis stream

# Alejandro Arouesty, Joaquín Badillo
# 2024-05-14

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
