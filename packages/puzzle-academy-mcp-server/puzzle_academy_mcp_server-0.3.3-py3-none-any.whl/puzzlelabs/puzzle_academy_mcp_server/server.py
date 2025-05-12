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
mcp = FastMCP("academy")

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

class AcademyInfoInput(BaseModel):
    academy_name: str = Field(..., description="학원 이름(예: '강남대성학원')")   

@mcp.tool()
def get_academy_info(academy_name: str) -> str:
    """
    퍼즐 학원 API를 사용하여 학원 정보를 조회합니다.
    
    Args:
        academy_name: 학원 이름(예: '강남대성학원')
    """

    params = AcademyInfoInput(academy_name=academy_name)
    
    base_url = "https://puzzle-hub-prd.data-puzzle.com/api/puzzle-data-service/academy/meta"
    query_params = {
        "name": params.academy_name,
        "limit": "5"  # Example value
    }
    headers = {
        "accept": "application/json;charset=UTF-8"
    }
    try:
        response = httpx.get(base_url, params=query_params, headers=headers)
        response.raise_for_status()
        return f"Academy info for {params.academy_name}: {response.text}"
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_academy_info (academy_name={params.academy_name})")

class AcademyRankingInput(BaseModel):
    yp_id: str = Field(..., description="학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)")
    
@mcp.tool()
def get_academy_ranking(yp_id: str) -> str:
    """
    특정 학원의 통화 통계 기반 인기 순위를 조회합니다.
    
    Args:
        yp_id: 학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)
    """
    params = AcademyRankingInput(yp_id=yp_id)
    
    try:
        response = sk_client.get(f"academy/ranking/yps/{params.yp_id}")
        return response.text
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_academy_ranking (yp_id={params.yp_id})")


class MonthlyCallStatInput(BaseModel):
    yp_id: str = Field(..., description="학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)")

@mcp.tool()
def get_academy_monthly_call_stat(yp_id: str) -> str:
    """
    최근 1년간 학원과 통화한 신규, 기존 고객수를 조회합니다.
    
    Args:
        yp_id: 학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)
    """
    params = MonthlyCallStatInput(yp_id=yp_id)
    
    try:
        response = sk_client.get(f"academy/analytics/call-count/stat/monthly/yps/{params.yp_id}")
        return response.text
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_academy_monthly_call_stat (yp_id={params.yp_id})")


class DistrictAcademyRankingInput(BaseModel):
    district_code: str = Field(..., description="학원 순위를 조회할 읍면동의 법정동 코드(예: '1147010200'은 서울특별시 양천구 목동)")
    category: str = Field(..., description="학원 분류(preparatory: 입시/고시, english: 영어, foreign: 외국어, math: 수학전문, art: 미술, music: 음악, entertainment: 예체능, etc: 기타, all: 전체)")
    school_age: str = Field(..., description="학령(high: 고등학생, middle: 중학생, elementary: 초등학생, preschool: 영유아, univ: 대학생, all: 전체)")

@mcp.tool()
def get_district_academy_ranking(district_code: str, category: str, school_age: str) -> str:
    """
    읍면동 내 지역 학원들의 순위를 조건별로 조회합니다.
    
    Args:
        district_code: 학원 순위를 조회할 읍면동의 법정동 코드(예: '1147010200'은 서울특별시 양천구 목동)
        category: 학원 분류(preparatory: 입시/고시, english: 영어, foreign: 외국어, math: 수학전문, art: 미술, music: 음악, entertainment: 예체능, etc: 기타, all: 전체)
        school_age: 학령(high: 고등학생, middle: 중학생, elementary: 초등학생, preschool: 영유아, univ: 대학생, all: 전체)
    """
    params = DistrictAcademyRankingInput(
        district_code=district_code,
        category=category,
        school_age=school_age
    )
    
    query_params = {}
    if params.category:
        query_params["category"] = params.category
    if params.school_age:
        query_params["schoolAge"] = params.school_age
    
    try:
        response = sk_client.get(f"academy/ranking/districts/{params.district_code}", params=query_params)
        return response.text
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_district_academy_ranking (district_code={params.district_code}, category={params.category}, school_age={params.school_age})")

class AcademyInflowInput(BaseModel):
    yp_id: str = Field(..., description="학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)")

@mcp.tool()
def get_academy_inflow_quartiles(yp_id: str) -> str:
    """
    학원과 거주지간의 거리로 계산한 학원 유입력을 Q1, Q2, Q3 사분위값으로 제공합니다.
    Args:
        yp_id: 학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)
    """
    params = AcademyInflowInput(yp_id=yp_id)
    try:
        response = sk_client.get(f"academy/analytics/home-distance/yps/{params.yp_id}")
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        stat = data.get("contents", {}).get("stat", {})
        q1 = stat.get("distanceQ1")
        q2 = stat.get("distanceQ2")
        q3 = stat.get("distanceQ3")
        year_month = data.get("contents", {}).get("yearMonth")
        stat_start = data.get("contents", {}).get("statStartDate")
        stat_end = data.get("contents", {}).get("statEndDate")
        return (
            f"학원 유입력 (사분위값)\n"
            f"- Q1: {q1} km\n"
            f"- Q2(중위값): {q2} km\n"
            f"- Q3: {q3} km\n"
            f"- 기준 년월: {year_month}, 기간: {stat_start} ~ {stat_end}"
        )
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_academy_inflow_quartiles (yp_id={params.yp_id})")

class DistrictInflowInput(BaseModel):
    district_code: str = Field(..., description="학원 유입력을 조회할 읍면동의 법정동 코드(예: '1147010200')")
    school_age: str = Field(..., description="학령(high: 고등학생, middle: 중학생, elementary: 초등학생, preschool: 영유아)")

@mcp.tool()
def get_district_inflow_quartiles(district_code: str, school_age: str) -> str:
    """
    학원 유입력의 읍면동 지역 평균을 Q1, Q2, Q3 사분위값으로 제공합니다.
    Args:
        district_code: 학원 유입력을 조회할 읍면동의 법정동 코드(예: '1147010200')
        school_age: 학령(high: 고등학생, middle: 중학생, elementary: 초등학생, preschool: 영유아)
    """
    params = DistrictInflowInput(district_code=district_code, school_age=school_age)
    query_params = {"schoolAge": params.school_age}
    try:
        response = sk_client.get(f"academy/analytics/home-distance/districts/{params.district_code}", params=query_params)
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        stat = data.get("contents", {}).get("stat", {})
        q1 = stat.get("distanceQ1")
        q2 = stat.get("distanceQ2")
        q3 = stat.get("distanceQ3")
        year_month = data.get("contents", {}).get("yearMonth")
        stat_start = data.get("contents", {}).get("statStartDate")
        stat_end = data.get("contents", {}).get("statEndDate")
        district_name = data.get("contents", {}).get("districtName")
        return (
            f"지역 학원 유입력 (사분위값)\n"
            f"- 지역: {district_name}\n"
            f"- Q1: {q1} km\n"
            f"- Q2(중위값): {q2} km\n"
            f"- Q3: {q3} km\n"
            f"- 기준 년월: {year_month}, 기간: {stat_start} ~ {stat_end}"
        )
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_district_inflow_quartiles (district_code={params.district_code}, school_age={params.school_age})")

class SimilarAcademiesInput(BaseModel):
    yp_id: str = Field(..., description="학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)")

@mcp.tool()
def get_similar_academies(yp_id: str) -> str:
    """
    특정 학원과 함께 알아보는(유사도 기반) 학원 목록을 조회합니다.
    Args:
        yp_id: 학원 코드(예: '3650775'는 시대인재학원 입시R&D센터)
    """
    params = SimilarAcademiesInput(yp_id=yp_id)
    try:
        response = sk_client.get(f"academy/analytics/similar/yps/{params.yp_id}")
        data = response.json()
        if data.get("status", {}).get("code") != "00":
            return f"API 오류: {data.get('status', {}).get('message', 'Unknown error')}"
        contents = data.get("contents", {})
        base_info = (
            f"조회 학원명: {contents.get('ypName')}\n"
            f"분류: {contents.get('category')}\n"
            f"기간: {contents.get('statStartDate')} ~ {contents.get('statEndDate')} (기준 년월: {contents.get('yearMonth')})\n"
        )
        stat_list = contents.get("stat", [])
        if not stat_list:
            return base_info + "\n함께 알아보는 유사 학원 정보가 없습니다."
        result = base_info + "\n함께 알아보는 학원 Top 5:\n"
        for idx, item in enumerate(stat_list, 1):
            result += (
                f"{idx}. {item.get('ypName')} (분류: {item.get('category')}, 유사도: {item.get('similarity'):.2f})\n"
            )
        return result
    except httpx.HTTPError as e:
        return handle_httpx_error(e, f"get_similar_academies (yp_id={params.yp_id})")

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
