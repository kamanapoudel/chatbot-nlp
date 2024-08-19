# Chatbot using NLP

### Overview
In this project, I have created a Streamlit Chatbot integrated with Langchain technology, specifically designed for Exploratory Data Analysis (EDA) using Large Language Models (LLMs). 
The chatbot will allow users to interact with a SQL database using natural language queries. It will provide real-time data visualization and insights, streamlining the process of data exploration and analysis.

### Key Components:
* Streamlit: A Python library used for creating web applications. In this project, it will be used to build the chatbot interface.
* Langchain: A framework for developing applications powered by LLMs. It helps in connecting the chatbot to the LLM for understanding and processing natural language queries.
* SQL Database: The data source for EDA. The chatbot will query the SQL database and return results based on user input.
* LLM: A large language model (such as LLama3) will be used to interpret user queries and generate SQL queries.
* Visualization Libraries: Libraries like matplotlib, seaborn, or plotly will be used to create visualizations based on the data retrieved from the database.

### Workflow
* User Input: The user interacts with the chatbot via a text input box on the Streamlit interface.
* Natural Language Processing: The input is sent to the LLM via Langchain, where it is interpreted and converted into a corresponding SQL query.
* Query Execution: The SQL query is executed on the database, and the results are fetched.
* Data Visualization: The results are then visualized using the chosen visualization libraries.
* Response Generation: The chatbot presents the visualizations and any textual insights back to the user.

### Explanation:
* Database Connection: Connect to your SQL database (in this case, an Postgres database).
* LLM Setup: Initialize the LLM using Langchain with a prompt template that converts natural language requests into SQL queries.
* Streamlit Interface: Build a simple interface where users can input their queries.
* SQL Query Generation: Use the LLM to generate SQL queries based on user input.
* Query Execution: Execute the generated SQL query and fetch the results.
* Visualization: Visualize the data using libraries like Matplotlib and Seaborn.
* Error Handling: Include basic error handling to manage any issues with query execution.

## Chatbot Application

## Installation
1. Clone the repo
2. Install Python dependent packages
```
apt install python3.11-venv
python3 -m venv venvir
venvir/bin/pip3 install -r requirements.txt 
source venvir/bin/activate
```
3. Install Ollama and Llama3.1 ML
```
curl -fsSL https://ollama.com/install.sh | sh
ollama run llama3.1
```
4. Bring up the Postgres DB
```
docker compose up -d
```
## Start the application
```
streamlit run main.py
```

Refer to example-input.txt for sample queries to run in the chatbot
