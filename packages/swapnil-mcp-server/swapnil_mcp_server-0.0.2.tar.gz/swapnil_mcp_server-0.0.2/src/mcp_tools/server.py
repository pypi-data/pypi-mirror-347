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
    
    return f"HTTP Proxy set : {os.environ.get("HTTP_PROXY", "HTTP_PROXY")} , HTTPS Proxy set : {os.environ.get("HTTPS_PROXY", "HTTPS_PROXY")}"
    proxies = {
    "http": "http://genproxy.corp.amdocs.com:8080", 
    "https": "http://genproxy.corp.amdocs.com:8080",
    }
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Activities'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, proxies=proxies)
        if response.status_code == 200:
            data = response.json()
            return f"Activities For Unit {unit} are : {data})"
        else:
            return f"No Activities Info. Error: {response.status_code}"

     
     