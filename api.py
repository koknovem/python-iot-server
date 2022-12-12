import requests

baseUrl = "http://192.168.3.22"

def jsonToRequestUrl(json, fileName):
	returnValue = f"/{fileName}?"
	for item in json:
		returnValue += item + "=" + json[item] + "&"
	if returnValue[-1] == "&":
		returnValue = returnValue[:-1]
	return returnValue



def getRequest(url):
    return requests.get(url)


def postRequest(url, json, headers):
    return requests.post(url, json=json, headers=headers)

def getHeatmap():
    paramJson = {
        "msubmenu": "heatmap",
        "action": "view",
    }
    url = baseUrl + jsonToRequestUrl(paramJson, "stw-cgi/eventsources.cgi")
    print(url)
    res = getRequest(url)
    return res