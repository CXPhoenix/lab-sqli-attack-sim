FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy application code
COPY src src

# Run the application
# Use uv run to execute in the virtual environment created by uv sync
CMD ["uv", "run", "uvicorn"]
