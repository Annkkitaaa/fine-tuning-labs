FROM python:3.9-slim

WORKDIR /app

# Increase pip timeout
ENV PIP_DEFAULT_TIMEOUT=1000

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]