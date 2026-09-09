"""Preserve observed failures, never infer unperformed historical checks as passes."""
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; REPO=ROOT.parents[2]
CAT=REPO/'skills/reference-review/references/failure-catalog.json'
CLI=REPO/'skills/reference-review/scripts/design_gate.py'
spec=importlib.util.spec_from_file_location('gate',CLI); gate=importlib.util.module_from_spec(spec); spec.loader.exec_module(gate)
catalog=json.loads(CAT.read_text())
for phase, failures in [('p1-source',{'RUI-17':'첫 기록 y614.625로 원본600.77보다14px아래; 첫값5완전가림;셋째진한값의재현손실.','RUI-22':'날짜행top/잉크위치혼동으로여백중복.','PROJECT-PROMPT-MAPPING':'components E1은공유계약, E2는E1내용으로한칸밀림.'}),('p2-source',{'RUI-02':'nav상태색/대부분간격/크기/그림자직접값과미사용--gap/--nav-safe-area로정의→사용불완전.','ORC-F14':'기록목록이div반복이며날짜span,ul/li/time의미태그누락.','ORC-G24':'기록목록이div반복이며날짜span,ul/li/time의미태그누락.','PROJECT-R3-RECONSTRUCTION':'E4원본둘째아이콘y356~357대비구현slot347로약9px위.36px슬롯과고유그림광학크기구별누락.'})]:
    dest=ROOT/'evidence'/phase

    note='\n'.join(f'{rid}: {reason}' for rid,reason in failures.items())
    (dest/'historical-review.md').write_text('# 최초 실패 보존\n\n'+note+'\n\n다른 항목은 이 스냅샷에서 실행한 전체검증이 없어unknown. 이후 최종검증과 구별한다.\n')
    rules=[]; results=[]
    for item in catalog['rules'] + [{'id':key,'checks':['spec','code','visual'],'status':'active'} for key in failures if key.startswith('PROJECT-')]:
        if item['status']!='active': continue
        rid=item['id']; reason=failures.get(rid,'역사스냅샷 전체검증은 미실행. 최종소스에서 별도재검증한다.')
        rules.append({'id':rid,'applicable':True,'scope':phase,'reason':reason,'checks':item['checks'],'exceptions':[]})
        ev=[{'kind':kind,'path':name,'sha256':hashlib.sha256((dest/name).read_bytes()).hexdigest()} for kind,name in [('spec','historical-review.md'),('code','ui.css'),('visual','gate-screen-390.png')]]
        results.append({'id':rid,'status':'fail' if rid in failures else 'unknown','reason':reason,'evidence':ev})
    contract={'schema_version':1,'catalog_version':catalog['version'],'targets':['screen.html','components.html','ui.css','prompt-v1.md'],'rules':rules}
    cp=dest/'gate-contract.json'; cp.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
    report={'schema_version':1,**gate.fingerprints(dest,CAT,cp,contract),'results':results}
    (dest/'gate-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    result=subprocess.run(['python3',str(CLI),'check','--root',str(dest),'--contract','gate-contract.json','--report','gate-report.json','--ledger',str(ROOT/'failure-events.jsonl')],capture_output=True,text=True,cwd=dest)
    (dest/'gate-result.json').write_text(result.stdout)
    print(phase,result.returncode,result.stdout[:350])
