# Multi-stage build for production-ready image

# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user early (before copying dependencies)
RUN useradd -m -u 1000 appuser

# Copy Python dependencies from builder to user-accessible location
COPY --from=builder /root/.local /home/appuser/.local

# Copy application code
COPY .env ./
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY alembic/ ./alembic/
COPY alembic.ini ./

# Change ownership to appuser
RUN chown -R appuser:appuser /app /home/appuser/.local

# Switch to non-root user
USER appuser

# Make sure scripts are on path for appuser
ENV PATH=/home/appuser/.local/bin:$PATH

# Expose port (7860 is HF Spaces default, 8000 for other deployments)
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:7860/health')" || exit 1

# Run application on port 7860 for HF Spaces
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
