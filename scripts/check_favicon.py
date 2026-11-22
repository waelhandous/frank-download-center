#!/usr/bin/env python3
"""Fail the static-site release if any FRANK HTML page drops the approved favicon."""
from pathlib import Path
import hashlib, re, subprocess, sys
root=Path(__file__).resolve().parent.parent
sha='6d363b403bc833a31fc2e9f659d38c6f7679f4aaca46dfd09dd702c6f86be8b7'
files=['favicon.svg','favicon.ico','favicon-32x32.png','favicon-192x192.png','apple-touch-icon.png']
errors=[]
for f in files:
 if not (root/f).is_file():errors.append('missing: '+f)
if (root/'favicon.svg').is_file() and hashlib.sha256((root/'favicon.svg').read_bytes()).hexdigest()!=sha:errors.append('official FRANK SVG changed')
if (root/'favicon.ico').is_file() and (root/'favicon.ico').read_bytes()[:4]!=b'\x00\x00\x01\x00':errors.append('favicon.ico not a valid ICO header')
for f in ['favicon-32x32.png','favicon-192x192.png','apple-touch-icon.png']:
 if (root/f).is_file() and not (root/f).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'):errors.append(f+' is not a PNG')
r=subprocess.run(['git','ls-files','-z','--','*.html'],cwd=root,capture_output=True,check=True)
pages=[root/p.decode() for p in r.stdout.split(b'\0') if p]
if not pages:errors.append('no tracked HTML pages found')
for page in pages:
 s=page.read_text(encoding='utf-8')
 head=s.split('</head>',1)[0]
 for expected in ['rel="icon" type="image/svg+xml" href="/favicon.svg"','rel="shortcut icon" href="/favicon.ico"','rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png"']:
  if expected not in head:errors.append(page.name+': missing '+expected)
if errors:
 for e in errors:print('FAIL:',e)
 sys.exit(1)
print('FRANK approved favicon compliance PASS —',len(pages),'HTML pages and',len(files),'assets')
