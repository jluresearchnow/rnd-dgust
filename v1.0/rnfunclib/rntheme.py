# -*- coding: utf-8 -*-
#for survey functions
import rncommon
reload(rncommon)
from rncommon import printError, labelsToArray
def rnGetPanelName(src):
  rnPanels = dict(vop=["1-40",42, "45-49", "64-66"],
                 er=["50-55","57-60"],
                 mmr=[56,"560-566"],
                 cs=["90-98"]
                 )
  for key, value in rnPanels.iteritems():
    if src in labelsToArray(value):
      return key
  return ''
  
def rnGetThemeFooter(src,decLang):
  rnfootersByPanel = {}
  rnfootersBySrc = {'6':'<span style="margin-right:20px"><a href="//www.valuedopinions.com.au/privacy" target="_blank" title="Privacy Policy">Privacy Policy</a></span><span><a onclick="window.open(\'/survey/selfserve/rnstarlib/logos/aucs.html\',\'\',\'width=600, height=400, toolbar=no, menubar=no, scrollbars=yes, status=yes, location=no, resizable=yes, titlebar=0, top=\' + (screen.availHeight/2 - 240)  +\', left=\' + (screen.availLeft + screen.availWidth/2 - 300));" href="#">Collection Statement</a></span>'}
  rnPanel = rnGetPanelName(src)
  if src in rnfootersBySrc:
    return rnfootersBySrc[src]
  elif rnPanel in rnfootersByPanel:
    return rnfootersByPanel[rnPanel]
  else:
    return ''
  

exported = dict(rnGetPanelName=rnGetPanelName,
                rnGetThemeFooter=rnGetThemeFooter
                )
