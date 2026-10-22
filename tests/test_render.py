import unittest,subprocess,tempfile,json,sys
from pathlib import Path
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
class RenderTests(unittest.TestCase):
    def run_cli(self,char,out):
        return subprocess.run([sys.executable,str(ROOT/'scripts/render.py'),char,'--out',str(out)],capture_output=True,text=True)
    def test_cumulative_examples(self):
        records={r['character']:r for r in map(json.loads,(ROOT/'assets/data/graphics.txt').read_text(encoding='utf-8').splitlines()) if r['character'] in ['三','财','喜']}
        with tempfile.TemporaryDirectory() as td:
            for char,n in [('三',3),('财',7),('喜',12)]:
                out=Path(td)/char;r=self.run_cli(char,out);self.assertEqual(r.returncode,0,r.stderr)
                files=sorted(out.glob('step-*.svg'));self.assertEqual(len(files),n)
                for k,f in enumerate(files,1):
                    root=ET.parse(f).getroot();all_nodes=list(root.iter())
                    paths=[e.attrib['d'] for e in all_nodes if e.tag.endswith('path') and e.attrib.get('fill')=='#808080']
                    self.assertEqual(paths,records[char]['strokes'][:k])
                    self.assertEqual(sum(e.tag.endswith('circle') and e.attrib.get('fill')=='#d92f2f' for e in all_nodes),1)
                    self.assertEqual(sum(e.tag.endswith('polygon') and e.attrib.get('fill')=='#d92f2f' for e in all_nodes),1)
                self.assertTrue((out/'licenses/APL/english/ARPHICPL.TXT').exists())
                self.assertEqual(json.loads((out/'manifest.json').read_text())['stroke_count'],n)
    def test_refuses_invalid_and_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'out'
            for char in ['财喜','🙂']:
                self.assertNotEqual(self.run_cli(char,out).returncode,0);self.assertFalse(out.exists())
            out.mkdir();sentinel=out/'keep.txt';sentinel.write_text('keep')
            self.assertNotEqual(self.run_cli('财',out).returncode,0);self.assertEqual(sentinel.read_text(),'keep')
if __name__=='__main__':unittest.main()
