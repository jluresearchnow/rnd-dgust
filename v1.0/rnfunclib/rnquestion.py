# -*- coding: utf-8 -*-

import rncommon
reload(rncommon)
from rncommon import printError, labelsToArray

def rncurqid(qid,p,removeMarker,setMarker):
  try: 
    curMarker = "rncurqid/" + qid 
    if p.get("rncurqid"):
      removeMarker(p.rncurqid) 
    setMarker(curMarker)
    p.rncurqid = curMarker
  except: pass
  return ''

def copyQ(toQ, fromQ):
  try:
    toQ.val = fromQ.val
  except Exception:
    for eachRow in fromQ.rows:
      try:
        toQ[eachRow].val = eachRow.val
      except Exception:
        for eachCol in fromQ.cols:
          try:
            toQ[eachRow][eachCol].val = eachRow[eachCol].val
          except Exception:
            try:
              toQ[eachRow][eachCol].val = None
            except Exception:
              try:
                toQ.val = None
              except Exception:
                pass

def domainValues(reqArray,qAttr):
  try:
    try: reqArray = reqArray.order
    except: pass
    return [str(eR.attr(qAttr)) for eR in reqArray if eR.displayed]
  except Exception as e:
    printError('domainValues', e)
    pass
def categories(reqArray,qAttr):
  try:
    try: reqArray = reqArray.order
    except: pass
    return [str(eR.attr(qAttr)) for eR in reqArray if (eR.any and eR.val not in ['',None])]
  except Exception as e:
    printError('categories', e)
    pass
def anyCodes(qid, arrLabels):
  try:
    cnt = 0
    for label in labelsToArray(arrLabels):
      try:
        if qid.attr(label).any and qid.attr(label).val not in ['',None]:
          cnt += 1
      except: pass
    return cnt
  except Exception as e:
    printError('anyCodes', e)
    pass

exported = dict(copyQ=copyQ,
                rncurqid=rncurqid,
                domainValues=domainValues,
                categories=categories,
                anyCodes=anyCodes
                )
