#D-GUST v1.0
import sys
rnlibpath = "/home/hermes/v2/selfserve/dgustlib"
if rnlibpath not in sys.path: sys.path.append(rnlibpath)
 
def onLoad(ctx):
  from v10.rnfunclib import rnonload as rnonload
  reload(rnonload)
  for f in rnonload.exported:
    f(ctx)

def survey_environment(env, survey):
  import json
  from v10.rnfunclib import rnfuncs
  reload(rnfuncs)
  env['json_loads'] = json.loads 
  env.update(rnfuncs.exported) 

def fields(vl, survey):
  from v10.rnfunclib import rnotherhooks
  reload(rnotherhooks)
  vl = rnotherhooks.fields(vl,survey)
  return vl
def pii_levels(survey, d):
  from v10.rnfunclib import rnotherhooks
  reload(rnotherhooks)
  rnotherhooks.pii_levels(survey, d)
  

