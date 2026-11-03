
document.querySelectorAll('.onepage').forEach(el=>{
  if(el.scrollHeight>el.clientHeight){const z=el.clientHeight/el.scrollHeight;
    el.style.height=(el.clientHeight/z)+'px';el.style.zoom=z;}
});
document.querySelectorAll('.fit').forEach(el=>{
  let fs=parseFloat(getComputedStyle(el).fontSize), n=0;
  while(el.scrollHeight>el.clientHeight+1 && fs>9 && n<60){fs*=0.95;el.style.fontSize=fs+'px';
    el.querySelectorAll('*').forEach(c=>{if(c.style)c.style.fontSize='';});n++;}
});
