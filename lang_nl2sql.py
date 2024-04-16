import os
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI, AzureChatOpenAI, OpenAIEmbeddings
from operator import itemgetter
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
import mysql.connector
from mysql.connector import Error

load_dotenv()

## MY SQL DB Connection details
db_user = os.getenv("MYSQL_DB_USER")
db_password = os.getenv("MYSQL_DB_PASS")
db_host = os.getenv("MYSQL_DB_HOST")
db_name = ''  # os.getenv("MYSQL_DB_NAME")

## Langchain API details
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")


def get_mysql_db_conn(db_user, db_password, db_host, db_name):
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
    return db

## This part is just for testing purpose on DB connection (MySQL)
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.table_info)

# ## Using Normal OpenAI
# OPENAI_API_KEY = os.getenv("O_OPENAI_API_KEY")
#
# llm_openai = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo", temperature=0)
# generate_query = create_sql_query_chain(llm_openai, db)
#
# query = generate_query.invoke({"question": "what is price of `1968 Ford Mustang`"})
# print(query)

## Using Azure OpenAI

AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
azure_api_version = os.getenv("AZURE_OPENAI_API_VERSION1"),
azure_endpoint = os.getenv("AZURE_OPENAI_API_BASE1")

# openai.api_type = "azure"
# openai.api_key = os.getenv("OPENAI_API_KEY")
# openai.api_base = os.getenv("OPENAI_API_BASE") # Endpoint
# openai.api_version = os.getenv("OPENAI_API_VERSION")
# openai.deployment_name = os.getenv("DEPLOYMENT_NAME")
# # openai_deployment = "chat-gpt35"
openai_deployment = os.getenv("AZURE_DEPLOYMENT_NAME1")
# openai_model = "gpt-35-turbo"

llm_azureopenai = AzureChatOpenAI(openai_api_key=AZURE_OPENAI_API_KEY,
                                  openai_api_version='2023-07-01-preview',
                                  azure_endpoint="https://qaazureaiservice.openai.azure.com/",
                                  azure_deployment=openai_deployment)


def get_sql_query(mysql_db, user_question):
    generate_query_az = get_query_chain(mysql_db)
    query_az = generate_query_az.invoke({"question": user_question})
    return query_az, generate_query_az


def get_query_chain(mysql_db):
    generate_query_az = create_sql_query_chain(llm_azureopenai, mysql_db)
    return generate_query_az


def get_sqlquery_result(mysql_db, sql_query, user_question, generate_query_az):
    execute_query = QuerySQLDataBaseTool(db=mysql_db)
    # execute_query.invoke(sql_query)

    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """ + """"only replace the query with is """ + sql_query +
        """" by removing any 'limit' keyword in the query and provide the only Answer: """
    )

    rephrase_answer = answer_prompt | llm_azureopenai | StrOutputParser()

    chain = (
            RunnablePassthrough.assign(query=generate_query_az).assign(
                result=itemgetter('query') | execute_query
            )
            | rephrase_answer
    )

    result = chain.invoke({"question": str(user_question)})
    sql_query_result = result.replace('\n', '')
    return sql_query_result


def get_sqlquery_result_only(mysql_db, user_question, generate_query_az):
    execute_query = QuerySQLDataBaseTool(db=mysql_db)
    # execute_query.invoke(sql_query)

    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question.
    
    Question: {question}
    SQL Query: {query}
    SQL Result: {result}
    Answer: """
    )

    rephrase_answer = answer_prompt | llm_azureopenai | StrOutputParser()

    chain = (
            RunnablePassthrough.assign(query=generate_query_az).assign(
                result=itemgetter('query') | execute_query
            )
            | rephrase_answer
    )

    result = chain.invoke({"question": str(user_question)})
    return result


def get_sql_with_result(user_question, database_name):
    user_question = str(user_question)
    mysql_db = get_mysql_db_conn(db_user, db_password, db_host, database_name)
    sql_query, generate_query_az = get_sql_query(mysql_db, user_question)
    query_result = get_sqlquery_result(mysql_db, sql_query, user_question, generate_query_az)
    return user_question, sql_query, query_result


def get_only_sql_query(user_question, database_name):
    user_question = str(user_question)
    mysql_db = get_mysql_db_conn(db_user, db_password, db_host, database_name)
    sql_query, generate_query_az = get_sql_query(mysql_db, user_question)
    return user_question, sql_query


def get_only_sqlquery_result(user_question, database_name):
    user_question = str(user_question)
    mysql_db = get_mysql_db_conn(db_user, db_password, db_host, database_name)
    generate_query_az = get_query_chain(mysql_db)
    query_result = get_sqlquery_result_only(mysql_db, user_question, generate_query_az)
    return user_question, query_result


def execute_mysql_file(sql_file):
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )

        cursor = connection.cursor()
        # Check if the connection is successful
        if connection.is_connected():
            print("Database connection successful.")
            # Read and execute SQL queries from the file
            with open(sql_file, 'r') as file:
                sql_commands = file.read().split(';')
                for sql_command in sql_commands:
                    if sql_command.strip():
                        cursor.execute(sql_command)

            # Commit changes
            connection.commit()

            print("Database/Schema created and SQL queries executed.")
        else:
            print("Error connecting to the database.")

    except Error as e:
        print(f"Error connecting to the database or executing SQL queries: {e}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")

def get_all_db_names():
    try:
        # Connect to MySQL server
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )

        cursor = connection.cursor()
        # Check if the connection is successful
        if connection.is_connected():
            print("Database connection successful.")
            # extract all DB/schema names from My sQL 
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            db_names = [db[0] for db in databases if not db[0].startswith('information_schema') and not db[0].startswith('mysql') and not db[0].startswith('performance_schema')]
            print("Extracted all the DB/Schema names:", db_names)
            return db_names
        else:
            print("Error connecting to the database.")

    except Error as e:
        print(f"Error connecting to the database or executing SQL queries: {e}")

    finally:
        # Close cursor and connection
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("Database connection closed.")
