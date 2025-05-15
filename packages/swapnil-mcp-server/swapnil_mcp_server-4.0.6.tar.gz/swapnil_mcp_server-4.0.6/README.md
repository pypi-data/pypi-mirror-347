# SWAPNIL MCP Server 🚀

A Model Context Protocol (MCP) server implementation for Get Weather

[![License](https://img.shields.io/github/license/erikhoward/azure-fhir-mcp-server)](https://opensource.org/licenses/MIT) [![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/) [![MCP](https://img.shields.io/badge/MCP-compatible-green.svg)](https://github.com/modelcontextprotocol/spec)

## Setup 🛠️

### Installation 📦

Requires Python 3.13 or higher.

Install the package using `pip`:

```bash
pip install swapnil-mcp-server
```

## MCP Tools 🧰

This MCP server provides a set of useful tools for various operations:

### get_Activities

Fetches the latest activities for a specific unit.

```python
async def get_Activities(unit: str) -> str
```

**Parameters:**
- `unit`: The name of the unit to retrieve activities for

**Returns:**
- A formatted string containing activity data for the specified unit

### get_SMS_Logs

Retrieves SMS logs from today up to a specified limit.

```python
async def get_SMS_Logs(limit: str) -> str
```

**Parameters:**
- `limit`: The number of SMS logs to fetch

**Returns:**
- A formatted string containing SMS log data

### send_SMS

Sends an SMS message to a specified number.

```python
async def send_SMS(to: str, body: str) -> str
```

**Parameters:**
- `to`: The phone number to send the SMS to
- `body`: The message content to be sent

**Returns:**
- A confirmation message with the message SID

## Usage 📋

To use the MCP server:

1. Install the package as described above
2. Set up required environment variables:
   - `SMS_ACCOUNT_SID`: Your Twilio account SID
   - `SMS_AUTH_TOKEN`: Your Twilio auth token
   - `HTTP_PROXY` and `HTTPS_PROXY`: If needed for your network environment
3. Run the server:

```bash
python -m mcp_tools
```

4. Connect to the server using any MCP-compatible client

## License ⚖️

Licensed under MIT - see [LICENSE.md](LICENSE) file.
