"""Assemble the recorded human decisions for this round only.
Not an automated UI judge: after any UI change, re-inspect and update decisions
and evidence before running this historical report generator.
"""
import json,hashlib,subprocess
from pathlib import Path
root=Path(__file__).resolve().parents[4]; base=root/'design/reference-language/round-01'
cat=json.loads((root/'skills/reference-review/references/failure-catalog.json').read_text())
notes={
'ORC-F01':'No sidebar exists in either specimen or assembled screen.', 'ORC-F02':'No sidebar or chromatic accent distribution exists.',
'ORC-F03':'Selected Day1 uses white 700 text on #111; contrast exceeds4.5:1.', 'ORC-F04':'Single completion button in assembled screen. Isolated E5 is a specimen, not a duplicate product CTA.',
'ORC-F05':'Three photo-led places, not a growing administrative dataset; image cards serve identification.', 'ORC-F06':'Neutral selected/unselected/disabled states; no danger or success colors.',
'ORC-F07':'The analyst-authored prompt E1 chooses18px/700 title,62px row and26px gap for the user-authorized reproduction; retain these in reference translation instead of generic48–56px/600/16px thresholds.',
'ORC-F08':'No per-row action buttons; visible native checkboxes are selection controls and grips are explicitly decorative in static experiment.',
'ORC-F09':'One vertical content column; no dashboard columns.', 'ORC-F10':'No coupled icon+text control: back icon stands alone; grips center on place rows. No plus characters.',
'ORC-F11':'No colored icon+text action pair.', 'ORC-F12':'The analyst-authored prompt chooses9px checkbox gap,18px row gaps,26px opening,6px card inset. Left/right screen inset both24px. These analyst reconstruction choices within the authorized reproduction scope supersede the generic4px grid; they are not user-specified numbers.',
'ORC-F13':'Disabled buttons show default cursor; native checkbox also default. Pointer semantics need correction.',
'ORC-F14':'Place lists and rows use div instead of ul/li; semantic lists need correction.',
'ORC-F15':'No colored badges, avatars or entity icon palette; provided photographic colors are content.',
'ORC-F16':'No nested scrollbars;390 comparison content fits669px region;320 expands to preserve long content. Fixed frame is explicitly static comparison scope.',
'ORC-G01':'No gradients in CSS or screen.', 'ORC-G02':'No shadows in CSS or screen.',
'ORC-G03':'The analyst-authored prompt E5 chooses12px completion radius for the user-authorized reproduction; preserve this exception to8px limit. Pill16px is allowed pill category; cards6px.',
'ORC-G04':'UI colors are grayscale; supplied photos are content, not UI accent colors.',
'ORC-G05':'No custom hover transform/scale/shadow/opacity rules; native checkboxes toggle immediately with no animation.',
'ORC-G06':'Reading sizes14/16/18px only in each view.', 'ORC-G07':'Analyst-selected prompt9/18/26/6px measurements are retained as documented reference translation exceptions to4px grid.',
'ORC-G08':'Three compact photo rows and Day3 fragment retain tool density; no hero or oversized title.',
'ORC-G09':'Grip symbols are explicitly requested static layout specimens, not added decoration; no ornamental lines, logos or shadows.',
'ORC-G10':'No sidebar or competing modes.', 'ORC-G11':'Selected Day1 white text700; no thin dark-background text.',
'ORC-G12':'One completion action per assembled screen; independent specimen is a review example.',
'ORC-G13':'No20+ item grid; only three supplied photographic rows.', 'ORC-G14':'No red/green UI colors.',
'ORC-G15':'Title18px is below24px maximum.', 'ORC-G16':'No repeated action buttons; selection checkboxes and decorative grips match static input.',
'ORC-G17':'No multi-column dashboard.', 'ORC-G18':'No icon-text control pairs; grip row centers and standalone back verified.',
'ORC-G19':'No colored text/icon pair.', 'ORC-G20':'Header/content/footer share24px inset; prompt9/18/26/6px gaps explicitly override generic4px grid.',
'ORC-G21':'Disabled buttons default cursor; pointer and disabled cursor mapping needs correction.',
'ORC-G22':'No status badges.', 'ORC-G23':'No nested scrolling or text truncation;320 height growth shows all supplied text.',
'ORC-G24':'Place collections need semantic ul/li instead of stacked divs.',
'ORC-A01':'Card6px, day pill16px, completion12px radii distinguish roles.',
'ORC-A02':'White surface includes fine item/control perimeters and selected black day; no need for conflicting micro-gradient.',
'ORC-A03':'No box shadows.', 'ORC-A04':'No blue default, invented brand or palette exploration; fixed supplied reference translation.',
'ORC-A05':'Asymmetric checkbox/photo/copy/grip columns; centered title serves screen identification.',
'ORC-A06':'All supplied place metadata remains visible; no invented price/rating/seller in static travel reference.',
'ORC-A07':'Prompt requests icon-only disabled back with accessible name and decorative grip hidden from accessibility; explicit static reference exception to visible text labels.',
'ORC-A08':'All photos use supplied crops; no placeholders or generic substituted stock.',
'ORC-A09':'Vertical list, not grid; prompt explicitly requires equal96px photos for short and long rows, so featured-card variation is out of scope.',
'ORC-A10':'No async data, backend, errors, loading, empty-state flows in explicitly static specimen experiment.',
'RUI-01':'Prompt separates295 image-px source,390 CSS chosen width, unknown DPR/font and observed-vs-chosen values.',
'RUI-02':'62 defined/referenced variables cover design values;359px media query literal documented native limitation. Negative image edge overlap derives from border variable and is documented.',
'RUI-03':'All75 active catalog rules retained with original checks and individual scope decisions; this is static screen review only.',
'RUI-04':'Required static E1–E5 appear assembled and isolated; pointer/Space checkbox works, disabled actions remain disabled. Saving, drag, date navigation not requested.',
'RUI-05':'No new idea synthesis request; explicit language-only reference reconstruction.',
'RUI-06':'Plain HTML/CSS only; browser parses and displays without image failures; no JS/TS implementation, hence no TS anti-slop pass claim.',
'RUI-07':'Prompt states roles before implementation: centered title, small day selector, date groups, external checkbox, image identification and screen-wide completion.',
'RUI-08':'No added logo, wordmark or slogan.',
'RUI-09':'Both pages at320/390 computed reading sizes minimum14px; no clipped text in measured text nodes.',
'RUI-10':'64×32 day pills distinct from342×56 completion at390; no text-only execution links.',
'RUI-11':'Assembled screen adds no hints. Components explanation belongs to review context and documents scope differences.',
'RUI-12':'Provided official chevron-left and grip-vertical SVGs only;24/18px gray outlines; disabled back named, decorative grips aria-hidden.',
'RUI-13':'390 three complete rows and observed fragment fit;320 content expands, no text overflow; Tab/Space focus remains accessible.',
'RUI-14':'No hr/pseudo/shadow/gradient/tab underline or footer divider. Item and control perimeters preserve separate boundary roles.',
'RUI-15':'No chat or conversation flow.',
'RUI-16':'Q1 external checks, Q2 full-height equal photos, Q3 group-gap hierarchy, Q4 pill/footer distinction directly compared to original AFTER blind implementation.',
'RUI-17':'Core single-column rhythm and three complete places remain.14px adaptation makes text visibly larger, native checks darker and Day3 only photo fragment remains; differences disclosed, not pixel fidelity.',
'RUI-18':'Single provided source; no multi-reference research branches.',
'RUI-19':'Day pills are static day selector specimens, not mobile destination navigation.',
'RUI-20':'Screen purpose h1 is18px/700, above16px group and14px row metadata.',
'RUI-21':'No date/time picker or editable date input; day state is explicitly static labeled sample.',
'RUI-22':'Container owns24px insets; check x24/card x55. Footer button x24. Image1px overlap documented; no doubled screen inset.',
'RUI-23':'Same markup/classes and shared CSS render identical E1–E5 roles at390; review headings are outside specimens.',
'RUI-24':'Day selector state and group heading label different navigation/group roles; dates add calendar information; no invented year.',
'RUI-25':'40px group gap exceeds18px internal row gap; dates label ownership, footer whole-screen action separate without forbidden divider.'}
na={'ORC-F01','ORC-F02','ORC-F09','ORC-F10','ORC-F11','ORC-G10','ORC-G17','ORC-G18','ORC-G19','ORC-G22','ORC-A04','ORC-A09','ORC-A10','RUI-05','RUI-15','RUI-18','RUI-19','RUI-21'}
exceptions={'ORC-F07','ORC-F12','ORC-G03','ORC-G07','ORC-G09','ORC-G20','ORC-A07'}
fails={'ORC-F13','ORC-F14','ORC-G21','ORC-G24'}
fixed=(base/'evidence/gate-fixed.marker').exists()
if fixed:
 for id in ['ORC-F13','ORC-G21']:notes[id]='Checkbox cursor pointer; disabled back/completion cursor not-allowed. Pointer/keyboard behavior and absence of layout shift verified.'
 for id in ['ORC-F14','ORC-G24']:notes[id]='Place collections now ul/li with explicit zero margin/padding and list-style none. Landmarks/header/section/footer and h1/h2 retained; layout wrappers carry grid/inset roles.'
 fails=set()
 notes['RUI-17']='Core single-column rhythm and three complete places remain.14px adaptation makes text visibly larger and native controls differ; prompt-v2 restores Day3 perimeter. Actual original/output comparison preserves main hierarchy without asserting pixel fidelity.'
contract={'schema_version':1,'catalog_version':cat['version'],'targets':['screen.html','components.html','ui.css','prompt-v1.md'],'rules':[]}
for r in cat['rules']:
 if r['status']!='active':continue
 id=r['id'];contract['rules'].append({'id':id,'applicable':id not in na,'scope':'Static E1–E5 specimen and assembled screen at390/320; excludes review board and complete travel-app flows','reason':notes[id],'checks':r['checks'],'exceptions':[{'id':'EX-'+id,'reason':notes[id]}] if id in exceptions else []})
contract['rules'].append({'id':'PROJECT-FRAGMENT','applicable':True,'scope':'Day3 observed fragment','reason':'Original visible top/right item perimeter was omitted by prompt-v1; preserve visible boundary without inventing hidden content.','checks':['spec','code','visual'],'exceptions':[]})
notes['PROJECT-FRAGMENT']='Visible fragment perimeter restored from prompt-v2; no hidden content invented.' if fixed else 'Original fragment includes top/right card perimeter absent in prompt-v1/output: translation omission, not blind implementation failure.'
if not fixed: fails.add('PROJECT-FRAGMENT')
if (base/'prompt-v2.md').exists(): contract['targets'].append('prompt-v2.md')
(base/'gate-contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
cli=[str(root/'skills/reference-review/scripts/design_gate.py')]
fp=json.loads(subprocess.check_output(['python3',*cli,'fingerprint','--root',str(base),'--contract','gate-contract.json'],cwd=base))
def evidence(kind,path):return {'kind':kind,'path':path,'sha256':hashlib.sha256((base/path).read_bytes()).hexdigest()}
report={'schema_version':1,**{k:fp[k] for k in ['catalog_sha256','contract_sha256','target_sha256']},'results':[]}
for r in contract['rules']:
 id=r['id'];status='not-applicable' if id in na else 'exception' if id in exceptions else 'fail' if id in fails else 'pass'
 ev=[]
 for kind in r['checks']:
  paths={'spec':['prompt-v1.md','gate-review.md']+(['prompt-v2.md'] if fixed else []),'code':['screen.html','components.html','ui.css'],'visual':['evidence/gate-screen-390.png','evidence/gate-screen-320.png','evidence/gate-components-390.png','evidence/gate-components-320.png','assets/source.png'],'interaction':['evidence/gate-browser.json']}
  ev.extend(evidence(kind,p) for p in paths[kind])
 rr={'id':id,'status':status,'reason':notes[id],'evidence':ev}
 if status=='exception':rr['exception_id']='EX-'+id
 report['results'].append(rr)
(base/'gate-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
r=subprocess.run(['python3',*cli,'check','--root',str(base),'--contract','gate-contract.json','--report','gate-report.json','--ledger','failure-events.jsonl'],capture_output=True,text=True,cwd=base)
(base/'gate-result.json').write_text(r.stdout);print(r.returncode,{k:v for k,v in json.loads(r.stdout).items() if k!='results'})
