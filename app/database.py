import psycopg2
from psycopg2.extras import RealDictCursor

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Anurag@604', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection successful!")
        break
    except Exception as e:
        print(f"Database connection failed: {e}")