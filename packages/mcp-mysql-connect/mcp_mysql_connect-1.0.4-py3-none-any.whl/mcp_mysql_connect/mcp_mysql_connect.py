from mcp.server.fastmcp import FastMCP
import os
from typing import Any, Dict, List
from dotenv import load_dotenv
import mysql.connector  
import logging
import sys 

# Configure logging 
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    stream=sys.stderr 
)
# Load environment variables from .env file
load_dotenv()

# Create an MCP server
mcp = FastMCP("db_server")
logging.info("MCP server object created.")

# Database connection configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME') 
}
logging.info("Database configuration loaded.")

def get_db_connection():
    conn = None 
    try:
        logging.info("Attempting to connect to the database...")
        # Attempt to establish a connection
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
             logging.info("Database connection established successfully.")
             return conn
        else:
            logging.error("mysql.connector.connect did not raise an error but connection is not active.")
            return None 
    except mysql.connector.Error as err:
        logging.error(f"MySQL connection error: {err}", exc_info=True)
        return None
    except Exception as e:
        # Catch any other unexpected errors during connection
        logging.error(f"Unexpected error during database connection: {e}", exc_info=True)
        return None
#tools in server
@mcp.tool()
def read_query(query: str, params: List[str] = None) -> Dict[str, Any]:
    """Execute a SELECT query"""
    logging.info(f"Executing query: {query} with params: {params}")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        # Check if the connection attempt was successful
        if conn is None or not conn.is_connected():
             logging.error("Failed to establish database connection for query.")
             return {"status": "error", "message": "Failed to connect to the database"} 

        # Proceed only if connection is valid
        logging.info(f"Connected to DB: {conn.get_server_info()} on database: {conn.database}")
        cursor = conn.cursor(dictionary=True)
        # Convert params to tuple if not None, else empty tuple
        param_tuple = tuple(params) if params is not None else ()
        logging.debug(f"Executing cursor with query: '{query}' and params: {param_tuple}")
        cursor.execute(query, param_tuple) 
        fetched_data = cursor.fetchall()
        logging.info(f"Query executed successfully. Fetched {len(fetched_data)} rows.")
        return {"status": "success", "data": fetched_data}
    except mysql.connector.Error as err:
         # Log specific database errors during query execution
         logging.error(f"Database error during query execution: {err}")
         # Use the correct variable 'err' in the log message below
         logging.error(f"An unexpected error occurred in read_query: {err}", exc_info=True)
         return {"status": "error", "message": str(err)} # Return the specific MySQL error
    except Exception as e:
        # Catch any other unexpected errors during the query process
        logging.error(f"An unexpected error occurred in read_query: {e}", exc_info=True)
        return {"status": "error", "message": "An unexpected server error occurred during query execution."}
    finally:
        # Ensure cursor and connection are closed if they were opened
        if cursor:
            cursor.close()
            logging.debug("Database cursor closed.")
        if conn and conn.is_connected():
            conn.close()
            logging.info("Database connection closed.")


@mcp.tool()
def list_tables() -> Dict[str, Any]:
    """List all tables in the current database"""
    logging.info("Listing all tables in the database.")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            logging.error("Failed to establish database connection for listing tables.")
            return {"status": "error", "message": "Failed to connect to the database"} 

        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = [row[0] for row in cursor.fetchall()]
        logging.info(f"Retrieved {len(tables)} tables.")
        return {"status": "success", "tables": tables}
    except mysql.connector.Error as err:
        logging.error(f"Database error during listing tables: {err}")
        return {"status": "error", "message": str(err)}
    except Exception as e:
        logging.error(f"An unexpected error occurred in list_tables: {e}", exc_info=True)
        return {"status": "error", "message": "An unexpected server error occurred during listing tables."}
    finally:
        if cursor:
            cursor.close()
            logging.debug("Database cursor closed.")
        if conn and conn.is_connected():
            conn.close()
            logging.info("Database connection closed.")

@mcp.tool()
def describe_table(table_name: str) -> Dict[str, Any]:
    """Describe the structure of a table"""
    logging.info(f"Describing table: {table_name}")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            logging.error("Failed to establish database connection for describing table.")
            return {"status": "error", "message": "Failed to connect to the database"} 

        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"DESCRIBE {table_name};")
        description = cursor.fetchall()
        logging.info(f"Retrieved description for table {table_name}.")
        return {"status": "success", "description": description}
    except mysql.connector.Error as err:
        logging.error(f"Database error during describing table: {err}")
        return {"status": "error", "message": str(err)}
    except Exception as e:
        logging.error(f"An unexpected error occurred in describe_table: {e}", exc_info=True)
        return {"status": "error", "message": "An unexpected server error occurred during describing table."}
    finally:
        if cursor:
            cursor.close()
            logging.debug("Database cursor closed.")
        if conn and conn.is_connected():
            conn.close()
            logging.info("Database connection closed.")

@mcp.tool()
def execute_query(query: str, params: List[str] = None) -> Dict[str, Any]:
    """Execute a general SQL query (INSERT, UPDATE, DELETE)"""
    logging.info(f"Executing query: {query} with params: {params}")
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        if conn is None or not conn.is_connected():
            logging.error("Failed to establish database connection for executing query.")
            return {"status": "error", "message": "Failed to connect to the database"} 

        cursor = conn.cursor()
        param_tuple = tuple(params) if params is not None else ()
        cursor.execute(query, param_tuple)
        conn.commit()
        affected_rows = cursor.rowcount
        logging.info(f"Query executed successfully. Affected {affected_rows} rows.")
        return {"status": "success", "affected_rows": affected_rows}
    except mysql.connector.Error as err:
        logging.error(f"Database error during executing query: {err}")
        return {"status": "error", "message": str(err)}
    except Exception as e:
        logging.error(f"An unexpected error occurred in execute_query: {e}", exc_info=True)
        return {"status": "error", "message": "An unexpected server error occurred during executing query."}
    finally:
        if cursor:
            cursor.close()
            logging.debug("Database cursor closed.")
        if conn and conn.is_connected():
            conn.close()
            logging.info("Database connection closed.")


if __name__ == "__main__":
    logging.info("Starting MCP server...")
    # Initialize and run the server
    mcp.run(transport='stdio')
    logging.info("MCP server has stopped.")