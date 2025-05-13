from mcp.server.fastmcp import FastMCP

import requests
import json
from typing import Tuple, List
import pandas as pd
import matplotlib.pyplot as plt
import os

# Create an MCP server
mcp = FastMCP("oppo-eap-mcp-server")


def auth(account: str, password: str, area: str) -> Tuple[str, str]: 
    """
        Use account and password to authenticate a user to get two tokens splitted by line
        Args:
            account: Account name
            password: Password
            area: Area code, 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
        Returns:
            Tuple[str, str]: tuple of Two string-type tokens 
    """

    assert(area == "zh" or area == "yd" or area == "dny"), f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'"

    url = "http://thirdpart.myoas.com/thirdpart-leida/common/getSessionKey"

    payload = json.dumps({
            "username": account,
            "password": password,
            "area": area
        })
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code != 200 or response.json()["code"] != 200:
        raise Exception(f"Error: username or password error, status code: {response.status_code}")
    response_json = response.json()
    
    if response_json["code"] != 200:
        raise Exception(f"Error: username or password error, status code: {response_json}")
    
    tgt = response_json["data"]["tgt"]
    token = response_json["data"]["token"]

    return (tgt, token)

def post(area: str, url: str, headers: dict = {}, data: dict = {}) -> str:
    """
        Send a request to the server
        Args:
            area: which area to query. 'zh' for china, 'yd' for india, 'dny' for southeast asia. don't accept other area code
            url: URL of the server
            headers: Additional Header of the request
            data: Data of the request
        Returns:
            str: Response from the server
    """
    Authorization_qodp, SessionKey = auth(USERNAME, PASSWORD, area)

    default_headers = {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json;charset=UTF-8',
        'Authorization': Authorization_qodp,
        'Session-Key': SessionKey
    }

    default_headers.update(headers)
    payload = json.dumps(data)
    response = requests.request("POST", url, headers=default_headers, data=payload)
    if response.status_code != 200:
        raise Exception(f"access {url} error with post request: status code {response.status_code}")
    response_json = response.json()
    if response_json["code"] != 200:
        raise Exception(f"access {url} error with post request: status code {response_json}")
    
    return response_json

@mcp.tool()
def get_models_information(area: str) -> str:
    """
    Get models information list for a specified area.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia, 'om' for Europe. Only these codes are accepted.
    
    Returns:
        str: List of models information, separated by lines. Each line is in the format: model name; market name; series name; go to market time
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/indexBoard/getModelOta2"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/indexBoard/getModelOta2"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/indexBoard/getModelOta2"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    data = {
        "gifOta": False,
        "models":[],
        "userNum": USERNAME,
        "isAdmin":0
    }

    response_json = post(area, url, headers={}, data=data)
    response_data =  response_json["data"]

    merged_data = []
    for series in response_data.values():
        for item in series:
            merged_item = {
                "model": item["model"],
                "marketName": item["marketName"],
                "series": item["series"],
                "marketTime": item["marketTime"]
            }
            merged_data.append(merged_item)
    
    return_data = []
    for series in response_data.values():
        for item in series:
            merged_item = f"{item['model']}; {item['marketName']}; {item['series']}; {item['marketTime']}"
            return_data.append(merged_item)

    return "\n".join(return_data)

@mcp.tool()
def get_ota_version_list_by_model_name(area: str, model_name: str) -> str:
    """
    Get OTA version list by model name for a specified area.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia. Only these codes are accepted.
        model_name (str): Model name, such as PKP110.
    
    Returns:
        str: List of OTA versions, separated by lines. Each line is in the format: otaVersion; versionDate; number of users in this OTA version
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/pbi/getOtaVersionByModels"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    data = {
            "models":[ model_name ],
            "isPre": None,
            "sort":1
        }

    response_json = post(area, url, data=data)
    version_list = response_json["data"][0]["otaConditionVos"]

    return_data = []
    for version in version_list:
        return_data.append(f"{version['otaVersion']}; {version['versionDate']}; {version['uv']}")

    return "\n".join(return_data)

@mcp.tool()
def today() -> str:
    """
    Get today's date in the format YYYY-MM-DD.
    
    Returns:
        str: Today's date in the format YYYY-MM-DD
    """
    from datetime import datetime
    today = datetime.today().strftime('%Y-%m-%d')
    return today

def fetch_crash_or_anr_trend_df(
        area: str,
        exceptionType: int,
        model: str,
        otaVersion: str,
        applicationType: int,
        startDate: str,
        endDate: str,
        dataType: int,
        queryType: int,
        foregroundType: int,
        availableRate: str
    ) -> pd.DataFrame:
    """
        Fetch crash or ANR trend data and return as a pandas DataFrame.
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/sys/available/overview/crashanr/trend"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/sys/available/overview/crashanr/trend"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/sys/available/overview/crashanr/trend"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    if otaVersion or otaVersion.strip() != "":
        otaVerList = [otaVersion]
    else:
        otaVerList = []

    data = {
        "excepType": exceptionType,
        "models": [
            {
                "model": model.strip(),
                "otaVerList": otaVerList
            }
        ],
        "self": applicationType,
        "dateType": 8,
        "startDate": startDate,
        "endDate": endDate,
        "order": "asc",
        "dataType": dataType,
        "systemType": queryType,
        "foreGround": foregroundType,
        "download": 2,
        "isTotal": 0,
        "memoryDeviceVersionList": [],
        "storageDeviceVersionList": [],
        "storageSizeList": []
    }

    if availableRate or availableRate.strip() != "":
        data["availableRateList"] = [ availableRate ]
    else:
        data["availableRateList"] = []

    response_json = post(area, url, data=data)
    response_data = response_json["data"]
    y_data = response_data["yAxisData"][0]
    x_data = response_data["xAxisData"]
    df = pd.DataFrame({"date": x_data, "value": y_data})
    return df

@mcp.tool()
def get_crash_or_anr_trend(
        area: str,
        exceptionType: int,
        model: str,
        otaVersion: str,
        applicationType: int,
        startDate: str,
        endDate: str,
        dataType: int,
        queryType: int,
        foregroundType: int,
        availableRate: str
    ) -> str:
    """
    Query crash or ANR trend and return as Model Context Protocol-compatible string.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia. Only these codes are accepted.
        exceptionType (int): 0 for crash, 1 for ANR.
        model (str): Model name, such as PKP110. Do not use market name.
        otaVersion (str): OTA version, such as PKP110_11_A.11.1.1.1_2023-10-01. Empty string for all versions.
        applicationType (int): 1 for system application, 2 for third party application, 3 for all applications.
        startDate (str): Start date, format YYYY-MM-DD.
        endDate (str): End date, format YYYY-MM-DD.
        dataType (int): 0 for error times, 1 for error affected users, 2 for error rate, 3 for error affected users rate.
        queryType (int): 1 for querying by model, 2 for query by model and otaVersion.
        foregroundType (int): 1 for foreground, 2 for background, 3 for all.
        availableRate (str): Storage usage rate, e.g., "", "0~10%", "10%~25%", "25%~50%", "50%~100%".
    
    Returns:
        str: List of crash or ANR trend, separated by lines. Each line is in the format: date; value
    """
    df = fetch_crash_or_anr_trend_df(
        area, exceptionType, model, otaVersion, applicationType, startDate, endDate, dataType, queryType, foregroundType, availableRate
    )
    return "\n".join([f"{row['date']}; {row['value']}" for _, row in df.iterrows()])

@mcp.tool()
def plot_crash_or_anr_trend_chart(
        area: str,
        exceptionType: int,
        model: str,
        otaVersion: str,
        applicationType: int,
        startDate: str,
        endDate: str,
        dataType: int,
        queryType: int,
        foregroundType: int,
        availableRate: str,
        window_size: int = 7
    ) -> str:
    """
    Generate and save a crash or ANR trend line chart with anomaly points marked (using IQR method), and return the absolute file path to the image. LLMs and clients should display or render the image at the returned path.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia. Only these codes are accepted.
        exceptionType (int): 0 for crash, 1 for ANR.
        model (str): Model name, such as PKP110. Do not use market name.
        otaVersion (str): OTA version, such as PKP110_11_A.11.1.1.1_2023-10-01. Empty string for all versions.
        applicationType (int): 1 for system application, 2 for third party application, 3 for all applications.
        startDate (str): Start date, format YYYY-MM-DD.
        endDate (str): End date, format YYYY-MM-DD.
        dataType (int): 0 for error times, 1 for error affected users, 2 for error rate, 3 for error affected users rate.
        queryType (int): 1 for querying by model, 2 for query by model and otaVersion.
        foregroundType (int): 1 for foreground, 2 for background, 3 for all.
        availableRate (str): Storage usage rate, e.g., "", "0~10%", "10%~25%", "25%~50%", "50%~100%".
        window_size (int, optional): Number of left-side non-anomaly points to use for IQR calculation. Default is 7.
    
    Returns:
        str: Absolute path to the generated chart image file. LLMs and clients should display or render the image at this path.
    """
    df = fetch_crash_or_anr_trend_df(
        area, exceptionType, model, otaVersion, applicationType, startDate, endDate, dataType, queryType, foregroundType, availableRate
    )
    values = df['value'].tolist()
    dates = df['date'].tolist()
    anomalies = [False] * len(values)
    for i in range(len(values)):
        # Collect previous window_size non-anomaly points
        left_indices = []
        j = i - 1
        while j >= 0 and len(left_indices) < window_size:
            if not anomalies[j]:
                left_indices.append(j)
            j -= 1
        if len(left_indices) < window_size:
            continue  # Not enough left-side non-anomaly points, skip anomaly detection for this point
        window_vals = [values[j] for j in reversed(left_indices)]
        q1 = pd.Series(window_vals).quantile(0.25)
        q3 = pd.Series(window_vals).quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        if values[i] > upper:
            anomalies[i] = True
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', label='Value')
    # Mark anomalies
    anomaly_dates = [dates[i] for i, a in enumerate(anomalies) if a]
    anomaly_values = [values[i] for i, a in enumerate(anomalies) if a]
    if anomaly_dates:
        plt.scatter(anomaly_dates, anomaly_values, color='red', label='Anomaly', zorder=5)
    plt.title('Crash/ANR Trend')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    output_dir = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(output_dir, f"crash_anr_trend_{model}_{exceptionType}_{dataType}.png")
    plt.savefig(output_path)
    plt.close()
    return output_path

def fetch_active_users_trend_df(
        area: str,
        model: str,
        startDate: str,
        endDate: str,
        otaVersion: str = ''
    ) -> pd.DataFrame:
    """
        Fetch active users trend data and return as a pandas DataFrame.
    """
    if area == "zh":
        url = "https://eap.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    elif area == "yd":
        url = "https://eap-in.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    elif area == "dny":
        url = "https://eap-sg.oppoer.me/stage-api/sys/performance/analyse/standby/getActiveTrend"
    else:
        raise Exception(f"Error: area code {area} is not supported, please use 'zh', 'yd', 'dny'")

    if otaVersion or otaVersion.strip() != "":
        ota_version_list = [otaVersion]
    else:
        ota_version_list = []

    data = {
        "excepType": 0,
        "models": [
            {
                "model": model,
                "otaVerList": ota_version_list
            }
        ],
        "self": 3,  # 3 查询所有， 1 表示自研， 2 表示非自研
        "dateType": 8,
        "startDate": startDate,
        "endDate": endDate,
        "order": "asc",
        "dataType": 4,
        "systemType": 1,
        "download": 2,
        "isTotal": 0,
        "memoryDeviceVersionList": [],
        "storageDeviceVersionList": [],
        "storageSizeList": [],
        "availableRateList": [],
        "isCrashRestartTotal": 1
    }

    response_json = post(area, url, data=data)
    response_data = response_json["data"]
    active_users = response_data["yAxisData"][0]
    datetime = response_data["xAxisData"]
    df = pd.DataFrame({"date": datetime, "active_users": active_users})
    return df

@mcp.tool()
def get_active_users_trend(
        area: str,
        model: str,
        startDate: str,
        endDate: str,
        otaVersion: str = ''
    ) -> str:
    """
    Query active users trend and return as Model Context Protocol-compatible string.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia. Only these codes are accepted.
        model (str): Model name, such as PKP110. Do not use market name.
        startDate (str): Start date, format YYYY-MM-DD.
        endDate (str): End date, format YYYY-MM-DD.
        otaVersion (str, optional): OTA version, such as PKP110_11_A.11.1.1.1_2023-10-01. If not specified, queries all OTA versions.
    
    Returns:
        str: List of active users trend, separated by lines. Each line is in the format: date; active users
    """
    df = fetch_active_users_trend_df(area, model, startDate, endDate, otaVersion)
    return "\n".join([f"{row['date']}; {row['active_users']}" for _, row in df.iterrows()])

@mcp.tool()
def plot_active_users_trend_chart(
        area: str,
        model: str,
        startDate: str,
        endDate: str,
        otaVersion: str = '',
        window_size: int = 7
    ) -> str:
    """
    Generate and save an active users trend line chart with anomaly points marked (using IQR method), and return the absolute file path to the image. LLMs and clients should display or render the image at the returned path.
    
    Args:
        area (str): Area code, 'zh' for China, 'yd' for India, 'dny' for Southeast Asia. Only these codes are accepted.
        model (str): Model name, such as PKP110. Do not use market name.
        startDate (str): Start date, format YYYY-MM-DD.
        endDate (str): End date, format YYYY-MM-DD.
        otaVersion (str, optional): OTA version, such as PKP110_11_A.11.1.1.1_2023-10-01. If not specified, queries all OTA versions.
        window_size (int, optional): Number of left-side non-anomaly points to use for IQR calculation. Default is 7.
    
    Returns:
        str: Absolute path to the generated chart image file. LLMs and clients should display or render the image at this path.
    """
    df = fetch_active_users_trend_df(area, model, startDate, endDate, otaVersion)
    values = df['active_users'].tolist()
    dates = df['date'].tolist()
    anomalies = [False] * len(values)
    for i in range(len(values)):
        # Collect previous window_size non-anomaly points
        left_indices = []
        j = i - 1
        while j >= 0 and len(left_indices) < window_size:
            if not anomalies[j]:
                left_indices.append(j)
            j -= 1
        if len(left_indices) < window_size:
            continue  # Not enough left-side non-anomaly points, skip anomaly detection for this point
        window_vals = [values[j] for j in reversed(left_indices)]
        q1 = pd.Series(window_vals).quantile(0.25)
        q3 = pd.Series(window_vals).quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        if values[i] > upper:
            anomalies[i] = True
    plt.figure(figsize=(10, 5))
    plt.plot(dates, values, marker='o', label='Active Users')
    anomaly_dates = [dates[i] for i, a in enumerate(anomalies) if a]
    anomaly_values = [values[i] for i, a in enumerate(anomalies) if a]
    if anomaly_dates:
        plt.scatter(anomaly_dates, anomaly_values, color='red', label='Anomaly', zorder=5)
    plt.title('Active Users Trend')
    plt.xlabel('Date')
    plt.ylabel('Active Users')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()
    output_dir = os.path.abspath(os.path.dirname(__file__))
    output_path = os.path.join(output_dir, f"active_users_trend_{model}.png")
    plt.savefig(output_path)
    plt.close()
    return output_path

@mcp.prompt()
def analyze_crash_or_anr_prompt(model: str, type: str) -> str:
    """
        Prompt for analyzing crash or ANR.
        Args:
            model: model name, such as PKP110 or Market name, such as A5 Pro and so on.
            type: crash or anr
        Returns:
            str: Prompt for analyzing crash or ANR.
    """
    return """
        Role:
            You are a data analyst. You are responsible for analyzing {type} data for user
        Task:
            Given a model name: {model}, you need to analyze {type} data for this model. You need to analyze the data and give a report.
        Setup:
            If user gvies a market name, you need to find the model name first, and then analyze the {type} data for this model.
            Before you analyze the {type} data, you should figure out the datetime of today
        Details:
            1. You should analyze foreground and background {type} data separately.
            2. You should look at {type} times data for the last month, and use regression analysis to find if there is a anomaly in the trend
            3. You should look at {type} affected users data for the last month, and use regression analysis to find if there is a anomaly in the trend
            4. You should look at {type} rate data for the last month, and use regression analysis to find if there is a anomaly in the trend
            5. You should look at {type} affected users rate data for the last month, and use regression analysis to find if there is a anomaly in the trend
            6. You should plot charts for each data, and use regression analysis to mark anomaly data point in the trend
    """

def main():

    # parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="FastMCP")
    parser.add_argument("--username", type=str, required=True, help="Username")
    parser.add_argument("--password", type=str, required=True, help="Password")
    args = parser.parse_args()

    # # save username and password to global variables
    global USERNAME
    global PASSWORD
    USERNAME = args.username
    PASSWORD = args.password


    # start the server by STDIO mode
    mcp.run(transport="stdio")

if __name__ == "__main__":
   
    main()