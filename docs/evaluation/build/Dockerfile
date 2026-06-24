# Evaluation Harness image — serves the API, the migration runner, and the
# statistical-engine job from one artifact. Build context = docs/evaluation/build.
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System deps: libpq for psycopg2-binary is bundled, but keep curl for probes.
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Install the package (with all runtime extras) first for layer caching.
COPY harness/pyproject.toml harness/README.md ./harness/
COPY harness/eval_harness ./harness/eval_harness
RUN pip install "./harness[all]"

# Migration runner + SQL (migrations and seed).
COPY db ./db

# Run as a non-root user (harness is isolated from production — spec §9.1).
RUN useradd --create-home --uid 10001 harness && chown -R harness:harness /app
USER harness

EXPOSE 8080

# Default: serve the Ingest + Review API. Overridden by the migrate/stats services.
CMD ["uvicorn", "eval_harness.api.app:app", "--host", "0.0.0.0", "--port", "8080"]
