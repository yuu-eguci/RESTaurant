FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

# NOTE: venv は /app の外に置きます。 compose で /app を bind mount しても消えないようにするためです。
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    UV_FROZEN=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --no-install-project

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py migrate && uv run python manage.py runserver 0.0.0.0:8000"]
