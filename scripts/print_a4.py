#!/usr/bin/env python3
"""A4 cumulative stroke sheet. Requires existing reportlab; never installs packages."""
import argparse, json, shutil, datetime
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
p=argparse.ArgumentParser();p.add_argument('character');p.add_argument('--images',type=Path,required=True);p.add_argument('--font',required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
steps=sorted(a.images.glob('step-*.png'), key=lambda x:int(x.stem.split('-')[1]))
if not steps: p.error('缺少步骤图片')
if len(a.character)!=1: p.error('请输入单个汉字')
if a.out.exists(): p.error('PDF已存在；请使用新路径，避免覆盖')
manifest=json.loads((a.images/'manifest.json').read_text(encoding='utf-8'))
if manifest['character']!=a.character or manifest['stroke_count']!=len(steps) or any(int(f.stem.split('-')[1])!=i+1 for i,f in enumerate(steps)): p.error('图片数量、编号或汉字与manifest不一致')
if not Path(a.font).is_file(): p.error('找不到中文TTF字体；请指定自己机器上的合法字体路径')
pdfmetrics.registerFont(TTFont('body',a.font))
a.out.parent.mkdir(parents=True,exist_ok=True)
c=canvas.Canvas(str(a.out),pagesize=A4);c.setTitle(a.character+'·楷书笔顺');c.setAuthor('Victor使用Codex制作');c.setSubject('Cumulative glyph extraction with grid and directions; modified '+datetime.date.today().isoformat()+'; Arphic Public License, see accompanying licenses. No warranty.')
for offset in range(0,len(steps),8):
 c.setFont('body',17);c.setFillColorRGB(.25,.25,.25);c.drawCentredString(105*mm,282*mm,a.character+' · 楷书笔顺')
 c.setFont('body',9);c.drawCentredString(105*mm,274*mm,'红点起笔，沿红线书写，箭头处收笔。')
 for j,f in enumerate(steps[offset:offset+8]):
  col=j%2;row=j//2;x=(35+90*col)*mm;y=(214-61*row)*mm
  c.drawImage(str(f),x,y,width=50*mm,height=50*mm)
  c.setFont('body',9);c.drawCentredString(x+25*mm,y-4*mm,f'{offset+j+1}/{len(steps)}')
 c.setFont('body',6);c.setFillColorRGB(.4,.4,.4);c.drawCentredString(105*mm,12*mm,'楷书笔顺演示 · 字形：Make Me a Hanzi / Arphic · 许可见随附说明')
 c.showPage()
c.save()
license_out=a.out.parent/'licenses'
if license_out.resolve()!=(a.images/'licenses').resolve(): shutil.copytree(a.images/'licenses',license_out,dirs_exist_ok=True)
