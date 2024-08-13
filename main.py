import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from configparser import ConfigParser
from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import matplotlib.pyplot as plt
import seaborn as sns

# Load configuration from the config.ini file
config = ConfigParser()
config.read('config.ini')

# Get database credentials from the config file
db_name = config.get('database', 'DB_NAME')
db_user = config.get('database', 'DB_USER')
db_password = config.get('database', 'DB_PASSWORD')
db_host = config.get('database', 'DB_HOST')
db_port = config.get('database', 'DB_PORT')

# Connect to the PostgreSQL database
engine = create_engine(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
conn = engine.connect()

# Set up the LLM
llm = OpenAI(temperature=0.7)

# Define the prompt template
template = """
You are an expert data analyst. Convert the following natural language request into a SQL query.
Request: {user_query}
SQL Query:
"""
prompt = PromptTemplate(template=template, input_variables=["user_query"])
chain = LLMChain(prompt=prompt, llm=llm)

# Streamlit interface
st.title("EDA Chatbot with Langchain")
user_query = st.text_input("Ask a question about your data:")

if user_query:
    # Generate SQL query from the user's natural language query
    sql_query = chain.run({"user_query": user_query})
    st.write(f"Generated SQL Query: {sql_query}")
    
    # Execute the SQL query
    try:
        df = pd.read_sql_query(sql_query, conn)
        
        # Display the results as a table
        st.write(df)
        
        # Basic visualization example (customize as needed)
        st.write("Data Visualization:")
        plt.figure(figsize=(10, 6))
        sns.histplot(df.iloc[:, 0], kde=True)
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Error executing query: {str(e)}")

# Close the database connection
conn.close()
