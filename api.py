import json
from urllib.request import urlopen
import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np

baseUrl = "http://192.168.3.22"
auth = HTTPDigestAuth('admin', 'A@dmin$2017')


def jsonToRequestUrl(json, fileName):
    returnValue = f"/stw-cgi/{fileName}?"
    for item in json:
        returnValue += item + "=" + str(json[item]) + "&"
    if returnValue[-1] == "&":
        returnValue = returnValue[:-1]
    return returnValue

def getJsonFromWeb(webResult):
    resJsonString = ""
    for row in webResult.text.split("\r\n")[:-1]:
        data = row.split("=")
        resJsonString += f"\"{data[0]}\": \"{data[1]}\","
    resJson = "{" + resJsonString[:-1] + "}"
    resJson = json.loads(resJson)
    return resJson


def getRequest(url):
    print(url)
    return requests.get(url, auth=auth)


def postRequest(url, json, headers):
    return requests.post(url, json=json, headers=headers)


def getAPIbyJson(paramJson, cgiFilename="eventsources.cgi"):
    url = baseUrl + jsonToRequestUrl(paramJson, cgiFilename)
    res = getRequest(url)
    return res

def getUrlPath(paramJson, cgiFilename):
    return baseUrl + jsonToRequestUrl(paramJson, cgiFilename)

#Deprecated: digest auth has been handled by requests.auth
def resolveDigestData(json):
    auths = json['WWW-Authenticate'].split(",")
    for i in range(len(auths)):
        auths[i] = auths[i].split("=")[1].replace("\"", "")
    realm = auths[0]
    nonce = auths[2]
    qop = auths[3]
    return {
        "realm": realm,
        "nonce": nonce,
        "qop": qop
    }


def getHeatmap(paramJson=""):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == ""):
        paramJson = {
            "msubmenu": "heatmap",
            "action": "view",
        }
    res = getAPIbyJson(paramJson)
    resJson = getJsonFromWeb(res)
    return resJson

def getPeoplecount(paramJson=""):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == ""):
        paramJson = {
            "msubmenu": "peoplecount",
            "action": "view",
        }
    res = getAPIbyJson(paramJson)
    resJson = getJsonFromWeb(res)
    return resJson

def showCameraStream(paramJson=""):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == ""):
        paramJson = {
            "msubmenu": "stream",
            "action": "view",
            "Profile": "1",
            "CodecType": "MJPEG",
            "Resolution": "800x450",
            "FrameRate": "15",
            "CompressionLevel": "10"
        }
    url = getUrlPath(paramJson, "video.cgi")
    stream = urlopen(url).headers
    print(stream)