FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MPLCONFIGDIR=/tmp/matplotlib

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY CareerLinkup CareerLinkup

# The SQLite database lives in /app/instance; mount a volume there to keep it.
RUN useradd --create-home app && mkdir -p instance && chown -R app instance CareerLinkup/static
USER app

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "main:app"]
