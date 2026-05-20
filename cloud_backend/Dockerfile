FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all python files
COPY *.py ./

# Proto files will need to be compiled. We can do this in the Dockerfile or beforehand.
# Let's do it in the Dockerfile for self-containment.
# But we need proto/ folder context. It's better to build context from the root repo,
# or we compile stubs before building the docker image.
# For simplicity, we assume stubs are pre-compiled and exist in cloud_backend.

CMD ["python", "main.py"]
