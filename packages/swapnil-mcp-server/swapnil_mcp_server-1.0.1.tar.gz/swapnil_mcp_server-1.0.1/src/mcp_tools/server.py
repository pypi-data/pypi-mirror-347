from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()

# Set up the proxy
proxies = {
    os.environ['HTTP_PROXY'],
    os.environ['HTTPS_PROXY'],
}

# Set up the proxy for requests
mcp = FastMCP("MCP_Tools")

@mcp.tool()
async def get_weather(city: str) -> str:
    """Get weather for city.
    Args:
        city: any indian city
    """
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=9714c902c784730338c95bd3140cc6ed" ,timeout=30.0, verify=False, proxies=proxies)
    return response.content