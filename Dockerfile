# Build stage
FROM python:3.12-alpine as builder

# Install build dependencies
RUN apk add --no-cache \
    build-base \
    file-dev \
    python3-dev \
    libffi-dev

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.12-alpine

# Install runtime dependencies
RUN apk add --no-cache \
    tesseract-ocr \
    file \
    libmagic

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ src/

# Create non-root user
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.app:app", \
    "--host", "0.0.0.0", \
    "--port", "8000", \
    "--workers", "4", \
    "--loop", "uvloop", \
    "--limit-concurrency", "1000", \
    "--timeout-keep-alive", "30", \
    "--access-log"] 