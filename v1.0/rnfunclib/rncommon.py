# -*- coding: utf-8 -*-
#print exception message
def printError(functionName, e):
    print "Error: " + functionName +": " + str(e)

def labelsToArray(arrLabels):
  try:
    codes = []
    for item in arrLabels:
      item = str(item)
      if item.find("-") > -1:
         items = item.split("-")
         preletter = ""
         st = items[0]
         ed = items[1]
         if items[0].find(":") > -1:
           tmpItems = items[0].split(":")
           preletter = tmpItems[0]
           st = tmpItems[1]
         for i in range(int(st),int(ed)+1):
           codes.append(preletter + str(i))
      else:
        codes.append(item)
    return codes
  except Exception as e:
    printError('labelsToArray', e)
    pass

def getFullPath(gv):
  return gv.request.fullPath

def getBaseUrl(gv):
  return gv.secureHost or gv.URL

def getHostId(gv):
  sid = '100' 
  curHost = getBaseUrl(gv)
  if curHost:
    if curHost.find('survey-d.researchnow.com') > -1:
      sid = '101'
    elif curHost.find('survey-ca.researchnow.com') > -1:
      sid = '102'
    elif curHost.find('survey-au.researchnow.com') > -1:
      sid = '103'
    elif curHost.find('survey-uk.researchnow.com') > -1:
      sid = '104'
  return sid

def getUrlParam(url,param):
    import urlparse
    from HTMLParser import HTMLParser
    try:
      parser = HTMLParser()
      url1 = parser.unescape(url).encode('ascii')
      parsed = urlparse.urlparse(url1)
      return urlparse.parse_qs(parsed.query)[param][0]
    except:
      return None

def rnTimerStart(p):
  import time
  if not p.get("nthTimer"):
    p.nthTimer = 0
  p.nthTimer = p.nthTimer + 1
  p.rnTimerStart = int(time.time())
  
def rnTimerEnd(p):
  import time
  if p.get("rnTimerStart"):
    timeDiff = int(time.time() - p.rnTimerStart)
    p.markers.append("rnTimer/%d/%d" % (p.nthTimer,timeDiff) )

def rnMedian(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2
    if lstLen < 1:
      return None
    if (lstLen % 2):
      return sortedLst[index]
    else:
      return (sortedLst[index] + sortedLst[index + 1])/2.0


def rnGetTimeSpent(gv,uuid):
  try:
    return gv.survey.preciseTime.get(uuid)
  except KeyError:
    return []

def rnGetTimeSpentStat(gv,uuid):
  origTimeArr = rnGetTimeSpent(gv,uuid)
  newTimeArr = [x for x in origTimeArr if x > 0]
  arrCount = len(newTimeArr)
  arrSum = 0
  arrMean = 0
  arrMedian = 0
  if arrCount > 0:
    arrSum = round(sum(newTimeArr) / 1000.0, 2)
    arrMean = round(arrSum/arrCount,2)
    arrMedian = round(rnMedian(newTimeArr) /1000.0,2)
  return {"count":arrCount,"sum":arrSum,"mean":arrMean,"median":arrMedian}

exported = dict(printError=printError,
                   labelsToArray=labelsToArray,
                   getFullPath=getFullPath,
                   getBaseUrl=getBaseUrl,
                   getHostId=getHostId,
                   getUrlParam=getUrlParam,
                   rnTimerStart=rnTimerStart,
                   rnTimerEnd=rnTimerEnd,
                   rnGetTimeSpent=rnGetTimeSpent,
                   rnGetTimeSpentStat=rnGetTimeSpentStat
                   )