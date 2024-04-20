import requests
import time


def poet(x):
    url = "https://robotext.io/create-write-job/poem"
    payload = {"radio": "value1",
               'keys': x}
    headers = {
        'Authorization': 'Bearer 25a04608-5679-49f3-bde6-30ea4c116510'

    }
    url1 = "https://robotext.io/ping-write-job"
    response = requests.request("POST", url, headers=headers, data=payload)
    response1 = response.json()

    url2 = url1 + "?job_id=" + str(response1["job_id"])
    response2 = requests.get(url2, "result")
    response3 = response2.json()
    while response3["status"] != "completed":
        time.sleep(15)
        response2 = requests.get(url2, "result")
        response3 = response2.json()

    return response3["result"]


print(poet(input()))
