from typing import Any, Optional, Dict
import httpx
import os
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ValidationError, Field
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
def get_apt_meta(apt_name: str) -> str:
    """
    아파트 건물의 메타 정보를 조회합니다.

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
            return data["contents"]
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

@mcp.tool()
def get_apartment_resident_features(kaptCode: str) -> str:
    """
    동일 시도 대비 해당 아파트 주민 구성의 비율이 높은 Life stage(영유아, 초등학생, 중학생, 고등학생, 대학생, 1인가구, 신혼부부, 시니어) 값을 제공합니다.

    Args:
        kaptCode: 아파트 코드 (예. A13805002)
    """
    try:
        response = sk_client.get(f"residence/resident/demo-feature/stat/monthly/apts/{kaptCode}")
        return response.text
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_apartment_resident_features (kaptCode={kaptCode})")


class DistrictPopularAptInput(BaseModel):
    district_code: str = Field(..., description="인기 아파트를 조회할 시군수(구/군) 법정동 코드(예: '1111000000')")
    type: str = Field(
        "all",
        description="조회 타입(아래 중 하나)\n- all\n- newlyweds(신혼부부)\n- single(1인가구)\n- preschool(영유아)\n- elementary(초등학생)\n- middle(중학생)\n- high(고등학생)\n- univ(대학생)\n- 2030(2030세대)\n- 4050(4050세대)\n- 60over(60세 이상)"
    )
    limit: int = Field(5, description="결과 개수 제한(기본값 5)")

@mcp.tool()
def get_district_popular_apartments(district_code: str, type: str = "all", limit: int = 5) -> str:
    """
    시군수(구/군) 내 인기 아파트를 조회합니다.
    Args:
        district_code: 시군수(구/군) 법정동 코드(예: '1111000000')
        type: 조회 타입(아래 중 하나)
            - all
            - newlyweds(신혼부부)
            - single(1인가구)
            - preschool(영유아)
            - elementary(초등학생)
            - middle(중학생)
            - high(고등학생)
            - univ(대학생)
            - 2030(2030세대)
            - 4050(4050세대)
            - 60over(60세 이상)
        limit: 결과 개수 제한(기본값 5)
    """
    params = DistrictPopularAptInput(district_code=district_code, type=type, limit=limit)
    base_url = f"https://puzzle-hub-prd.data-puzzle.com/api/puzzle-data-service/apt/realtor-popular-apt/stat/weekly/districts/{params.district_code}"
    query_params = {
        "type": params.type,
        "limit": str(params.limit)
    }
    headers = {
        "accept": "application/json;charset=UTF-8"
    }
    try:
        response = httpx.get(base_url, params=query_params, headers=headers)
        response.raise_for_status()
        return f"District popular apartments for {params.district_code}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_district_popular_apartments (district_code={params.district_code}, type={params.type}, limit={params.limit})")

class DistrictCodeSearchInput(BaseModel):
    name: str = Field(..., description="법정동, 시군구 이름(예: '명동', '강남구')")
    districtType: str = Field("all", description="법정동 타입(기본값: all)")
    limit: int = Field(10, description="결과 개수 제한(기본값: 10)")

@mcp.tool()
def get_district_code_by_name(name: str, type: str = "skt", districtType: str = "all", polygon: bool = False, limit: int = 10) -> str:
    """
    법정동, 시군구 이름으로 법정동 코드를 조회합니다.
    Args:
        name: 법정동, 시군구 이름(예: '명동', '강남구')
        districtType: 법정동 타입(기본값: all)
        limit: 결과 개수 제한(기본값: 10)
    """
    params = DistrictCodeSearchInput(name=name, districtType=districtType, limit=limit)
    base_url = "https://puzzle-hub-prd.data-puzzle.com/api/puzzle-data-service/apt/districts"
    query_params = {
        "name": params.name,
        "districtType": params.districtType,
        "limit": str(params.limit)
    }
    headers = {
        "accept": "application/json;charset=UTF-8"
    }
    try:
        response = httpx.get(base_url, params=query_params, headers=headers)
        response.raise_for_status()
        return f"District code search for {params.name}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_district_code_by_name (name={params.name})")


def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
