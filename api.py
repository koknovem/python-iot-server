import json
import requests
from requests.auth import HTTPDigestAuth
import cv2
import numpy as np


host = "192.168.3.22"
baseUrl = "http://" + host
auth = HTTPDigestAuth('admin', 'A@dmin$2017')


def getUriFromJson(paramJson, uri):
    returnValue = f"/stw-cgi/{uri}?"
    for item in paramJson:
        returnValue += item + "=" + str(paramJson[item]) + "&"
    if returnValue[-1] == "&":
        returnValue = returnValue[:-1]
    return returnValue


def getRequest(url, isUseAuth=True, isStream=False):
    print(url)
    if isUseAuth:
        return requests.get(url, auth=auth, stream=isStream, headers={"Accept": "application/json"})
    return requests.get(url)


def postRequest(url, jsonBody, headers):
    return requests.post(url, json=jsonBody, headers=headers)


def getAPIbyJson(paramJson, cgiFilename="eventsources.cgi"):
    url = getUrlPath(paramJson, cgiFilename)
    res = json.loads(getRequest(url))
    return res


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
    resJson = getAPIbyJson(paramJson)
    jsonHeaders = [name for name in resJson]
    levels = [int(x) for x in resJson[jsonHeaders[0]].split(",")]
    heatmapResolution = [int(x) for x in resJson[jsonHeaders[2]].split("x")]
    levelsNp = np.reshape(levels, heatmapResolution).astype(np.uint8)
    return levelsNp

def getHeatmapHeatmapImage():
    heatmapNumpy = getHeatmapNumpy()
    heatmapImage = cv2.applyColorMap(heatmapNumpy, cv2.COLORMAP_JET)
    return heatmapImage

def getPeoplecount(paramJson={}):
    """
    Not a doc string, check the function name to understand what this does la you
    """
    if (paramJson == {}):
        paramJson = {
            "msubmenu": "peoplecount",
            "action": "view",
        }
    res = getAPIbyJson(paramJson)
    # resJson = getJsonFromWeb(res)
    return res

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
    res = getAPIbyJson(paramJson)
    return res

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
    res = getAPIbyJson(paramJson)
    return res


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
    vidCap = cv2.VideoCapture(f"rtsp://admin:A%40dmin%242017@{host}/H.264/media.smp")
    cv2.namedWindow('image_display', cv2.WINDOW_AUTOSIZE)

    while True:
        ret, image = vidCap.read()
        if ret:
            cv2.imshow('image_display', image)
            cv2.waitKey(10)
        else:
            break