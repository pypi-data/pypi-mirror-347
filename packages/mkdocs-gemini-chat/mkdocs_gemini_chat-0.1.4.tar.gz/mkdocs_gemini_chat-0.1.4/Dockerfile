FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only the files needed for installation
COPY setup.py pyproject.toml MANIFEST.in ./
COPY README.md LICENSE ./
COPY mkdocs_gemini_chat ./mkdocs_gemini_chat

# Install the package
RUN pip install --no-cache-dir -e .

# Install production dependencies
RUN pip install --no-cache-dir gunicorn uvicorn

# Create non-root user
RUN useradd -m -u 1000 appuser
USER appuser

# Expose the port
EXPOSE 8000

# Run the server
CMD ["gunicorn", "mkdocs_gemini_chat.server:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"] 