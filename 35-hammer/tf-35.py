#!/usr/bin/env python

import re, string, sys
import time

stops = open("../stop_words.txt").read()
s = open(sys.argv[1]).read()

letters = xrange(ord('a'),ord('z')+1)

# Clean-up text:
for x in letters: # Translate to lower case
    s = re.compile(chr(x-32)).sub(chr(x), s)
s = re.compile('[^a-z]+').sub(' ',s) # Replace and collapse non-letters
s = re.compile(r'^[^\w]+|[^\w]+$').sub('',s) # Trim

# Remove stop-words
for swm in re.compile(r'\b\w+\b').finditer(stops):
    sw = swm.group()
    s = re.compile(r'\b'+sw+r'\b *').sub("", s)

# Sort words (using bubblesort):
change = True
while change:
    chgcnt = 0
    change = False
    for x in letters:
        if x==ord('a'):
            pattern = r'\b(\w+)() \1(\w+)\b'
        else:
            pattern = r'\b(\w*)('+chr(x)+r'\w*) \1([a-'+chr(x-1)+r']\w*)\b'
        p = re.compile(pattern)
        (s,count) = p.subn(r'\1\3 \1\2', s)
        chgcnt += count
        change = change or (count>0)
    sys.stderr.write("DB: chgcnt=%d\t@ %d\n" % (chgcnt, time.time()))

# Count words:
s = re.compile(r'\b(\w)').sub(r'<x>\1', s)
p = re.compile(r'<(x*)>(\w+) <(x*)>\2')
change = True
while change:
    change = False
    (s,count) = p.subn(r'<\1\3>\2', s)
    change = change or (count>0)

sys.stderr.write("DB: s=%s\n" % (s))

# Sort by count:
p = re.compile(r'<(x*)>(\w+) <(\1x+)>(\w+)\b')
change = True
while change:
    chgcnt = 0
    change = False
    (s,count) = p.subn(r'<\3>\4 <\1>\2', s)
    chgcnt += count
    change = change or (count>0)
    sys.stderr.write("DB: chgcnt2=%d\t@ %d\n" % (chgcnt, time.time()))

# Report:
i = 0
for wm in re.compile(r'<(x*)>(\w+)').finditer(s):
    print wm.group(2), ' - ', len(wm.group(1))
    i +=1
    if i>=25: break
