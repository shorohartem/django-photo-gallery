from prometheus_client import Counter, Histogram, Gauge
import time

REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram('http_request_duration_seconds',
                             'Request duration',
                             ['method', 'endpoint'])


DB_CONNECTION_GAUGE = Gauge('db_connection_status', 'Status of database connection (1=up, 0=down)')

def check_db_connection():
    from django.db import connection
    try:
        connection.ensure_connection()
        DB_CONNECTION_GAUGE.set(1)
    except Exception:
        DB_CONNECTION_GAUGE.set(0)