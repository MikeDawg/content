import re

domain = 'demisto.com'
if 'domain' in demisto.args():
    domain = demisto.args()['domain']

def levenshtein(s1, s2):
    l1 = len(s1)
    l2 = len(s2)

    matrix = [range(l1 + 1)] * (l2 + 1)
    for zz in range(l2 + 1):
        matrix[zz] = range(zz,zz + l1 + 1)
    for zz in range(0,l2):
        for sz in range(0,l1):
            if s1[sz] == s2[zz]:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
            else:
                matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
    return matrix[l2][l1]

res = []
found = False
sender = demisto.get(demisto.args(), 'sender')
if not sender:
    sender = re.search(r".*From\w*:.*\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})\b", demisto.incidents()[0]['details'], re.I)
if sender:
    parts = sender.group(1).split('@')
    if len(parts) == 2:
        distance = levenshtein(domain, parts[1])
        if distance > 0 and distance < 3:
            res.append({'Type': entryTypes['note'], 'ContentsFormat': formats['text'], 'Contents': 'Domain ' + parts[1] + ' is suspicioiusly close to ' + domain})
            found = True
    else:
        res.append({'Type': entryTypes['error'], 'ContentsFormat': formats['text'], 'Contents': 'Unable to extract domain from sender - ' + sender.group(1)})
else:
    res.append({'Type': entryTypes['error'], 'ContentsFormat': formats['text'], 'Contents': 'Unable to find sender in email'})

if found:
    res.append('yes')
else:
    res.append('no')

demisto.results(res)
