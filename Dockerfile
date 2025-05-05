FROM python:3.9-slim
WORKDIR /app

# Install our Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all our code and pre-built data/index.json
COPY . /app/

# Cloud Run uses port 8080 by default
ENV PORT=8080
EXPOSE 8080

# Use gunicorn in production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "0", "main:app"]
