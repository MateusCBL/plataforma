FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc libpq-dev --no-install-recommends \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY server.py .

ENV LISTEN_PORT=8001
ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=clientsdb
ENV DB_USER=postgres
ENV DB_PASS=postgres

EXPOSE 8001

CMD ["python", "server.py"]

RUN chmod +x /app/run-tests.sh && chmod +x /app/test-code.sh