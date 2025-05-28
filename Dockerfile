# Use Python 3.9 slim as base image
FROM python:3.9-slim

# Set environment variables
# PYTHONDONTWRITEBYTECODE and PYTHONUNBUFFERED are good practices for containers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# WORKDIR for application
WORKDIR /app

# Install system dependencies (if any beyond basic python)
# Example: RUN apt-get update && apt-get install -y --no-install-recommends some-package && apt-get clean && rm -rf /var/lib/apt/lists/*

# Create a non-root user and group for security
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on (ensure this matches your app's configuration)
# This should be set by Render's PORT environment variable, but good to document
# EXPOSE $PORT 

# Health check (optional but recommended for Render)
# Render uses this to determine if your service is healthy.
# Adjust the CMD to match your application\'s health check endpoint.
# HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \\
#    CMD curl -f http://localhost:${PORT}/health || exit 1
# Note: Render injects the PORT environment variable.

# Command to run the application
# Render will use the command specified in its service settings.
# This CMD is a fallback or for local testing.
# Ensure your Procfile or Render start command uses gunicorn or similar.
# Example: CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:$PORT"]
# For your project, it seems you use `python app.py` or `sh run.sh`
# If run.sh starts gunicorn, that's fine.
CMD ["sh", "run.sh"]
