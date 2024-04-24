import os
import random
import time
import boto3
from boto3.dynamodb.conditions import Key


os.environ['AWS_ACCESS_KEY_ID'] = 'ASIAW3MEABTPXILZXFUG'
os.environ['AWS_SECRET_ACCESS_KEY'] = '3vb6GT/YEK4FJ0PWL34M6dOp3z5Z3oM/Rd74Zt82'
os.environ['AWS_SESSION_TOKEN'] = 'IQoJb3JpZ2luX2VjEHsaCXVzLXdlc3QtMiJHMEUCIB5lqDhGxSBkRF/F8IGq41SUvxN/kjkI+35hnY5AqK8WAiEAmdA0R++H7GxPDT0HxOpqnpx2L6YzQM6HDvs8/IlVnnUqvgIItP//////////ARAAGgw0NzExMTI2MTcxODMiDAYyQALR1ST6cCYj3iqSAoOKaQU11odv/WQa+dkY0TmA/uC3CSv9Dp9TtWfR+gUpuy39lb1vv2JoG6OHdR6CyFEl3IG4yyNqYbcYQfG3OeU24FwRFhzOjpPFtXnlwkOEaN6rW+F5od5ZPLz4A/2C2K0hf19zHdtpuY9Dyy5j5tBHYlVb43UusXYN+Y+5KXYU8FV1XiFFuv1TcLc9C7WoXDh3+Sumb9hmmaPFI+mAvF4vj8qr1zXTR4J8DPJgf2447oMv2f6ZJt+fVYhUwRL16WrcvTprEMtYQNbWAgXXU+9x546qox0q6EfFiedCCIzfI/SCCRc+wo89XAwdrvLzFGozGvvIBTZHvyRxJhUjjpWiI4nQkVVXwDOFvPcyIlFOO5swktv3sAY6nQGPqp/ZP/C4qN0mW50KExmWRIdEYhsRrgpOH8uzTjmAE1N94If5ip/Imy0yVuUJSFN/bnagDoNAnnsBwhPujwJlSEtCRdcthgOmcFTKyDt1w1565roYHAqXoiK9oFX+UwL6OWeSOUk04964f7mY6QWVR0smlXUy5/pnQG2/jQXGYbSZhpHlc8nanlIs5t6mjrdcrObmKGoZcKVLaveJ'
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
os.environ['DYNAMODB_TABLE_NAME'] = 'call_chunks'


dynamodb = boto3.resource(
    'dynamodb',
    region_name=os.getenv('AWS_DEFAULT_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    aws_session_token=os.getenv('AWS_SESSION_TOKEN')
)
table = dynamodb.Table(os.getenv('DYNAMODB_TABLE_NAME'))


def generate_data():

    return {
        'call_id': random.randint(1000, 9999),
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
        'sentiment': random.choice(['positive', 'neutral', 'negative'])
        
    }

def chunk_data(data, chunk_size):
    
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

def send_to_dynamodb(chunks):

    try:
        for chunk in chunks:
            with table.batch_writer() as batch:
                for item in chunk:
                    batch.put_item(Item=item)
            print("Chunk sent to DynamoDB")
    except Exception as e:
        print(f"Failed to send chunk: {e}")


if __name__ == "__main__":
    data_stream = [generate_data() for _ in range(10)] 
    chunks = list(chunk_data(data_stream, 3)) 
    send_to_dynamodb(chunks)
