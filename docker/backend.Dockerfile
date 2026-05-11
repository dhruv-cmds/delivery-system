FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Development
CMD [ "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]

# Production
# CMD [ "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4" ]