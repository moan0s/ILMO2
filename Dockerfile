
# Install Python dependencies in this layer
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim AS python_builder

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN ls
# Copy dependency metadata first so Docker can cache them.
COPY pyproject.toml ./
COPY uv.lock ./
COPY README.md ./

# Install production dependencies into /app/.venv.
# --locked ensures that uv.lock is used
# --no-dev excludes optional development dependencies like pytest

RUN uv sync --locked --no-dev --no-install-project

COPY src ./src

# Install the project itself
RUN uv sync --locked --no-dev


# Stage 2: Build css and assets
FROM node:24-slim AS css_builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build


# Runtime
FROM python:3.14-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PATH="/app/.venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends gosu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy the complete uv-created virtual environment.
COPY --from=python_builder /app/.venv /app/.venv

# Copy built frontend/static assets.
COPY --from=css_builder /app/src/library/static/library/css/main.css \
    /app/library/static/library/css/main.css

COPY --from=css_builder /app/src/library/static/library/webfonts \
    /app/library/static/library/webfonts

# Copy application source
COPY src .

COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]