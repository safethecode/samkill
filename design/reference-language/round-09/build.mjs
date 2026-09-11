import {build} from 'esbuild';
import {readFile,writeFile,mkdir} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('.',import.meta.url));
const parts=await Promise.all(['icons.js','model.js','view.js','app.js'].map(name=>readFile(root+'dist/'+name,'utf8')));
await mkdir(root+'.build',{recursive:true});
await writeFile(root+'.build/entry.js',"import {z} from 'zod';\n"+parts.join('\n'));
await build({entryPoints:[root+'.build/entry.js'],bundle:true,format:'iife',outfile:root+'dist/app.bundle.js',target:'es2022'});
