FROM python:3.13-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

ENV DEBIAN_FRONTEND=noninteractive
ARG ROUTER_IP=192.168.3.2
ENV ROUTER_IP=${ROUTER_IP}

# Install system dependencies (curl for healthcheck/wait script, iproute2 for routing)
RUN apt-get update && apt-get install -y curl iproute2 && rm -rf /var/lib/apt/lists/*

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set working directory
WORKDIR /app

# Copy project files
COPY pyproject.toml .
COPY uv.lock .


# Install dependencies
RUN uv sync --frozen --no-install-project

# Copy source code
COPY src src

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Run the application
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
