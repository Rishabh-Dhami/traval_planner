FROM python:3.11-slim

WORKDIR /app

COPY mcp-server/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY mcp-server/ .

EXPOSE 9000

CMD ["python", "server.py"]