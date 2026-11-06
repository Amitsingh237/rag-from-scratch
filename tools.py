from datetime import datetime
import requests
import json
from Utilities.utilities import log
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d  %H:%M:%S")

def get_city_weather(city):
      url=f"https://wttr.in/{city}?format=3"
      response=requests.get(url,timeout=10)
      response.raise_for_status()
      return response.text

def get_user_city():
     return "Bangalore"


def run_tool(tool_call):
        func_name = tool_call.function.name
        func_args = {}
     
        try:
            func_args = json.loads(tool_call.function.arguments or "{}")
            log(f" {func_name} ({func_args})")
            fn = FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
            result = fn(**func_args)
     
        except Exception as e:
            result = f"Error while running {func_name}: {e}"
     
        log(f"  {result}")
        return str(result)


TOOLS=[
    {
        "type":"function",
        "function":{
            "name":"get_current_time",
            "description":"Returns the current data and time as a formatted string. ",
            "parameters":{"type":"object","properties":{}}
        }
    }
    ,{
        "type":"function",
        "function":{
            "name":"get_city_weather",
            "description":"returns the current weather of a given city",
            "parameters":{
                "type":"Object",
                "properties":{
                    "city":{
                        "type":"string",
                        "description":"city to get the weather for"
                    }
                },
                "required":["city"]
            }
        }
    },
    {
         "type":"function",
         "function":{
              "name":"get_user_city",
              "description":"return  the city where the user lives.Use this when the user says 'my city','where i live or 'my location' without naming the city ",
              "parameters":{
                   "type":"object",
                   "properties":{}
              }
         }
    }
]

FUNCTION_NAME_TO_FUNCTION_MAP={
    "get_current_time":get_current_time,
    "get_city_weather":get_city_weather,
    "get_user_city": get_user_city
}


