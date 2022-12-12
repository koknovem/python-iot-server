import requests

baseUrl = "http://192.168.3.22"

def jsonToRequestUrl(json, fileName):
	returnValue = f"/stw-cgi/{fileName}?"
	for item in json:
		returnValue += item + "=" + str(json[item]) + "&"
	if returnValue[-1] == "&":
		returnValue = returnValue[:-1]
	return returnValue



def getRequest(url):
    return requests.get(url)


def postRequest(url, json, headers):
    return requests.post(url, json=json, headers=headers)

def getAPIbyJson(paramJson, basePath):
    url = baseUrl + jsonToRequestUrl(paramJson, basePath)
    res = getRequest(url)
    return res

def getHeatmap(paramJson=""):
    if(paramJson == ""):
        paramJson = {
            "msubmenu": "heatmap",
            "action": "view",
        }
    res = getAPIbyJson(paramJson, "eventsources.cgi")
    return res

def getPeopleCount(paramJson=""):
    if(paramJson == ""):
        paramJson = {
            "msubmenu": "peoplecount",
            "action": "view",
            "channel": 0,
        }
    res = getAPIbyJson(paramJson, "eventsources.cgi")
    return res