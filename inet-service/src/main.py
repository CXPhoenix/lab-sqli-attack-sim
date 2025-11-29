from fastapi import FastAPI, HTTPException
import mysql.connector
import os

from contextlib import asynccontextmanager
from faker import Faker

fake = Faker()


def get_db_connection():
    try:
        return mysql.connector.connect(
            host=os.getenv("DB_HOST", "mariadb"),
            user=os.getenv("DB_USER", "user"),
            password=os.getenv("DB_PASSWORD", "password"),
            database=os.getenv("DB_NAME", "sqli_lab"),
            autocommit=True,
        )
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        raise HTTPException(status_code=500, detail="Database connection error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Create items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                description TEXT
            )
        """)

        # Check if items exist
        cursor.execute("SELECT COUNT(*) FROM items")
        count = cursor.fetchone()[0]

        if count < 100:
            print("Populating items table...")
            for _ in range(100 - count):
                name = fake.word().capitalize()
                description = fake.sentence()
                cursor.execute(
                    "INSERT INTO items (name, description) VALUES (%s, %s)",
                    (name, description),
                )
            print("Items table populated.")

        # Create flags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flags (
                id INT AUTO_INCREMENT PRIMARY KEY,
                flag VARCHAR(255) NOT NULL
            )
        """)

        # Insert flag
        flag_value = os.getenv("FLAG", "ISIP{TEST_FLAG}")
        cursor.execute("DELETE FROM flags")  # Ensure only one flag exists
        cursor.execute("INSERT INTO flags (flag) VALUES (%s)", (flag_value,))
        print(f"Flag inserted: {flag_value}")

    except mysql.connector.Error as err:
        print(f"Database initialization error: {err}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"message": "Welcome to the SQLi Lab!"}


@app.get("/search")
def search_items(q: str):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # VULNERABLE CODE: SQL Injection via string formatting
    query = f"SELECT * FROM items WHERE name LIKE '%{q}%'"
    print(f"Executing query: {query}")

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return {"results": results}
    except mysql.connector.Error as err:
        return {"error": str(err), "query": query}
    finally:
        cursor.close()
        conn.close()
