from mcp.server.fastmcp import FastMCP
import httpx
import os 
from dotenv import load_dotenv 
mcp = FastMCP("MCP_Tools")

@mcp.tool()
async def get_Activities(unit : str) -> str:
    """Get Latest Activities for UNIT
    Args:
        unit: Unit Name
    """
    load_dotenv()
    
    proxies = {
    "http": os.environ.get("HTTP_PROXY"), 
    "https":os.environ.get("HTTPS_PROXY"),
    }
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Activities'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            return f"Activities For Unit {unit} are : {data})"
        else:
            return f"No Activities Info. Error: {response.status_code}"

     
     