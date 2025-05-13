from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("WebExtractor")

@mcp.tool()
def extract_content(url: str) -> str:
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Get web text
        text = soup.get_text()
        return text
    except Exception as e:
        return f"Error: {str(e)}"
    
def main():
    mcp.run()

if __name__ == "__main__":
    main()
