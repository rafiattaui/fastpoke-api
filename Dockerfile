# Use an official lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY ./app ./app

# Expose FastAPI default port
EXPOSE 8000

# Run the app
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]