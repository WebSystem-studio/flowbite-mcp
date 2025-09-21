# Flowbite MCP Server Docker Image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set Python path
ENV PYTHONPATH=/app

# Create data directory
RUN mkdir -p data/components data/examples

# Set proper permissions
RUN chmod +x src/server.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import src.server; print('OK')" || exit 1

# Expose port (if running HTTP server)
EXPOSE 8000

# Run the MCP server
CMD ["python", "-m", "src.server"]