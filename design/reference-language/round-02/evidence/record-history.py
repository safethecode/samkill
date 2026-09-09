#!/usr/bin/env python3
"""One-time serialization of observed P1/P2 failures from preserved source/render.
Requires final contract to exist. This does not assert full P1 visual inspection.
Re-run only to verify identical history, never overwrite preserved UI/captures.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
GATE = REPO/'skills/reference-review/scripts/design_gate.py'
CATALOG = REPO/'skills/reference-review/references/failure-catalog.json'
spec = importlib.util.spec_from_file_location('design_gate', GATE)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
final_contract = json.loads((ROOT/'gate-contract.json').read_text())
final_report = json.loads((ROOT/'gate-report.json').read_text())

def ev(root, kind, path):
    return {'kind':kind,'path':path,'sha256':hashlib.sha256((root/path).read_bytes()).hexdigest()}

for version, archive in [('p1','p1-source'),('p2','p2-first')]:
    root = ROOT/'evidence'/archive
    if (root/'gate-result.json').exists():
        print('Preserving existing',version,'gate history')
        continue
    evidence = root/'evidence'
    evidence.mkdir(exist_ok=True)
    if version == 'p1':
        shutil.copy2(ROOT/'prompt-v1.md',root/'prompt-v1.md')
        shutil.copy2(ROOT/'evidence/screen-p1-390.png',evidence/'screen.png')
        note = 'P1 아카이브 직접 판독. 이름24+간격8+배지24=56으로 식별48 계약과 충돌. 조립 카드188/둘째y380으로8px 밀린 실제 초기 렌더. P1 독립 표본/전체 행동은 당시 미검증이므로 다른 적용 규칙은 unknown을 유지한다. 최종 판독으로 과거 검사를 소급하지 않는다.'
    else:
        for file in root.glob('gate-*.png'):
            shutil.copy2(file,evidence/file.name)
        shutil.copy2(root/'gate-browser.json',evidence/'gate-browser.json')
        shutil.copy2(ROOT/'evidence/code-checks.txt',evidence/'code-checks.txt')
        note = 'P2 첫4화면과 입력 실행 직접 판독. 조립390 검색x16/w358에 비해 독립390 검색x40/w310,표본342. 바깥 설명24px 여백이 표본폭을 줄여 E3도 독립에서만2줄이다. 다른조립관계는P2에서식별48/카드180/둘째y372로수정확인.320은가로잘림없다. 원본의흰표면/배경/두자격과찜상태는유지. RUI22/23와표본폭규칙은확정실패.'
    (root/'gate-review.md').write_text(note+'\n')
    contract=copy.deepcopy(final_contract)
    contract['targets']=[name for name in final_contract['targets'] if (root/name).exists()]
    contract_path=root/'gate-contract.json'
    contract_path.write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
    results=copy.deepcopy(final_report['results'])
    for result in results:
        rid=result['id']
        if result['status']=='not-applicable':
            continue
        if version=='p1':
            result['status']='fail' if rid=='PROJECT-BOX-SUM' else 'unknown'
            result.pop('exception_id',None)
            result['reason']=note if rid=='PROJECT-BOX-SUM' else 'P1 당시 이 규칙의 전체 검사를 실행하지 않았다. 최종 검증으로 소급 PASS 하지 않음.'
            result['evidence']=[ev(root,'spec','gate-review.md'),ev(root,'code','ui.css'),ev(root,'visual','evidence/screen.png')]
        else:
            for item in result['evidence']:
                item['sha256']=hashlib.sha256((root/item['path']).read_bytes()).hexdigest()
            if rid in ['RUI-22','RUI-23','PROJECT-SPECIMEN-WIDTH','PROJECT-R2-RECONSTRUCTION']:
                result['status']='fail'
                result.pop('exception_id',None)
                result['reason']=note
    report={'schema_version':1,**gate.fingerprints(root,CATALOG,contract_path,contract),'results':results}
    report_path=root/'gate-report.json'
    report_path.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    run=subprocess.run(['python3',str(GATE),'check','--root',str(root),'--contract',str(contract_path),'--report',str(report_path),'--ledger',str(ROOT/'failure-events.jsonl')],text=True,capture_output=True)
    (root/'gate-result.json').write_text(run.stdout)
    outcome=json.loads(run.stdout)
    print(version,run.returncode,outcome['status'],outcome['failures'])
