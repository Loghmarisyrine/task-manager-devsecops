FROM python:3.12-slim

# Dépendances système minimales pour psycopg2
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

# Durcissement : ne pas exécuter en root
RUN addgroup --system django && adduser --system --ingroup django django \
    && chown -R django:django /app
USER django

EXPOSE 8000

CMD ["gunicorn", "taskmanager.wsgi:application", "--bind", "0.0.0.0:8000"]
