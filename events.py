def chunkify(data):
  segments = data.get('Segments')
  def process_segment(segment):
    content = sentiment = None
    if segment.get('Transcript'):
      content = segment.get('Transcript')
      sentiment = content.get('Sentiment')
      content = f"{content.get('ParticipantRole')}: {content.get('Content')}"
    elif segment.get('Utterance'):
      content = segment.get('Utterance')
      content = f"{content.get('ParticipantRole')}: {content.get('PartialContent')}"
    return {
      'callId': data.get('ContactId'),
      'content': content,
      'sentiment': sentiment
    }
  
  return list(map(process_segment, segments))
