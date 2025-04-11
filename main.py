import os
import openai
import psycopg2
import pandas as pd
from pandasql import sqldf
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

# Configure OpenAI
openai.api_type = os.getenv("OPENAI_API_TYPE")
openai.api_base = os.getenv("OPENAI_API_BASE")
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_version = os.getenv("OPENAI_API_VERSION")

# Sample data
data = {
    "name": ["Ram", "Shyam", "Sita", "Geeta", "Rohan"],
    "department": ["CSE", "IT", "ECE", "ME", "CE"],
    "salary": [50000, 60000, 55000, 58000, 62000]
}
df = pd.DataFrame(data)

def llm_convert_query_to_sql(user_query):
    """
    Uses the OpenAI LLM to convert a natural language query into a valid PostgreSQL SELECT statement.
    """
    try:
        prompt = f"""
        You are an SQL Query Generator. 
        in answer just only provide the SQL query. 
        The database is represented by a Pandas DataFrame called "employees" with the following columns:
        - name (text)
        - department (text)
        - salary (numeric)
        
        Your task is to convert a natural language question into a valid PostgreSQL SELECT query that can be executed using pandasql.
        The query must:
        - Be read-only (use only SELECT statements).
        - Perform case-insensitive matching when comparing text fields.
        - Not include any commentary, explanation, or extra text.
        
        For example, if the question is:
        "What is Ram's salary from the CSE department?"
        An appropriate SQL query would be:
        SELECT salary FROM employees WHERE LOWER(name) = LOWER('Ram') AND LOWER(department) = LOWER('CSE');
        
        Now, convert the following question into a valid SQL query:
        Question: "{user_query}"
        SQL Query:
        """

        response = openai.ChatCompletion.create(  
            engine="gpt-4",  # or another model of your choice
            messages=[
                {"role": "system", "content": "You convert natural language queries into PostgreSQL."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0,
        )

        sql_query = response.choices[0].message['content'].strip()
        logger.info(f"Generated SQL query: {sql_query}")
        return sql_query
    except Exception as e:
        logger.error(f"Error generating SQL query: {e}")
        return None

def execute_sql(sql_query):
    """
    Executes the provided SQL query on the sample DataFrame using pandasql.
    """
    try:
        if not sql_query:
            raise ValueError("Empty SQL query provided")
            
        # Safety check: Ensure only SELECT queries are allowed
        if not sql_query.strip().lower().startswith("select"):
            raise ValueError("Only SELECT queries are allowed")
        
        results = sqldf(sql_query, {"employees": df})
        logger.info("Successfully executed SQL query")
        return results
    except Exception as e:
        error_msg = f"Error executing query: {e}"
        logger.error(error_msg)
        return error_msg

def chatbot():
    """
    Main chatbot function that handles user interaction
    """
    print("Welcome to the Employee Info Chatbot!")
    print("Ask questions like: 'What is Ram's salary from the CSE department?'")
    print("Type 'exit' or 'quit' to end the session")
    
    while True:
        try:
            user_query = input("\nYour question: ").strip()
            
            if user_query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            
            if not user_query:
                print("Please enter a valid question")
                continue
            
            sql_query = llm_convert_query_to_sql(user_query)
            if sql_query is None:
                print("Sorry, I couldn't generate a valid query. Please try again.")
                continue
            
            results = execute_sql(sql_query)
            print("\nResults:")
            print(results)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    chatbot()
