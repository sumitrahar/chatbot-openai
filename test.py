

import openai
import psycopg2
from psycopg2 import sql

# Azure OpenAI Configuration
openai.api_type = "azure"
openai.api_base = "https://project-komp.openai.azure.com/"
openai.api_key = "CdTiGBHZd04q2kNbXKzMud27LvssSsfm0RkrTDlvPpDdHLKOknK9JQQJ99BAACYeBjFXJ3w3AAABACOGvVoL"  # Replace with your actual key
openai.api_version = "2023-09-01-preview"


# PostgreSQL Configuration
conn_params = {
    "host": "127.0.0.1",
    "database": "demo",
    "user": "postgres",
    "password": "Esol@s",  # Replace with your password
    "port": "5432"
}


def generate_sql_query(prompt):
    """Generate Postgres query using Azure Open AI with schema context."""
    try:
        # Provide database schema context to improve SQL accuracy
        schema_context = (
            "The database has tables: products (id, name, price, stock_quantity), "
            "orders (id, product_id, quantity), customers (id, name, email). "
            "Generate a valid postgres query without semicolons."
        )
        
        response = openai.ChatCompletion.create(
            engine="gpt-4o",  # e.g., "gpt-4"
            messages=[
                {"role": "system", "content": "You are a postgres query generator. " + schema_context},
                {"role": "user", "content": f"Convert this to postgres: {prompt}"}
            ],
            temperature=0.1,  # Lower temperature for deterministic responses
            max_tokens=200  # Increase token limit for longer queries
        )
        
        # Extract SQL from response (adjust based on model output format)
        sql_query = response.choices[0].message["content"].strip()
        # Remove any trailing semicolons to avoid syntax errors
        sql_query = sql_query.rstrip(';').strip()
        return sql_query
    
    except Exception as e:
        print(f"Error generating SQL: {e}")
        return None

def execute_sql_query(sql):
    """Execute SQL query safely with error handling."""
    try:
        conn = psycopg2.connect(**conn_params)
        cursor = conn.cursor()
        
        # Use parameterized queries if possible (example for future expansion)
        # cursor.execute(sql.SQL("SELECT * FROM products WHERE price < %s"), (price_limit,))
        
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results
    
    except psycopg2.Error as e:
        print(f"PostgreSQL Error: {e.pgerror}")
        return None
    except Exception as e:
        print(f"Error executing SQL: {e}")
        return None
    finally:
        if conn:
            conn.close()

def main():
    user_query = input("Enter your search (e.g., 'Show products with price < $500'): ")
    print("\nGenerating SQL query...")
    sql = generate_sql_query(user_query)
    
    if sql:
        print(f"Generated SQL: {sql}")
        print("\nExecuting SQL query...")
        results = execute_sql_query(sql)
        
        if results:
            print("\nQuery Results:")
            for row in results:
                print(row)
        else:
            print("No results found or an error occurred.")
    else:
        print("Failed to generate SQL query. Please try again.")

if __name__ == "__main__":
    main()


