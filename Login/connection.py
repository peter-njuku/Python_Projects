import psycopg2
from psycopg2 import OperationalError

def connection():
    try:
        connection=psycopg2.connect(
            host="localhost",
            database="login",
            user="peter",
            password="Peter",
            port="5432",
        )
        print("Connected")
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None


def create_users_table():
    conn=connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                create_table_query=(
                    """
                    CREATE TABLE IF NOT EXISTS users_table (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password_hash VARCHAR(50) NOT NULL
                    )"""
                )
                cursor.execute(create_table_query)
                conn.commit()
                print("✅ Users table created/verified")

        except Exception as e:
            print(f'Error while creating the table: {e}')
        finally:
            if conn:
                cursor.close()
                conn.close()


if __name__ =="__main__":create_users_table()