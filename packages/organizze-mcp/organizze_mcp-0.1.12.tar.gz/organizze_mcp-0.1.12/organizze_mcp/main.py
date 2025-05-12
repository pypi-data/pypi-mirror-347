import os
import requests
import base64
from fastmcp import FastMCP
from dotenv import load_dotenv
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO)

load_dotenv()

mcp = FastMCP("Organizze MCP Server")
today = datetime.now().strftime("%Y-%m-%d")

ORGANIZZE_API_URL = "https://api.organizze.com.br/rest/v2"

def get_auth_header():
    """Get API authentication header using environment variables"""
    
    auth_str = f"{os.getenv('ORGANIZZE_EMAIL')}:{os.getenv('ORGANIZZE_TOKEN')}"
    auth_bytes = auth_str.encode("ascii")
    auth_b64 = base64.b64encode(auth_bytes).decode("ascii")
    
    logging.info(f"User-Agent: {os.getenv('ORGANIZZE_NAME')} ({os.getenv('ORGANIZZE_EMAIL')})")
    return {"Authorization": f"Basic {auth_b64}", "User-Agent": f"{os.getenv('ORGANIZZE_NAME')} ({os.getenv('ORGANIZZE_EMAIL')})"}


@mcp.tool()
def list_transactions(start_date: str = today, end_date: str = today):
    """List transactions for a given date range
    
    Args:
        start_date (str): The start date of the date range (YYYY-MM-DD)
        end_date (str): The end date of the date range (YYYY-MM-DD)

    Returns:
        list: A list of transaction
    """
    response = requests.get(f"{ORGANIZZE_API_URL}/transactions", headers=get_auth_header(), params={"start_date": start_date, "end_date": end_date})
    return response.json()

@mcp.tool()
def list_categories():
    response = requests.get(f"{ORGANIZZE_API_URL}/categories", headers=get_auth_header())
    return response.json()

@mcp.tool()
def set_transaction_category(transaction_id: str, category_id: str):
    """Set the category of a transaction
    Before update check if the category id isn't already correct
    
    Args:
        transaction_id (str): The transaction id
        category_id (str): The category id
    """
    response = requests.put(f"{ORGANIZZE_API_URL}/transactions/{transaction_id}", headers=get_auth_header(), json={"category_id": category_id})
    return response.json()

@mcp.tool()
def list_accounts():
    response = requests.get(f"{ORGANIZZE_API_URL}/accounts", headers=get_auth_header())
    return response.json()

@mcp.tool()
def list_credit_cards():
    response = requests.get(f"{ORGANIZZE_API_URL}/credit_cards", headers=get_auth_header())
    return response.json()

@mcp.tool()
def list_budgets():
    response = requests.get(f"{ORGANIZZE_API_URL}/budgets", headers=get_auth_header())
    return response.json()

def main():
    mcp.run()

if __name__ == "__main__":
    main()