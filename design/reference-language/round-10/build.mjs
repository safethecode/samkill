import {build} from 'esbuild';
await build({entryPoints:[new URL('./dist/app.js',import.meta.url).pathname],bundle:true,format:'iife',outfile:new URL('./dist/app.bundle.js',import.meta.url).pathname,target:'es2022'});
