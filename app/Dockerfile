# Container 2: The Mock API Server
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000 so other containers can reach us
EXPOSE 5000

CMD ["python", "server.py"]
