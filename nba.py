import os
from sqlalchemy import create_engine
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# PostgreSQL Connection Parameters
conn_params = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "database": os.getenv("DB_NAME", "nba_db"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

def test_connection():
    """Test the PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**conn_params)
        logger.info("✅ Successfully connected to PostgreSQL using psycopg2!")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"❌ Error connecting to PostgreSQL: {e}")
        return False

def get_engine():
    """Create and return SQLAlchemy engine"""
    try:
        engine = create_engine(
            f"postgresql://{conn_params['user']}:{conn_params['password']}@{conn_params['host']}:{conn_params['port']}/{conn_params['database']}"
        )
        return engine
    except Exception as e:
        logger.error(f"❌ Error creating SQLAlchemy engine: {e}")
        return None

def get_tables():
    """Fetch all tables in the database"""
    try:
        engine = get_engine()
        if engine is None:
            return None

        query = """
        SELECT table_schema, table_name 
        FROM information_schema.tables 
        WHERE table_schema NOT IN ('pg_catalog', 'information_schema') 
        ORDER BY table_schema, table_name;
        """

        df_tables = pd.read_sql(query, engine)
        logger.info("✅ Successfully fetched database tables")
        return df_tables
    except Exception as e:
        logger.error(f"❌ Error fetching tables: {e}")
        return None

if __name__ == "__main__":
    if test_connection():
        tables = get_tables()
        if tables is not None:
            print(tables)


