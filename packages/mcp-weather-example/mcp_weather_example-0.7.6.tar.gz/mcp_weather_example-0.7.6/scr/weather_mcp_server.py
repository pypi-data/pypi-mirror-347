# _*_ coding : utf-8 _*_
# @Time : 2025-05-01 20:16
# @Author : liubiao
# @File : weather-mcp-server
# @Project : mcp-weather-example
import json


from mcp.server.fastmcp import FastMCP
import requests
from httpx import HTTPStatusError
import httpx

mcp = FastMCP("WeatherServer")

# 接入的是心知天气
OPEN_WEATHER_URL = "https://api.seniverse.com/v3/weather/now.json"

#
# key	String	无	是	你的 API 密钥
# location	Location	无	是	所查询的位置
# language	Language	zh-Hans	否	语言
# unit	Unit	c	否	单位
#
API_KEY = "P7qum_9iZqQjjIc__"
API_SECRET = "Svl7bpz0DoweZftVR"
USER_AGENT="weather-app/1.0"


def search_weather(city):

    params = {
        "key": API_SECRET,
        "location": city,
        "language": "zh-Hans",
        "unit": "c",
    }

    headers = {
        "User-Agent": USER_AGENT,
    }


    try:
        response = requests.get(OPEN_WEATHER_URL, params=params, headers=headers,verify=False)
        response.encoding = "utf-8"
        response.raise_for_status()
        j =  json.loads(response.text)
        return j
    except httpx.HTTPStatusError as e:
        print(e)
        return {"error":f"HTTP 错误: {e.response.status_code}" }

    except Exception as e:
        print(e)
        return {"error":f"<UNK>: {e}" }



def weather_format(weather_api_res_json):
    # print(json.dumps( weather_api_res_json))
    print(json.dumps(weather_api_res_json,ensure_ascii=False,indent=4))

    print(weather_api_res_json["results"][0]["location"]["name"])


    city = weather_api_res_json["results"][0]["location"]["name"]
    temp = weather_api_res_json["results"][0]["now"]["temperature"]
    text  = weather_api_res_json["results"][0]["now"]["text"]
    return ( f" {city} \n"
             f" 温度: {temp} ℃ \n"
             f" 天气: {text} \n")


def fetch_weather(city):
    res = search_weather(city)
    weather_data = weather_format(res)
    return weather_data

def main():
    print("启动 weather server")
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()


# 声明这个方法为mcp
@mcp.tool()
def query_weather(city:str) -> str :
    data = fetch_weather(city)
    return data

