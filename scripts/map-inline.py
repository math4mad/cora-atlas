#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""map-inline.py — 地铁图定位功能挂碑 (主人 0924 令: 项目主页高亮个体站, 半透明显上级项目群)
只动地铁图: 在 topography.html 里把 topos-flat.svg 内联 (img 养不活脚本), 挂 here/kin/dim 三段光照。
用法: python3 scripts/map-inline.py  (build-site.sh 尾部调用, 幂等: 已注入即跳过)"""
import re, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
html_p, svg_p = root/"docs/topography.html", root/"docs/figs/topos-flat.svg"
if not html_p.exists() or not svg_p.exists():
    print("· 缺页或缺图, 跳过"); raise SystemExit(0)
html = html_p.read_text()
if "garden-metro" in html:
    print("· 地铁图已注入, 跳过"); raise SystemExit(0)

svg = svg_p.read_text()
m = re.search(r'<img[^>]*topos-flat\.svg[^>]*>', html)
if not m:
    print("· 未找到 flat 图 <img>, 跳过"); raise SystemExit(0)

script = """
<div id="metro-holder" style="overflow-x:auto">__SVG__</div>
<script>
(function(){
 var svg=document.getElementById('garden-metro'); if(!svg)return;
 var G=JSON.parse(svg.getAttribute('data-groups')); var st2g={};
 for(var g in G){G[g].members.forEach(function(k){st2g[k]=g;});}
 var lnwrap=svg.querySelector('#lnwrap');
 function clear(){
   svg.querySelectorAll('.st').forEach(function(e){e.classList.remove('dim','kin','here');});
   if(lnwrap)lnwrap.querySelectorAll('path').forEach(function(p){p.setAttribute('opacity','.88');});
   var t=document.getElementById('metro-here'); if(t)t.remove();
 }
 function apply(id){
   clear(); var el=svg.querySelector('#st-'+id); if(!el)return;
   var grp=el.getAttribute('data-group');
   svg.querySelectorAll('.st').forEach(function(e){
     if(e===el)e.classList.add('here');
     else if(e.getAttribute('data-group')===grp)e.classList.add('kin');
     else e.classList.add('dim');
   });
   if(lnwrap)lnwrap.querySelectorAll('path').forEach(function(p){
     var via=(p.getAttribute('data-via')||'').split(' ');
     var keep=via.indexOf(id)>=0||via.some(function(v){return st2g[v]===grp;});
     p.setAttribute('opacity',keep?'.88':'.06');
   });
   var chip=document.createElement('div'); chip.id='metro-here';
   chip.style.cssText='font:12px/1.4 -apple-system,system-ui;color:#6f6558;letter-spacing:1px;padding:.3rem .7rem;border:1px solid #d8cba6;background:#fff9ea;border-radius:999px;display:inline-block;margin:.4rem 0';
   chip.textContent='Here 在此 · '+el.getAttribute('data-name')+'　|　Group 群 · '+(G[grp]?G[grp].label:'—')+'　|　Whole 园体';
   var holder=document.getElementById('metro-holder');
   holder.parentNode.insertBefore(chip,holder);
   if(history.replaceState)history.replaceState(null,'','?at='+id);
 }
 svg.querySelectorAll('.st').forEach(function(e){
   e.addEventListener('click',function(ev){ev.stopPropagation();apply(e.id.replace('st-',''));});
 });
 document.addEventListener('click',function(ev){
   if(ev.target.closest&&ev.target.closest('#metro-holder'))return;
   clear(); if(history.replaceState)history.replaceState(null,'','topography.html');
 });
 var at=(new URLSearchParams(location.search)).get('at');
 if(at&&(at in st2g||svg.querySelector('#st-'+at)))apply(at);
})();
</script>
"""
html = html[:m.start()] + script.replace("__SVG__", svg) + html[m.end():]
html_p.write_text(html)
print("· 地铁图已内联挂光照 (topography.html)")
