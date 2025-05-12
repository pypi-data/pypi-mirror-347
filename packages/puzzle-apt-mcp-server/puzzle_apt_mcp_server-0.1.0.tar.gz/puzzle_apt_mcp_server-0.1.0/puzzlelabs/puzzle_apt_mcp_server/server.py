from typing import Any, Optional, Dict
import httpx
import os
from mcp.server.fastmcp import FastMCP
import httpx
import os

class SKOpenAPIClient:
    BASE_URL = "https://apis.openapi.sk.com/puzzle"

    def __init__(self, app_key: str = None):
        self.app_key = app_key or os.getenv("APP_KEY")
        if not self.app_key:
            raise ValueError("APP_KEY environment variable is not set")
        self.client = httpx.Client(base_url=self.BASE_URL, headers={
            "accept": "application/json",
            "appKey": self.app_key
        })

    def get(self, endpoint: str, params: dict = None, headers: dict = None):
        merged_headers = self.client.headers.copy()
        if headers:
            merged_headers.update(headers)
        response = self.client.get(endpoint, params=params, headers=merged_headers)
        response.raise_for_status()
        return response 
    
# Initialize FastMCP server
mcp = FastMCP("apt")

# Get appKey from environment variable
APP_KEY = os.getenv("APP_KEY")
if not APP_KEY:
    raise ValueError("APP_KEY environment variable is not set")

sk_client = SKOpenAPIClient(APP_KEY)

def handle_httpx_error(e: httpx.HTTPError, context: str = "") -> str:
    """
    Handle httpx.HTTPError and return a formatted error message.
    """
    try:
        error_data = e.response.json()
        return (
            f"Error details{f' ({context})' if context else ''} - "
            f"ID: {error_data.get('error', {}).get('id', 'N/A')}, "
            f"Code: {error_data.get('error', {}).get('code', 'N/A')}, "
            f"Message: {error_data.get('error', {}).get('message', str(e))}"
        )
    except Exception:
        return f"HTTP error{f' ({context})' if context else ''}: {str(e)}"

@mcp.tool()
def get_apt_meta_code(apt_name: str) -> str:
    """
    아파트 건물의 메타 코드(kaptCode)를 조회합니다.

    Args:
        apt_name : 아파트 이름
    """
    
    base_url = "https://puzzle-hub-dev.data-puzzle.com"
    endpoint = f"/api/puzzle-data-service/apt/apts"
    
    try:
        response = httpx.get(
            f"{base_url}{endpoint}",
            params={"name": apt_name, "type": "skt"},
            headers={"accept": "application/json;charset=UTF-8"}
        )
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        
        # Check if contents exist and has items
        if data.get("contents") and len(data["contents"]) > 0:
            return data["contents"][0]["kaptCode"]
        else:
            return "No apartment found with the given name"
            
    except httpx.HTTPError as e:
        return f"Error fetching apartment meta code: {str(e)}"
    except json.JSONDecodeError as e:
        return f"Error parsing response: {str(e)}"

@mcp.tool()
def get_apartments_lifestyle_preference(kaptCode: str, category: str) -> str:
    """
    아파트 거주민의 라이프스타일 항목별 선호 목록 조회
    
    Args:
        kaptCode: 아파트 코드 (예. A13805002)
        category: 라이프스타일 항목, 아래 영문 단어 중 하나
            - kindergarden: 유치원
            - academy: 학원
            - shoppingmall: 쇼핑몰
            - mart: 대형마트
            - move-from: 이사 온 아파트
            - move-to: 이사 간 아파트
            - start-subway-station: 지하철 출발역
            - destination-subway-station: 지하철 도착역
            - workplace: 근무지
    """

    try:
        response = sk_client.get(f"residence/categories/{category}/stat/monthly/apts/{kaptCode}")
        return f"Lifestyle preference of apartments: {kaptCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_apartments_lifestyle_preference (kaptCode={kaptCode}, category={category})")

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
