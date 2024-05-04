# chunks_to_dynamo
Code for lambda that will receive calls and send them to our dyanmo db via graphql 

## Local Usage (without docker)
Create a python virtual environment to avoid conflicts
```bash
python -m venv venv
```

Activate venv
```bash
source ./venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

Now you can try the code out by running in interactive mode
```bash
python -i lambda_handler.py
```

## Using with Docker
Build the image (we will run it in the bg for convenience)
```bash
docker build -t jiva/chunks . &
```

In the meantime we will create a `.env` file (you can also pass the environment variables directly if you want to)
```env
API_URL=<your_api_url>
API_KEY=<your_api_key>
```

Hopefully the docker image is built now. Let's run it (we will use port 9000 for the host)
```bash
docker run -dp 9000:8080 --env-file=/path/to/.env jiva/chunks
```

You should be able to send requests to `http://localhost:9000/2015-03-31/functions/function/invocations` now.
