# Dockerfile

# Uses the AWS Lambda base image for Python 3.10
# Installs the dependencies from the requirements.txt file and
# sets the handler function from the lambda_handler file as the entrypoint

# Joaquín Badillo
# 2024-05-04

FROM public.ecr.aws/lambda/python:3.10
LABEL org.opencontainers.image.authors="joaquin.badillo.g@gmail.com"

ENV PRODUCTION true

COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install --no-cache-dir -r requirements.txt

COPY . ${LAMBDA_TASK_ROOT}

CMD ["lambda_handler.handler"]