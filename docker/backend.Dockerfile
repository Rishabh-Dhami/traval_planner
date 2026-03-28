FROM python:3.11-slim

WORKDIR /app

# copy requirements first
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# copy backend code
COPY backend/ .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]