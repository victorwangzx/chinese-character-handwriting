#!/usr/bin/env python3
"""Deterministic cumulative SVGs; Python standard library only."""
import argparse, json, html, math, shutil, hashlib, datetime
from pathlib import Path
from xml.etree import ElementTree as ET

NOTICE = '楷书笔顺演示 | Make Me a Hanzi; Arphic PL KaitiM GB / PL UKai; Arphic Public License. See accompanying COPYING and APL licenses.'

def grid():
    return '<rect width="1024" height="1024" fill="white"/><rect x="2" y="2" width="1020" height="1020" fill="none" stroke="#a6ceb0" stroke-width="4"/><path d="M512 2V1022 M2 512H1022" fill="none" stroke="#c1dfc6" stroke-width="2" stroke-dasharray="12 10"/>'

def cell(strokes, medians, k):
    paths = ''.join('<path fill="%s" d="%s"/>' % ('#808080',html.escape(d, quote=True)) for i,d in enumerate(strokes[:k]))
    points=medians[k-1]
    start=points[0]; end=points[-1]
    previous=next((v for v in reversed(points[:-1]) if v!=end),None)
    if previous is None: raise ValueError('行笔中线无有效方向')
    dx=end[0]-previous[0]; dy=end[1]-previous[1]; length=math.hypot(dx,dy)
    ux,uy=dx/length,dy/length
    left=(end[0]-ux*25-uy*13,end[1]-uy*25+ux*13)
    right=(end[0]-ux*25+uy*13,end[1]-uy*25-ux*13)
    d='M'+' L'.join(f'{x} {y}' for x,y in points)
    annotation=f'<path d="{d}" fill="none" stroke="#d92f2f" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/><circle cx="{start[0]}" cy="{start[1]}" r="11" fill="#d92f2f"/><polygon points="{end[0]},{end[1]} {left[0]},{left[1]} {right[0]},{right[1]}" fill="#d92f2f"/>'
    return grid() + '<g transform="translate(102.4 102.4) scale(0.8)"><g transform="scale(1 -1) translate(0 -900)">' + paths + annotation + '</g></g>'

def svg(body, w=1024, h=1024):
    return '<svg xmlns="http://www.w3.org/2000/svg" width="%s" height="%s" viewBox="0 0 %s %s"><metadata>%s</metadata>%s</svg>' % (w,h,w,h,html.escape(NOTICE+' Modified: cumulative outlines with grid and directions, '+datetime.datetime.now(datetime.timezone.utc).date().isoformat()+'; derivative graphics under Arphic Public License.'),body)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('character'); p.add_argument('--out',required=True,type=Path)
    p.add_argument('--data',type=Path,default=Path(__file__).resolve().parents[1]/'assets/data/graphics.txt',help="仅接受随包核验数据；保留此参数供诊断")
    a=p.parse_args()
    if a.data.resolve() != (Path(__file__).resolve().parents[1]/'assets/data/graphics.txt').resolve(): p.error('公开版仅接受内置许可数据；自定义字形请先适配来源与许可处理')
    if len(a.character)!=1: p.error('请输入单个汉字')
    if not a.data.is_file(): p.error('找不到字形数据，请检查完整安装包或 --data 路径')
    record=None
    with a.data.open(encoding='utf-8') as f:
        for line in f:
            r=json.loads(line)
            if r.get('character')==a.character: record=r; break
    if not record or not record.get('strokes'): p.error('数据未覆盖此字；不可猜造笔画')
    strokes=record['strokes']; n=len(strokes)
    medians=record.get('medians',[])
    if len(medians)!=n or any(not isinstance(m,list) or len(m)<2 for m in medians): p.error('缺少逐笔行笔中线，不可猜造箭头')
    if not all(isinstance(d,str) and d.strip() for d in strokes): p.error('无效路径')
    for median in medians:
        if any(not isinstance(v,list) or len(v)!=2 or any(not isinstance(t,(int,float)) or not math.isfinite(t) or abs(t)>100000 for t in v) for v in median): p.error('行笔中线坐标无效')
        if all(v==median[-1] for v in median): p.error('行笔中线无有效方向')
    if a.out.exists() and (not a.out.is_dir() or any(a.out.iterdir())): p.error('输出目录须为空，避免混入旧步骤')
    a.out.mkdir(parents=True,exist_ok=True)
    for k in range(1,n+1):
        content=svg(cell(strokes,medians,k))
        root=ET.fromstring(content)
        paths=root.findall('.//{http://www.w3.org/2000/svg}g/{http://www.w3.org/2000/svg}g/{http://www.w3.org/2000/svg}path')
        assert [v.attrib['d'] for v in paths if v.attrib.get('fill')=='#808080']==strokes[:k]
        assert sum(v.attrib.get('stroke')=='#d92f2f' for v in paths)==1
        (a.out/f'step-{k:02}.svg').write_text(content,encoding='utf-8')
    cols=min(n,4); rows=math.ceil(n/cols)
    body='<rect width="100%" height="100%" fill="white"/>'
    for i in range(n):
        x=(i%cols)*280+12; y=(i//cols)*300+12
        body+=f'<g transform="translate({x} {y}) scale(0.25)">{cell(strokes,medians,i+1)}</g>'
        body+=f'<text x="{x+128}" y="{y+278}" text-anchor="middle" font-family="sans-serif" font-size="16">{i+1}/{n}</text>'
    (a.out/'overview.svg').write_text(svg(body,cols*280,rows*300),encoding='utf-8')
    license_dir=a.out/'licenses'
    license_dir.mkdir()
    bundled=Path(__file__).resolve().parents[1]/'assets/data'
    for name in ['COPYING','APL','provenance.json']:
        source=bundled/name
        if source.is_dir(): shutil.copytree(source,license_dir/name)
        else: shutil.copy2(source,license_dir/name)
    manifest={'character':a.character,'stroke_count':n,'source_sha256':hashlib.sha256(a.data.read_bytes()).hexdigest(),'style':{'glyph':'#808080','arrow':'#d92f2f','grid':'#a6ceb0','grid_inner':'#c1dfc6'},'generated_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'notice':NOTICE,'modification':'Cumulative stroke extraction with grid and direction annotations; original data unchanged. Generated derivative graphics supplied under Arphic Public License.','standard_review':'Agent must verify target character before teaching delivery.'}
    (a.out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'character':a.character,'strokes':n,'steps':n,'out':str(a.out)},ensure_ascii=False))
if __name__=='__main__': main()
