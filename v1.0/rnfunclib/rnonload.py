from hermes.elements import Row, Exec, Term, Quota, Radio, Checkbox, Group, Col, Text, Choice, Condition, Noanswer, Suspend, Samplesources
def gather(root, predicate):
    "find all items fullfilling predicate in survey tree"
    items = []
    def rec(el):
        if predicate(el):
            items.append(el)
        map(rec, el.children)
    rec(root)
    return items
def createVCurQid(ctx):
    return
    if ctx.compat < 127: return
    if 'vrncurqid' in ctx:
        return
    el = ctx.root.createTransient("radio", label="vrncurqid", title='RN Last seen question')
    from hermes.QuestionElement import QuestionElement
    from hermes.elements.Html import Html
    from hermes.elements.Comment import Comment

    el.attr['virtual'] = '''
try: 
    for m in markers:
      if m.startswith("rncurqid"):
        q = m.split("/")[1]
        for row in this.rows:
            if row.label == q:
               data[0][0] = row.index
               break
except:
    pass
'''
    pages = {}
    page = 0
    # We do not have a ctx.root.elements until all mutators have fired
    elements = gather(ctx.root, lambda x: isinstance(x, (QuestionElement, Suspend.Suspend, Html)))
    for q in elements:
        if isinstance(q, Suspend.Suspend):
            page += 1
        elif isinstance(q, (QuestionElement, Html, Comment)):
            where = q.attr.get('where') or ''
            if where in ('report', 'data'): continue
            if 'execute' in where: continue
            if q.attr.get('style') == 'dev': continue
            if q.attr.get('virtual') or q.attr.get('aggregate'):    continue
            label = q.attr.get('label')
            if label == "rnjumpto" or label == '_tcx': continue
            if not label: return ctx.error("Missing label", q)
            pages.setdefault(page, []).append((label, q))

    el._lmap = lmap = {}   
    rows = 0

    for page, elements in sorted(pages.items()):
        labels = ','.join(label for label,_ in elements)
        first = elements[0][1]
        if isinstance(first, (Html, Comment)): text = 'Comment element'
        else:                                  text = first.attr['title']
        el.createTransient('row', label=elements[-1][0], cdata=labels)
        for label, _ in elements:
            lmap[label] = rows
        rows += 1
    el.notifyEnd(0)

def createJumptoQid(ctx):

    if 'brnjumpto' not in ctx or 'rnjumpto' not in ctx:
        return
    from hermes.QuestionElement import QuestionElement
    from hermes.elements.Html import Html
    from hermes.elements.Comment import Comment
    from hermes.elements import Suspend

    pages = {}
    page = 0
    # We do not have a ctx.root.elements until all mutators have fired
    elements = gather(ctx.root, lambda x: isinstance(x, (QuestionElement, Suspend.Suspend, Html)))
    for q in elements:
        if isinstance(q, Suspend.Suspend):
            page += 1
            gotoEl = q.parent.createTransient("goto", target="brnjumpto",cond="gv.request.get('jumpto0')>'0'")
            gotoEl.moveAfter(q)
        elif isinstance(q, (QuestionElement, Html, Comment)):
            where = q.attr.get('where') or ''
            if where in ('report', 'data'): continue
            if 'execute' in where: continue
            if q.attr.get('style') == 'dev': continue
            if q.attr.get('virtual') or q.attr.get('aggregate'):    continue
            label = q.attr.get('label')
            if label == "rnjumpto" or label == '_tcx': continue
            if not label: return ctx.error("Missing label", q)
            pages.setdefault(page, []).append((label, q))

    bel = ctx.geterr('brnjumpto')
    el = ctx.geterr('rnjumpto')
    bel.createTransient("suspend")

    rows = 0
    for page, elements in sorted(pages.items()):
        labels = ','.join(label for label,_ in elements)
        el.createTransient('choice', label=elements[0][0], cdata=labels)
        bel.createTransient("goto", target=elements[0][0],cond="rnjumpto." + elements[0][0])
        rows += 1
    el.notifyEnd(0)


def createVStatus(ctx):
    from hermes.elements import Radio, Row
    if 'vStatus' in ctx:
        return
    el = ctx.root.createChild(Radio.Radio, label="vStatus", title="vStatus - captures respondents status/ reason for removal")
    el.transient = True
    el.attr['virtual'] = '''
for row in vStatus.rows:
    if row.label in markers:
       vStatus.val = row.index
       break

if not vStatus.val:
    for mark in markers:
        if mark.startswith('term:'):
          vStatus.val = vStatus.term.index
          break
if vStatus.term and 'lateScreenOut' in markers: vStatus.val = vStatus.lateScreenOut.index
if vStatus.OQ and 'lateQuotaFull' in markers: vStatus.val = vStatus.lateQuotaFull.index
if vStatus.qualified and 'shortComplete' in markers: vStatus.val = vStatus.shortComplete.index
if vStatus.qualified and 'longComplete' in markers: vStatus.val = vStatus.longComplete.index
'''
    
    el.createTransient(Row.Row, value=1, label='term' , cdata="Terminated")
    el.createTransient(Row.Row, value=2, label='OQ' , cdata="Overquota (Hard Quotafull)") 
    el.createTransient(Row.Row, value=3, label='qualified' , cdata="Qualified")
    el.createTransient(Row.Row, value=4, label='autorecover' , cdata="Partial")
    el.createTransient(Row.Row, value=5, label='softquotafull' , cdata="Terminated - Soft Quotafull")
    el.createTransient(Row.Row, value=6, label='speeder' , cdata="Terminated - Speeder / Racer")
    el.createTransient(Row.Row, value=7, label='speederAuto' , cdata="Terminated - Speeder - Auto Removed")
    el.createTransient(Row.Row, value=8, label='speederAutoCheck' , cdata="Terminated - Speeder Template Check - Auto Removed")
    el.createTransient(Row.Row, value=9, label='slowpoke' , cdata="Terminated - SlowPoke - respondent who took too long to complete")
    el.createTransient(Row.Row, value=10, label='slowpokeAuto' , cdata="Terminated - SlowPoke - Auto Removed - respondent who took too long to complete")
    el.createTransient(Row.Row, value=11, label='straightliner' , cdata="Terminated - Straightliner")
    el.createTransient(Row.Row, value=12, label='straightlinerAuto' , cdata="Terminated - Straightliner - Auto Removed")
    el.createTransient(Row.Row, value=13, label='badopen' , cdata="Terminated - Bad Verbatim")
    el.createTransient(Row.Row, value=14, label='badopenAuto' , cdata="Terminated - Bad Verbatim - Auto Removed")
    el.createTransient(Row.Row, value=15, label='foreigner' , cdata="Terminated - Out of country IP")
    el.createTransient(Row.Row, value=16, label='failed' , cdata="Terminated - Quality Check Failed")
    el.createTransient(Row.Row, value=17, label='failedAuto' , cdata="Terminated - Quality Check Failed - Auto Removed")
    el.createTransient(Row.Row, value=18, label='error' , cdata="Terminated - Error - removed due to system / script error")
    el.createTransient(Row.Row, value=19, label='badqualified' , cdata="Terminated - Bad Qualified")
    el.createTransient(Row.Row, value=20, label='other' , cdata="Terminated - Other - removed for some other reason")
    el.createTransient(Row.Row, value=21, label='test' , cdata="Terminated - Test record")
    el.createTransient(Row.Row, value=22, label='NQ' , cdata="Terminated - Non-Qualified")
    el.createTransient(Row.Row, value=23, label='bad:qualified' , cdata="Terminated - Disqualified")
    el.createTransient(Row.Row, value=24, label='lateScreenOut' , cdata="Terminated - late")
    el.createTransient(Row.Row, value=25, label='lateQuotaFull' , cdata="Overquota - Late")
    el.createTransient(Row.Row, value=26, label='shortComplete' , cdata="Complete - short")
    el.createTransient(Row.Row, value=27, label='longComplete' , cdata="Complete - Long") 
    el.notifyEnd(0)

def createVqtimeMin(ctx):
    from hermes.elements import Float
    if 'qtimeMin' in ctx:
        return
    el = ctx.root.createChild(Float.Float, label="qtimeMin", title="Total Interview Time in Minutes")
    el.transient = True

    el.attr['virtual'] = '''
timerAll = 0
try: 
    for m in markers:
      if m.startswith("rnTimer"):
         timerAll += int(m.split("/")[-1])
except:
    pass
qtimeMin.val = ((qtime.val or 0) + timerAll )/ 60

'''

    el.notifyEnd(0)

exported = [createVCurQid, createJumptoQid, createVStatus, createVqtimeMin]




