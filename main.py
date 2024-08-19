#Author: Kamana Poudel
#Date: 19-Aug-2024

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from configparser import ConfigParser
import requests  # For making HTTP requests to the Llama3 API
import matplotlib.pyplot as plt
import seaborn as sns
import traceback  # To capture the full stack trace of exceptions

# Load configuration from the config.ini file
config = ConfigParser()
config.read('config.ini')

# Get database credentials from the config file
db_name = config.get('database-dev', 'DB_NAME')
db_user = config.get('database-dev', 'DB_USER')
db_password = config.get('database-dev', 'DB_PASSWORD')
db_host = config.get('database-dev', 'DB_HOST')
db_port = config.get('database-dev', 'DB_PORT')

# Connect to the PostgreSQL database
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
conn = engine.connect()

# Set the Llama3 API URL (assuming it's hosted on localhost with port 11434)
llama3_api_url = "http://localhost:11434/api/generate"

# Function to get existing tables from the database
def get_existing_tables():
    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_type = 'BASE TABLE' 
    AND table_schema NOT IN ('pg_catalog', 'information_schema');
    """
    try:
        st.write("Executing query to fetch tables...")
        tables_df = pd.read_sql_query(query, conn)
        st.write(f"Tables fetched: {tables_df['table_name'].tolist()}")
        return tables_df['table_name'].tolist()  # Return list of table names
    except Exception as e:
        st.error(f"Error fetching tables: {str(e)}")
        st.write(f"Full error details: {traceback.format_exc()}")
        return []  # Return an empty list in case of error

# Function to format the list of tables
def format_table_list(table_list):
    if not table_list:
        st.write("No tables found.")
        return "No tables available."
    formatted_list = "\n".join(f"- {table}" for table in table_list)
    st.write(f"Formatted table list: {formatted_list}")
    return formatted_list

# Define the prompt template with the table list
def create_prompt(user_query, table_list):
    table_list_str = format_table_list(table_list)
    prompt_template = f"""
    You are an expert data analyst. Convert the following natural language request into a SQL query.
    Available tables: {table_list_str}
    Request: {user_query}
    SQL Query:
    """
    st.write(f"Prompt created: {prompt_template}")
    return prompt_template

# Function to extract SQL query from the Llama3 response
def extract_sql_query(text):
    start_marker = "```sql"
    end_marker = "```"
    
    start_idx = text.find(start_marker)
    end_idx = text.find(end_marker, start_idx + len(start_marker))
    
    if start_idx != -1 and end_idx != -1:
        start_idx += len(start_marker)
        extracted_query = text[start_idx:end_idx].strip()
        st.write(f"Extracted SQL query: {extracted_query}")
        return extracted_query
    else:
        st.write("Failed to find SQL query markers in response.")
        return "SQL query not found"

# Function to generate SQL query using the Llama3 API
def generate_sql_query(user_query):
    table_list = get_existing_tables()  # Fetch list of tables
    prompt = create_prompt(user_query, table_list)  # Create prompt with table list
    print(f"User Query: {user_query}")  # Display the query for inspection

    # Prepare the JSON payload
    payload = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False  # This should be properly capitalized
    }
    print(f"Payload: {payload}")  # Display the payload

    # Send the POST request
    response = requests.post(llama3_api_url, json=payload)
    print(f"Response from Llama3: {response}")  # Display the response status code

    if response.status_code == 200:
        result = response.json()
        print(f"Result from Llama3: {result}")  # Display the result

        # Extract the SQL query from the 'response' field
        sql_query_text = result['response'].strip()
        print(f"Generated SQL Query Text: {sql_query_text}")  # Display the entire response for inspection

        # Extract only the SQL query
        sql_query = extract_sql_query(sql_query_text)
        print(f"Extracted SQL Query: {sql_query}")  # Display the extracted SQL query
        return sql_query
    else:
        print(f"Response from Llama3 in else block: {response.status_code}, {response.text}")  # Display the response error
        raise Exception(f"Error from Llama3 API: {response.status_code}, {response.text}")


### Main
# Streamlit interface
st.title("Text to SQL- Chatbot with Llama3")

# User query input
user_query = st.text_input("Ask a question about your data:")

if user_query:
    # Generate SQL query from the user's natural language query
    try:
        sql_query = generate_sql_query(user_query)
        st.write(f"Generated SQL Query: {sql_query}")
        
        # Execute the SQL query
        try:
            st.write(f"Executing SQL query: {sql_query}")
            df = pd.read_sql_query(sql_query, conn)
            st.write("Query executed successfully.")
            
            # Display the results as a table
            st.write(df)
            
            # Basic visualization example (customize as needed)
            st.write("Data Visualization:")
            plt.figure(figsize=(10, 6))
            sns.histplot(df.iloc[:, 0], kde=True)
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")
            st.write(f"Full error details: {traceback.format_exc()}")  # Full stack trace for error debugging
    except Exception as e:
        st.error(f"Error generating SQL query: {str(e)}")
        st.write(f"Full error details: {traceback.format_exc()}")  # Full stack trace for error debugging

# Close the database connection
conn.close()
