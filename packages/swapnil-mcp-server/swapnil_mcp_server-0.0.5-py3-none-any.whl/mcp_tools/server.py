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
    
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Activities'
    async with httpx.AsyncClient() as client:
        load_dotenv()     
        httpProxy = os.environ.get("HTTP_PROXY", "http://genproxy.corp.amdocs.com:8080")
        httpsProxy = os.environ.get("HTTPS_PROXY", "http://genproxy.corp.amdocs.com:8080")   
        myproxies = {
        "http": httpProxy, 
        "https": httpsProxy,
        }
        response = await client.get(url, proxies=myproxies)
        if response.status_code == 200:
            data = response.json()
            return f"Activities For Unit {unit} are : {data})"
        else:
            return f"No Activities Info. Error: {response.status_code}"

     
     