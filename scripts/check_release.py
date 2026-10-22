#!/usr/bin/env python3
"""Offline release checks using only the Python standard library."""
from pathlib import Path
import json,hashlib,re
ROOT=Path(__file__).resolve().parents[1]
def main():
    skill=(ROOT/'SKILL.md').read_text(encoding='utf-8')
    version=json.loads((ROOT/'package.json').read_text())['version']
    assert re.search(r'  version: "'+re.escape(version)+'"',skill)
    assert 'v'+version in (ROOT/'README.md').read_text(encoding='utf-8')
    assert re.search(r'^name: '+re.escape(json.loads((ROOT/'package.json').read_text())['name'])+r'$',skill,re.M)
    required=['README.md','LICENSE','THIRD_PARTY_NOTICES.md','agents/openai.yaml','scripts/render.py','scripts/export_png.mjs','scripts/print_a4.py','requirements-print.txt']
    for name in required: assert (ROOT/name).is_file(),name
    data=ROOT/'assets/data';manifest=json.loads((data/'provenance.json').read_text())
    for name,digest in manifest['sha256'].items():
        assert hashlib.sha256((data/name).read_bytes()).hexdigest()==digest,name
    count=0
    for line in (data/'graphics.txt').open(encoding='utf-8'):
        r=json.loads(line);assert len(r['strokes'])==len(r['medians']);count+=1
    for f in ROOT.rglob('*'):
        if f.suffix in ['.py','.mjs','.md','.yaml','.yml','.json'] and 'node_modules' not in f.parts and f.name!='graphics.txt':
            assert ('/'+'Users'+'/') not in f.read_text(encoding='utf-8'),str(f)
    print(f'PASS version={version}, data={count}, hashes, portable paths, required files')
if __name__=='__main__': main()
