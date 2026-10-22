#!/usr/bin/env node
/** Render original SVG paths, never upscale a low-resolution bitmap. */
import fs from 'node:fs/promises';
import path from 'node:path';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
async function main() {
  const args = process.argv.slice(2);
  if (args.length !== 4 || args[0] !== '--input' || args[2] !== '--out') {
    throw new Error('Usage: node scripts/export_png.mjs --input SVG_DIR --out EMPTY_PNG_DIR');
  }
  let sharp;
  try { sharp = require('sharp'); } catch { throw new Error('Missing optional dependency sharp. See README.md; no packages were installed automatically.'); }
  const input = path.resolve(args[1]), out = path.resolve(args[3]);
  const files = (await fs.readdir(input)).filter(x => /^step-\d+\.svg$/.test(x)).sort((a,b)=>Number(a.match(/\d+/)[0])-Number(b.match(/\d+/)[0]));
  if (!files.length || files.some((f,i)=>Number(f.match(/\d+/)[0])!==i+1)) throw new Error('Missing steps or non-contiguous numbering');
  await fs.access(path.join(input,'overview.svg'));
  try { if ((await fs.readdir(out)).length) throw new Error('Output directory must be empty'); }
  catch (e) { if(e.code !== 'ENOENT') throw e; }
  await fs.mkdir(out,{recursive:true});
  for (const f of [...files,'overview.svg']) {
    const width = f === 'overview.svg' ? 6000 : 4096;
    const target = path.join(out,f.replace(/\.svg$/,'.png'));
    const notice = `Cumulative Arphic-derived glyph outlines with grid and direction annotations; modified ${new Date().toISOString().slice(0,10)}. Arphic Public License; see accompanying licenses and manifest. No warranty.`;
    const xmp = `<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:description><rdf:Alt><rdf:li xml:lang="x-default">${notice}</rdf:li></rdf:Alt></dc:description></rdf:Description></rdf:RDF></x:xmpmeta>`;
    await sharp(path.join(input,f),{density:384,limitInputPixels:268402689}).resize({width}).withMetadata({density:300}).withXmp(xmp).png().toFile(target);
    const meta = await sharp(target).metadata();
    if(meta.width!==width || meta.density!==300 || (f!=='overview.svg' && meta.height!==4096)) throw new Error('PNG verification failed');
  }
  await fs.cp(path.join(input,'licenses'),path.join(out,'licenses'),{recursive:true});
  await fs.copyFile(path.join(input,'manifest.json'),path.join(out,'manifest.json'));
  console.log(JSON.stringify({steps:files.length,width:4096,dpi:300,out}));
}
main().catch(e=>{console.error(e.message);process.exitCode=1;});
