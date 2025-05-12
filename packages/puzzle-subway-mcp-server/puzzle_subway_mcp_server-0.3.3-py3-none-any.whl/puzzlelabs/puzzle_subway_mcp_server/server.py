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
mcp = FastMCP("subway")

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

class RealTimeCongestionInput(BaseModel):
    station_name: str = Field(..., description="지하철역 이름")

@mcp.tool()
def get_subway_real_time_congestion(station_name: str) -> str:
    """
    특정 역으로 진입하는 열차의 실시간 혼잡도를 조회합니다.
    
    Args:
        station_name: 지하철역 이름
    """
    
    params = RealTimeCongestionInput(station_name=station_name)
    
    base_url = "http://alb-diaas-pzl-dev-1196007480.ap-northeast-2.elb.amazonaws.com:3000"
    endpoint = f"/subway-qa/congestion-car-rltm/{params.station_name}"
    
    try:
        response = httpx.get(
            f"{base_url}{endpoint}",
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        return f"Congestion data for {params.station_name} station: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_real_time_congestion (station_name={params.station_name})")


class StationInfoInput(BaseModel):
    station_name: str = Field(..., description="지하철역 이름(예: '강남역')")

@mcp.tool()
def get_subway_station_info(station_name: str) -> str:
    """
    퍼즐 지하철 API를 사용하여 지하철역 정보를 조회합니다.
    
    Args:
        station_name: 지하철역 이름(예: '강남역')
    """

    params = StationInfoInput(station_name=station_name)
    
    base_url = "https://puzzle-hub-prd.data-puzzle.com/api/puzzle-data-service/subway/subway-stations"
    query_params = {
        "name": params.station_name,
        "type": "skt",  # Example value
        "limit": "5"  # Example value
    }
    headers = {
        "accept": "application/json;charset=UTF-8"
    }
    try:
        response = httpx.get(base_url, params=query_params, headers=headers)
        response.raise_for_status()
        return f"Station info for {params.station_name}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_station_info (station_name={params.station_name})")

class TrainCongestionInput(BaseModel):
    stationCode: str = Field(..., description="역 코드 (e.g., '221' for 역삼역)")
    dow: str = Field(..., description="요일 (e.g., 'MON', 'TUE', etc.). 미입력 시 현재 요일")
    hh: str = Field(..., description="시간 (e.g., '08' for 8:00-8:59). 미입력 시 현재 시간")

@mcp.tool()
def get_subway_train_congestion(stationCode: str, dow: str, hh: str) -> str:
    """
    특정 역으로 진입하는 열차의 혼잡도를 제공합니다.
    
    Args:
        stationCode: 역 코드 (예: '221'은 역삼역)
        dow: 검색 기준 요일 (예: 'MON', 'TUE' 등, 미입력 시 현재 요일)
        hh: 검색 기준 시간 (예: '08'은 8:00-8:59, 미입력 시 현재 시간)
    """
    
    params = TrainCongestionInput(stationCode=stationCode, dow=dow, hh=hh)
    
    query_params = {
        "dow": params.dow,
        "hh": params.hh
    }

    try:
        response = sk_client.get(f"/subway/congestion/stat/train/stations/{params.stationCode}", params=query_params)
        return f"Train congestion data for station {params.stationCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_train_congestion (stationCode={params.stationCode})")

class CarCongestionInput(BaseModel):
    stationCode: str = Field(..., description="역 코드 (e.g., '133' for 서울역)")
    dow: str = Field(..., description="요일 (e.g., 'MON', 'TUE', etc.). 미입력 시 현재 요일")
    hh: str = Field(..., description="시간 (e.g., '08' for 8:00-8:59). 미입력 시 현재 시간")

@mcp.tool()
def get_subway_car_congestion(stationCode: str, dow: str, hh: str) -> str:
    """
    특정 역으로 진입하는 열차의 칸별 혼잡도를 제공합니다.
    
    Args:
        stationCode: 역 코드 (예: '133'은 서울역)
        dow: 검색 기준 요일 (예: 'MON', 'TUE' 등, 미입력 시 현재 요일)
        hh: 검색 기준 시간 (예: '08'은 8:00-8:59, 미입력 시 현재 시간)
    """
    
    params = CarCongestionInput(stationCode=stationCode, dow=dow, hh=hh)
    
    query_params = {
        "dow": params.dow,
        "hh": params.hh
    }

    try:
        response = sk_client.get(f"/subway/congestion/stat/car/stations/{params.stationCode}", params=query_params)
        return f"Car congestion data for station {params.stationCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_car_congestion (stationCode={params.stationCode})")

class CarExitRateInput(BaseModel):
    stationCode: str = Field(..., description="역 코드 (e.g., '133' for 서울역)")
    dow: str = Field(..., description="요일 (e.g., 'MON', 'TUE', etc.). 미입력 시 현재 요일")
    hh: str = Field(..., description="시간 (e.g., '08' for 8:00-8:59). 미입력 시 현재 시간")

@mcp.tool()
def get_subway_car_exit_rate(stationCode: str, dow: str, hh: str) -> str:
    """
    특정 역으로 진입하는 열차에서 하차한 인원의 칸별 하차 비율을 제공합니다. 
    
    Args:
        stationCode: 역 코드 (예: '133'은 서울역)
        dow: 검색 기준 요일 (예: 'MON', 'TUE' 등, 미입력 시 현재 요일)
        hh: 검색 기준 시간 (예: '08'은 8:00-8:59, 미입력 시 현재 시간)
    """
    
    params = CarExitRateInput(stationCode=stationCode, dow=dow, hh=hh)
    
    query_params = {
        "dow": params.dow,
        "hh": params.hh
    }

    try:
        response = sk_client.get(f"/subway/congestion/stat/get-off/stations/{params.stationCode}", params=query_params)
        return f"Car exit rate data for station {params.stationCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_car_exit_rate (stationCode={params.stationCode})")

# 요일별 지하철역 출구 통행자 수
class ExitTrafficByDowInput(BaseModel):
    stationCode: str = Field(..., description="역 코드 (e.g., '221' for 역삼역)")
    gender: str = Field('all', description="성별 필터 ('male', 'female', 'all'). 기본값 'all'.")
    ageGrp: str = Field('all', description="연령대 필터 ('10', '20', '30', '40', '50', '60_over', 'all'). 기본값 'all'.")
    dow: Optional[str] = Field(None, description="요일 (e.g., 'MON', 'TUE', etc.). 미입력 시 현재 요일")

@mcp.tool()
def get_subway_exit_traffic_by_dow(stationCode: str, gender: str, ageGrp: str, dow: str) -> str:
    """
    최근 3개월 내 해당 지하철역 출구를 이용한 고유한 통행자 수를 제공합니다. 
    
    Args:
        stationCode: 역 코드 (예: '221'은 역삼역)
        gender: 성별 필터 ('male', 'female', 'all' - 기본값 'all')
        ageGrp: 연령대 필터 ('10', '20', '30', '40', '50', '60_over', 'all' - 기본값 'all')
        dow: 요일 (예: 'MON', 'TUE' 등, 미입력 시 현재 요일)
    """
    
    params = ExitTrafficByDowInput(stationCode=stationCode, dow=dow, gender=gender, ageGrp=ageGrp)
    
    query_params = {
        "gender": params.gender,
        "ageGrp": params.ageGrp,
        "dow": params.dow
    }

    try:
        response = sk_client.get(f"/subway/exit/stat/dow/stations/{params.stationCode}", params=query_params)
        return f"Exit traffic data for station {params.stationCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_exit_traffic_by_dow (stationCode={params.stationCode})")

class ExitTrafficByHourInput(BaseModel):
    stationCode: str = Field(..., description="The station code (e.g., '221' for 역삼역)")
    gender: str = Field('all', description="Gender to filter by ('male', 'female', 'all'). Defaults to 'all'.")
    ageGrp: str = Field('all', description="Age group to filter by ('10', '20', '30', '40', '50', '60_over', 'all'). Defaults to 'all'.")
    date: str = Field('latest', description="Date to filter by in YYYYMMDD format or 'latest' for the most recent date. Defaults to 'latest'.")

@mcp.tool()
def get_subway_exit_traffic_by_hour(stationCode: str, gender: str, ageGrp: str, date: str) -> str:
    """
    특정 일자의 해당 지하철역 출구를 이용한 적이 있는 고유한 통행자 수를 시간대로 구분하여 제공합니다.
    
    Args:
        stationCode: 역 코드 (예: '221'은 역삼역)
        gender: 성별 필터 ('male', 'female', 'all' - 기본값 'all')
        ageGrp: 연령대 필터 ('10', '20', '30', '40', '50', '60_over', 'all' - 기본값 'all')
        date: 조회할 날짜 (YYYYMMDD 형식 또는 'latest' - 기본값 'latest')
    """
    
    params = ExitTrafficByHourInput(stationCode=stationCode, gender=gender, ageGrp=ageGrp, date=date)
    
    query_params = {
        "gender": params.gender,
        "ageGrp": params.ageGrp,
        "date": params.date
    }

    try:
        response = sk_client.get(f"/subway/exit/raw/hourly/stations/{params.stationCode}", params=query_params)
        return f"Hourly exit traffic data for station {params.stationCode}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_subway_exit_traffic_by_hour (stationCode={params.stationCode})")

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
