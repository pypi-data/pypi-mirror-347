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
mcp = FastMCP("place")

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

class PlaceRealtimeCongestionInput(BaseModel):
    poi_id: str = Field(..., description="관심 장소(POI) ID")

@mcp.tool()
def get_place_realtime_congestion(poi_id: str) -> str:
    """
    특정 장소의 실시간 혼잡도를 제공합니다. (SK OpenAPI)
    Args:
        poi_id: 관심 장소(POI) ID (예: '10067845')
    """
    params = PlaceRealtimeCongestionInput(poi_id=poi_id)

    endpoint = f"place/congestion/rltm/pois/{params.poi_id}"
   
    try:
        response = sk_client.get(endpoint)
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        contents = data.get("contents", {})
        rltm_list = contents.get("rltm", [])
        if not rltm_list:
            return f"혼잡도 정보가 없습니다. (poiId={params.poi_id})"
        result = (
            f"[장소 혼잡도 정보] {contents.get('poiName', '')} (POI ID: {contents.get('poiId', '')})\n"
        )
        for item in rltm_list:
            level_map = {1: '여유', 2: '보통', 3: '혼잡', 4: '매우 혼잡'}
            result += (
                f"- 유형: {'장소' if item.get('type') == 1 else '주변'} 혼잡도\n"
                f"- 혼잡도: {item.get('congestion')} 명/㎡\n"
                f"- 혼잡도 레벨: {item.get('congestionLevel')} ({level_map.get(item.get('congestionLevel'), '알수없음')})\n"
                f"- 집계 시각: {item.get('datetime')}\n"
            )
        return result
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_place_realtime_congestion (poi_id={params.poi_id})")

class PlaceMetaInput(BaseModel):
    name: str = Field(..., description="POI 이름")
    
@mcp.tool()
def get_place_meta(name: str) -> str:
    """
    POI 이름을 입력 받아서 메타 정보를 조회합니다.
    Args:
        name: POI 이름 (예: '스타필드')
    """
    params = PlaceMetaInput(name=name)
    endpoint = "https://puzzle-hub-prd.data-puzzle.com/api/puzzle-data-service/poi/pois/meta"
    try:
        response = httpx.get(endpoint, params=params.dict(), headers={"accept": "application/json;charset=UTF-8"})
        response.raise_for_status()
        return f"Place info for {params.name}: {response.text}"    
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_place_meta (name={name})")

class PlaceStatHourlyCongestionInput(BaseModel):
    poi_id: str = Field(..., description="관심 장소(POI) ID")
    dow: str = Field(..., description="검색 기준 요일 (예: 'MON', 'TUE' 등)")

@mcp.tool()
def get_place_hourly_congestion(poi_id: str, dow: str) -> str:
    """
    특정 장소의 요일 및 시간대별 통계성 혼잡도를 제공합니다.
    Args:
        poi_id: 관심 장소(POI) ID (예: '10067845')
        dow: 검색 기준 요일 (예: 'MON', 'TUE' 등)
    """
    params = PlaceStatHourlyCongestionInput(poi_id=poi_id, dow=dow)
    endpoint = f"place/congestion/stat/hourly/pois/{params.poi_id}"
    query_params = {"dow": params.dow} if params.dow else None
    try:
        response = sk_client.get(endpoint, params=query_params)
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        contents = data.get("contents", {})
        stat_list = contents.get("stat", [])
        if not stat_list:
            return f"통계성 혼잡도 정보가 없습니다. (poiId={params.poi_id})"
        # 4단계 혼잡도 매핑
        def map_to_4level(congestion: float) -> str:
            if congestion < 0.025:
                return "여유"
            elif congestion < 0.05:
                return "보통"
            elif congestion < 0.3:
                return "혼잡"
            else:
                return "매우 혼잡"
        result = (
            f"[통계성 장소 혼잡도 정보] {contents.get('poiName', '')} (POI ID: {contents.get('poiId', '')})\n"
            f"통계 기간: {contents.get('statStartDate', '')} ~ {contents.get('statEndDate', '')}\n"
        )
        for item in stat_list:
            congestion = item.get('congestion')
            congestion_level = item.get('congestionLevel')
            dow = item.get('dow')
            hh = item.get('hh')
            result += (
                f"- 요일: {dow}, 시간: {hh}시\n"
                f"  · 혼잡도: {congestion} 명/㎡\n"
                f"  · 혼잡도 레벨(1~10): {congestion_level}\n"
                f"  · 4단계 혼잡도: {map_to_4level(congestion)}\n"
            )
        return result
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_place_hourly_congestion (poi_id={params.poi_id}, dow={params.dow})")

class PlaceDailyVisitCountInput(BaseModel):
    poi_id: str = Field(..., description="관심 장소(POI) ID")
    gender: str = Field(..., description="조회 대상 성별 (male, female, all)")
    ageGrp: str = Field(..., description="조회 대상 연령대 (0, 10, 20, ..., 100_over, all)")
    
@mcp.tool()
def get_place_daily_visit_count(
    poi_id: str,
    gender: str,
    ageGrp: str,
) -> str:
    """
    특정 장소의 최근 30일간 일자별 추정 방문자 수를 조회합니다.
    Args:
        poi_id: 관심 장소(POI) ID (예: '10067845')
        gender: 조회 대상 성별 (male, female, all)
        ageGrp: 조회 대상 연령대 (0, 10, 20, ..., 100_over, all)
    """
    params = PlaceDailyVisitCountInput(
        poi_id=poi_id, gender=gender, ageGrp=ageGrp,
    )
    endpoint = f"place/visit/count/raw/daily/pois/{params.poi_id}"
    query_params = {}
    if params.gender: query_params["gender"] = params.gender
    if params.ageGrp: query_params["ageGrp"] = params.ageGrp
    try:
        response = sk_client.get(endpoint, params=query_params)
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        contents = data.get("contents", {})
        visit_list = contents.get("raw", [])
        if not visit_list:
            return f"방문자 수 정보가 없습니다. (poiId={params.poi_id})"
        result = (
            f"[일자별 추정 방문자 수] {contents.get('poiName', '')} (POI ID: {contents.get('poiId', '')})\n"
        )
        for item in visit_list:
            result += (
                f"- 일자: {item.get('date', '')}, 방문자 수: {item.get('approxVisitorCount', '')}\n"
            )
        return result
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_place_daily_visit_count (poi_id={params.poi_id})")

class PlaceAgeDistributionInput(BaseModel):
    poi_id: str = Field(..., description="관심 장소(POI) ID")

@mcp.tool()
def get_place_age_distribution(poi_id: str) -> str:
    """
    특정 장소 방문자 연령 분포를 제공합니다. (SK OpenAPI)
    Args:
        poi_id: 관심 장소(POI) ID (예: '10067845')
    """
    params = PlaceAgeDistributionInput(poi_id=poi_id)
    endpoint = f"place/visit/seg/stat/daily/pois/{params.poi_id}"
    try:
        response = sk_client.get(endpoint)
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        contents = data.get("contents", {})
        stat_list = contents.get("stat", [])
        if not stat_list:
            return f"방문자 연령 분포 정보가 없습니다. (poiId={params.poi_id})"
        result = (
            f"[방문자 연령 분포] {contents.get('poiName', '')} (POI ID: {contents.get('poiId', '')})\n"
            f"통계 기간: {contents.get('statStartDate', '')} ~ {contents.get('statEndDate', '')}\n"
        )
        for item in stat_list:
            gender = item.get('gender', '')
            ageGrp = item.get('ageGrp', '')
            rate = item.get('rate', '')
            result += (
                f"- 성별: {gender}, 연령대: {ageGrp}, 비율: {rate}%\n"
            )
        return result
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_place_age_distribution (poi_id={params.poi_id})")

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
