const {chromium}=require('playwright');const fs=require('fs');const http=require('http');const path=require('path');
const srv=http.createServer((q,r)=>{const p=path.join(__dirname,decodeURIComponent(q.url.split('?')[0]));fs.readFile(p,(e,d)=>{if(e){r.writeHead(404);return r.end()}const t=p.endsWith('.js')?'text/javascript':p.endsWith('.html')?'text/html':'application/octet-stream';r.writeHead(200,{'Content-Type':t});r.end(d)})}).listen(8765,async()=>{
 const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const pg=await b.newPage({viewport:{width:1200,height:1400}});
 pg.on('console',m=>console.log('console',m.text()));
 await pg.goto('http://localhost:8765/bust.html');await pg.waitForFunction('window.ready===true');
 const jobs=[['lee','bust_front',0,0.08,1.55],['lee','bust_34',-0.6,0.1,1.55],['lee','bust_profile',-1.5,0.05,1.6],['lee','bust_34r',0.55,0.12,1.55],['lee','bust_up',-0.3,-0.35,1.5]];
 let cur='';for(const [w,n,y,p,d] of jobs){if(w!==cur){await pg.evaluate(x=>window.load(x),w);cur=w}
  const url=await pg.evaluate(([y,p,d])=>window.shot(y,p,d),[y,p,d]);fs.writeFileSync(n+'.png',Buffer.from(url.split(',')[1],'base64'));console.log('ok',n)}
 await b.close();srv.close()});
