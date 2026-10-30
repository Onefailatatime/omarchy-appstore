/* In house ads for omarchyapps.com, built by inhouse_ads.py.
 * They fill the site's own sponsor slots only while no paid sponsor holds them:
 * the homepage header and footer rotations and the app profile banner.
 * Fair rotation: each browser starts at a random ad and then steps to the
 * next one for every unit it fills, so all twenty get equal exposure and
 * no ad repeats on a page. Header and footer show three at a time.
 * Impressions count once per unit when it is half visible; clicks
 * open /adN in a new tab. */
(function(){"use strict";
var ADS=[{"r":1,"n":"Homesafe","l":"Snapshots skip your home folder. Back it up."},{"r":2,"n":"Theme Vault","l":"Twelve handcrafted themes that match every app."},{"r":3,"n":"Query Deck","l":"A fast keyboard first database client for Omarchy."},{"r":4,"n":"Tiling Mastery","l":"Master Omarchy in one weekend of video lessons."},{"r":5,"n":"Config Doctor","l":"Update Omarchy. Keep every custom tweak working."},{"r":6,"n":"Rice Market","l":"Sell your Omarchy theme. Buy a finished one."},{"r":7,"n":"WinGPU Kit","l":"Windows apps with real GPU power on Omarchy."},{"r":8,"n":"Desk Profiles","l":"Dock your laptop. Monitors arrange themselves."},{"r":9,"n":"Palette Pro","l":"Raycast style power inside your Omarchy launcher."},{"r":10,"n":"Power Tune","l":"Longer battery, cooler laptop, smarter GPU switching."},{"r":11,"n":"Focus Log","l":"See where your hours go. Wayland native."},{"r":12,"n":"Drive Bridge","l":"Google Drive and OneDrive, native in your file manager."},{"r":13,"n":"Game Key","l":"One key turns Omarchy into a gaming rig."},{"r":14,"n":"Demo Cast","l":"Terminal demos that zoom and show every keystroke."},{"r":15,"n":"Live Walls","l":"Living wallpapers that match your Omarchy theme."},{"r":16,"n":"Dot Sync","l":"Same Omarchy setup on every machine you own."},{"r":17,"n":"Shell Port","l":"Every server one keystroke away, synced everywhere."},{"r":18,"n":"Laptop Fit Packs","l":"Your exact laptop, tuned and tested for Omarchy."},{"r":19,"n":"Bar Widgets Pro","l":"CI status, calendar and battery time in your bar."},{"r":20,"n":"Snip Key","l":"Type less. Expand snippets anywhere on Omarchy."}],N=ADS.length,KEY="oa_ad_next",used=window.__oaUsed||(window.__oaUsed={});
var slots=document.querySelectorAll("[data-oa-slot]:not([data-oa-done])");
function step(){var i;try{var s=localStorage.getItem(KEY);i=s===null?Math.floor(Math.random()*N):(parseInt(s,10)%N+N)%N;localStorage.setItem(KEY,String((i+1)%N))}catch(e){i=window.__oaI===undefined?Math.floor(Math.random()*N):(window.__oaI+1)%N;window.__oaI=i}return i}
function next(){for(var t=0;t<N;t++){var ad=ADS[step()];if(!used[ad.r]){used[ad.r]=1;return ad}}return null}
function send(ad,t,page){var b=JSON.stringify({ad:ad.r,type:t,page:page});try{if(navigator.sendBeacon&&navigator.sendBeacon("/api/ads/event",new Blob([b],{type:"application/json"})))return}catch(e){}try{fetch("/api/ads/event",{method:"POST",headers:{"content-type":"application/json"},body:b,keepalive:true})}catch(e){}}
if(!document.getElementById("oa-ad-css")){var st=document.createElement("style");st.id="oa-ad-css";st.textContent=".oa-row{padding-top:0;margin-bottom:0;align-items:stretch;} .oa-row > .ad{min-width:0;display:grid;grid-template-columns:auto minmax(0,1fr) auto;grid-template-areas:\"mark name cta\" \"mark sub sub\";column-gap:0.75em;row-gap:0.2em;align-items:center;} .oa-row > .ad .copy{display:contents;} .oa-row > .ad .mark{grid-area:mark;align-self:start;} .oa-row > .ad strong{grid-area:name;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;} .oa-row > .ad .sub{grid-area:sub;} .oa-row > .ad .cta{grid-area:cta;padding:0.15em 0.55em;font-size:78%;} .ad-app-banner .oa-row > .ad{border-width:var(--border-width);} @media (max-width:760px){.ad-header .oa-row,.ad-app-banner .oa-row{display:flex;gap:var(--space-small,0.6em);overflow-x:auto;overscroll-behavior-x:contain;scroll-snap-type:x mandatory;scroll-padding-left:0;scrollbar-width:none;-webkit-overflow-scrolling:touch;} .ad-header .oa-row::-webkit-scrollbar,.ad-app-banner .oa-row::-webkit-scrollbar{display:none;} .ad-header .oa-row > .ad,.ad-app-banner .oa-row > .ad{flex:0 0 86%;scroll-snap-align:start;} .ad-footer .oa-row{gap:var(--space-small,0.6em);}}";document.head.appendChild(st)}
var io="IntersectionObserver" in window?new IntersectionObserver(function(es){for(var k=0;k<es.length;k++){if(es[k].isIntersecting){var el=es[k].target;io.unobserve(el);if(el.__oaImp)el.__oaImp()}}},{threshold:.5}):null;
function unit(ad,cls,type,pos,page){
var a=document.createElement("a");a.className=cls;
a.href="/ad"+ad.r+"?from="+encodeURIComponent(type)+(pos?"&slot="+encodeURIComponent(pos):"");a.target="_blank";a.rel="noopener";
a.setAttribute("data-oa-ad",String(ad.r));
a.innerHTML='<span class="mark" aria-hidden="true"></span><span class="copy"><strong></strong><span class="sub"></span></span><span class="cta">Join the waitlist ↗</span>';
a.querySelector(".mark").textContent=ad.n.charAt(0);a.querySelector("strong").textContent=ad.n;a.querySelector(".sub").textContent=ad.l;
a.setAttribute("aria-label",ad.n+": "+ad.l+" Opens the waitlist in a new tab.");
a.addEventListener("click",function(){send(ad,"click",page);if(window.umami)try{umami.track("house_ad_click",{ad:ad.r,page:type,slot:pos})}catch(e){}});
var seen=false;a.__oaImp=function(){if(seen)return;seen=true;send(ad,"impression",page)};
return a}
function fill(slot){
slot.setAttribute("data-oa-done","1");
var type=slot.getAttribute("data-oa-slot")||"other",pos=slot.getAttribute("data-oa-pos")||"",page=pos?type+"_"+pos:type;
var cls=slot.getAttribute("data-oa-class")||"ad",n=Math.max(1,Math.min(3,parseInt(slot.getAttribute("data-oa-count")||"1",10)||1));
var box=slot;if(n>1){box=document.createElement("div");box.className="ad-rotate oa-row";box.setAttribute("data-oa-row",pos||type);slot.appendChild(box)}
var made=[];for(var k=0;k<n;k++){var ad=next();if(!ad)break;var a=unit(ad,cls,type,pos,page);box.appendChild(a);made.push(a)}
for(var m=0;m<made.length;m++){if(io)io.observe(made[m]);else made[m].__oaImp()}}
for(var j=0;j<slots.length;j++)fill(slots[j]);
})();