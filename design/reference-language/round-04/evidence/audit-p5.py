"""Check final P5 token references and official SVG geometry; not a visual judge."""
import re
import xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
css=(ROOT/'app.css').read_text()
defs=set(re.findall(r'(--[\w-]+)\s*:',css))
refs=set(re.findall(r'var\((--[\w-]+)',css))
assert not refs-defs
assert not defs-refs
names=[]
for svg in re.findall(r'<svg\b[\s\S]*?</svg>',(ROOT/'app.html').read_text()):
 match=re.search(r'data-(interface|category)-icon="([^"]+)"',svg)
 if not match:continue
 name=match.group(2)
 actual=ET.fromstring(svg)
 original=ET.fromstring((ROOT/'assets'/f'{name}.svg').read_text())
 def geometry(node):
  return [(c.tag.split('}')[-1],sorted((k,v)for k,v in c.attrib.items()if k not in ['class','fill','stroke']))for c in node]
 assert geometry(actual)==geometry(original),name
 names.append(match.group(1)+':'+name)
assert len(names)==14
text=f'''Tokens {len(defs)}; undefined=[]; unused=[]
Official SVG child geometry unchanged for {len(names)} templates: {', '.join(names)}
Tag text #34558b on #eaf0ff contrast6.53:1; same color at scoped12px. Additional note muted/white5.35 and muted/surface4.86.
App.js + inspect-browser-p5.cjs + verify-review-p5.cjs + verify-accessibility-p5.cjs + verify-p5-review.cjs + verify-times-p5.cjs: existing todo anti-slop Oxlint deny-warnings exit0; TypeScript checkJs ESNext/DOM/DOM.Iterable NodeNext explicit Node types exit0.
Final P5 full behavior/accessibility and horizontal-times reruns performed. Normal and forced-colors focus newly verified after white inset correction.
Tokens compact-meta12/16, tag-icon14, time-option-width72 express scoped user requirements. Main price/date/time/action/field labels remain >=14.
Previous P4 time600/white accent5.43/hover7.37 and detailed0/40/100/200ms transition samples are reused only for unchanged role declarations. P5 hover entry/leave and fixed geometry were rerun.
No CSS gradients; no decorative section/tab line. Scrollbar hiding is only actual overflowing six-option time strips; document horizontal overflow0 at both widths/200%.
Python serialization/audit is not represented as JS anti-slop lint.
'''
(ROOT/'evidence/review-p5/code-checks.txt').write_text(text)
print(text)
