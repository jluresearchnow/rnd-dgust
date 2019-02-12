import os
def fields(vl, survey):
    if os.path.isfile('%s/variables.xls' % survey.path):
      return vl
    exVs = ['vrncurqid','jumpto', 'stsd*', 'vlist','vos','vosr15oe','vbrowser','vbrowserr15oe','vmobiledevice','vmobileos','start_date','source','decLang','list','userAgent','dcua','session','url','ipAddress','src','c','study','date','qtime','vdropout','Source','settings','pagetime','fp_*','vStatus']
    for x in vl:
      for v in exVs:
        xl = x.label if v[-1:] != '*' else x.label[:len(v)-1] + '*'
        if xl == v:
            x.notdp = True
    return vl
def pii_levels(survey, d):
  hides = ("ipAddress","XID", "Source","panelSource","src","stsd1","stsd2","stsd3","stsd4","stsd5","stsd6","stsd7")
    
  for hide in hides:
    try:
      d[hide].pii = 4
    except KeyError:
      pass
