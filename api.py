import datetime
import json
import time

import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np

host = "192.168.3.21"
lightingHost = "192.168.3.218:8888"

baseUrl = "http://" + host
lightingUrl = "http://" + lightingHost

auth = HTTPDigestAuth('admin', 'A@dmin$2017')


def getUriFromJson(paramJson, uri):
    returnValue = f"/stw-cgi/{uri}?"
    for item in paramJson:
        returnValue += item + "=" + str(paramJson[item]) + "&"
    if returnValue[-1] == "&":
        returnValue = returnValue[:-1]
    return returnValue


def getRequest(url, isUseAuth=True, isStream=False, isAcceptJson=True):
    header = {"Accept": "application/json"}
    if (isAcceptJson == False):
        header = {}
    if isUseAuth:
        return requests.get(url, auth=auth, stream=isStream, headers=header)
    return requests.get(url)


def postRequest(url, jsonBody, headers):
    return requests.post(url, json=jsonBody, headers=headers)


def getJsonFromWeb(webResult):
    resJsonString = ""
    for row in webResult.text.split("\r\n")[:-1]:
        if (row == "NG"):
            return {"status": "error", "message": webResult.text}
        data = row.split("=")
        resJsonString += f"\"{data[0]}\": \"{data[1]}\","
    resJson = "{" + resJsonString[:-1] + "}"
    resJson = json.loads(resJson)
    return resJson


def getAPIbyJson(paramJson, cgiFilename="eventsources.cgi", isAcceptJson=True):
    url = getUrlPath(paramJson, cgiFilename)
    resJson = {}
    if (isAcceptJson):
        resJson = json.loads(getRequest(url).text)
    else:
        res = getRequest(url, isAcceptJson=isAcceptJson)
        resJson = getJsonFromWeb(res)
    jsonHeader = [header for header in resJson]
    return [resJson, jsonHeader]


def getUrlPath(paramJson, cgiFilename):
    return baseUrl + getUriFromJson(paramJson, cgiFilename)


# Deprecated: digest auth has been handled by requests.auth
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


def getHeatmapNumpy(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "heatmap",
            "action": "check",
        }
    resJson, headers = getAPIbyJson(paramJson)
    resJson = resJson[headers[0]][0]
    jsonHeaders = [name for name in resJson]
    levels = resJson[jsonHeaders[1]]
    np.savetxt("heatmap/" + datetime.datetime.now().strftime("%H-%M-%S") + ".csv", levels, delimiter=",")
    levels = [linearMapper(x, 0, 9999, 255, 0) for x in levels]
    heatmapResolution = [int(x) for x in resJson[jsonHeaders[3]].split("x")]
    levelsNp = np.reshape(levels, heatmapResolution).astype(np.uint8)
    return [levelsNp, heatmapResolution]


def getHeatmapHeatmapImage():
    heatmapNumpy, heatmapResolution = getHeatmapNumpy()
    heatmapImage = cv2.applyColorMap(heatmapNumpy, cv2.COLORMAP_JET)
    return heatmapImage, heatmapResolution


def getPeoplecount(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "peoplecount",
            "action": "view",
        }
    resJson, headers = getAPIbyJson(paramJson)
    # resJson = getJsonFromWeb(res)
    return resJson


# TODO: Submenu Not Found
def getObjectDetectFromImage(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "objectdetectfromimage",
            "action": "control",
            "ObjectType": "Face"
        }
    resJson, headers = getAPIbyJson(paramJson, isAcceptJson=False)
    return resJson


def getThermalDetection(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "thermaldetectionmode",
            "action": "view",
            "Channel": "0"
        }
    resJson, headers = getAPIbyJson(paramJson)
    return resJson


# Deprecated as this method is too fucking slow
def showCameraStream(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "stream",
            "action": "view",
            # "Profile": "1",
            "CodecType": "MJPEG",
            # "Resolution": "300x300",
            "FrameRate": "30",
            "CompressionLevel": "50"
        }
    url = getUrlPath(paramJson, "video.cgi")
    stream = requests.get(url, stream=True, auth=auth)
    try:
        if stream.ok:
            boundary = b'--SamsungTechwin'
            buffer = b''
            for chunk in stream.iter_content():
                if boundary not in buffer:
                    buffer += chunk
                else:
                    imageByte = buffer
                    a = imageByte.find(b'\xff\xd8')
                    b = imageByte.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        jpg = imageByte[a:b + 2]
                        imageNumpy = np.fromstring(jpg, dtype=np.uint8)
                        i = cv2.imdecode(imageNumpy, cv2.IMREAD_COLOR)
                        cv2.imshow('i', i)
                        if cv2.waitKey(1) == 27:
                            exit(0)
                    buffer = b''
    except:
        showCameraStream()


def rtspStream():
    # startTime = time.time()
    cap = cv2.VideoCapture(f"rtsp://admin:A%40dmin%242017@{host}/H.264/media.smp")
    return cap


def setLightLevel(group=31, level=20):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    requestUrl = lightingUrl + "/group/{}/level/{}"
    requestUrl = requestUrl.format(group, level)
    res = getRequest(requestUrl)
    if res.status_code == 200:
        return True
    return False


def linearMapper(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin
    valueScaled = float(value - leftMin) / float(leftSpan)
    return rightMin + (valueScaled * rightSpan)
