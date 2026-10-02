# ==========================================
# Production Dockerfile for Hostel Management Backend
# Base: Python 3.11-slim with security hardening
# ==========================================

FROM python:3.11-slim AS runtime

# Set environment variables to optimize Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

# Install curl for healthcheck monitoring and clean up apt cache
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a non-root dedicated application user for security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -s /bin/bash -m appuser

# Copy application source code with proper ownership
COPY --chown=appuser:appgroup app /app/app

# Switch to non-root user
USER appuser

# Expose FastAPI backend port
EXPOSE 8000

# Container Healthcheck verifying /health endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Execute FastAPI via Uvicorn ASGI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
