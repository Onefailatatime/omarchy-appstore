/* In house ads for omarchyapps.com, built by inhouse_ads.py.
 * Fair rotation: each browser starts at a random ad and then steps to the
 * next one on every page view, so all twenty get equal exposure on every
 * page type. Impressions count once per page view when the ad is half
 * visible; clicks open /adN in a new tab. */
(function(){"use strict";
var ADS=[{"r":1,"n":"Homesafe","l":"Snapshots skip your home folder. Back it up."},{"r":2,"n":"Theme Vault","l":"Twelve handcrafted themes that match every app."},{"r":3,"n":"Query Deck","l":"A fast keyboard first database client for Omarchy."},{"r":4,"n":"Tiling Mastery","l":"Master Omarchy in one weekend of video lessons."},{"r":5,"n":"Config Doctor","l":"Update Omarchy. Keep every custom tweak working."},{"r":6,"n":"Rice Market","l":"Sell your Omarchy theme. Buy a finished one."},{"r":7,"n":"WinGPU Kit","l":"Windows apps with real GPU power on Omarchy."},{"r":8,"n":"Desk Profiles","l":"Dock your laptop. Monitors arrange themselves."},{"r":9,"n":"Palette Pro","l":"Raycast style power inside your Omarchy launcher."},{"r":10,"n":"Power Tune","l":"Longer battery, cooler laptop, smarter GPU switching."},{"r":11,"n":"Focus Log","l":"See where your hours go. Wayland native."},{"r":12,"n":"Drive Bridge","l":"Google Drive and OneDrive, native in your file manager."},{"r":13,"n":"Game Key","l":"One key turns Omarchy into a gaming rig."},{"r":14,"n":"Demo Cast","l":"Terminal demos that zoom and show every keystroke."},{"r":15,"n":"Live Walls","l":"Living wallpapers that match your Omarchy theme."},{"r":16,"n":"Dot Sync","l":"Same Omarchy setup on every machine you own."},{"r":17,"n":"Shell Port","l":"Every server one keystroke away, synced everywhere."},{"r":18,"n":"Laptop Fit Packs","l":"Your exact laptop, tuned and tested for Omarchy."},{"r":19,"n":"Bar Widgets Pro","l":"CI status, calendar and battery time in your bar."},{"r":20,"n":"Snip Key","l":"Type less. Expand snippets anywhere on Omarchy."}],N=ADS.length,KEY="oa_ad_next";
var slot=document.querySelector("[data-oa-slot]");if(!slot)return;
var type=slot.getAttribute("data-oa-slot")||"other",i;
try{var s=localStorage.getItem(KEY);i=s===null?Math.floor(Math.random()*N):(parseInt(s,10)%N+N)%N;localStorage.setItem(KEY,String((i+1)%N))}catch(e){i=Math.floor(Math.random()*N)}
var ad=ADS[i];
function send(t){var b=JSON.stringify({ad:ad.r,type:t,page:type});try{if(navigator.sendBeacon&&navigator.sendBeacon("/api/ads/event",new Blob([b],{type:"application/json"})))return}catch(e){}try{fetch("/api/ads/event",{method:"POST",headers:{"content-type":"application/json"},body:b,keepalive:true})}catch(e){}}
if(!document.getElementById("oa-ad-css")){var st=document.createElement("style");st.id="oa-ad-css";st.textContent=
".oa-house{max-width:var(--maxw,76rem);margin:.6rem auto 0;padding:0 var(--space-medium,1rem)}"+
".oa-house a{display:flex;align-items:center;gap:.65em;padding:.5em .8em;border:var(--border-width,1px) solid var(--border-color,rgba(65,72,104,.8));border-radius:var(--radius,.4em);background:rgba(36,40,59,.55);color:rgb(192,202,245);text-decoration:none;font-size:.86rem;line-height:1.35;transition:border-color .15s}"+
".oa-house a:hover,.oa-house a:focus-visible{border-color:rgb(122,162,247)}"+
".oa-house .t{flex:none;padding:.05em .45em;border:1px solid rgba(255,158,100,.6);border-radius:.3em;color:rgb(255,158,100);font:700 .7rem/1.5 var(--font-family,monospace);letter-spacing:.03em}"+
".oa-house .c{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}"+
".oa-house .c b{color:rgb(125,207,255);font-weight:600;margin-right:.45em}"+
".oa-house .g{flex:none;color:rgb(122,162,247);font:700 .78rem/1.3 var(--font-family,monospace)}"+
"@media (max-width:40rem){.oa-house .c{white-space:normal}.oa-house .g .x{display:none}}";
document.head.appendChild(st)}
var a=document.createElement("a");a.href="/ad"+ad.r+"?from="+encodeURIComponent(type);a.target="_blank";a.rel="noopener";
a.setAttribute("data-oa-ad",String(ad.r));
a.innerHTML='<span class="t">FROM US</span><span class="c"><b></b><span></span></span><span class="g"><span class="x">Join the waitlist </span>↗</span>';
a.querySelector(".c b").textContent=ad.n;a.querySelector(".c span").textContent=ad.l;
a.setAttribute("aria-label",ad.n+": "+ad.l+" Opens the waitlist in a new tab.");
a.addEventListener("click",function(){send("click");if(window.umami)try{umami.track("house_ad_click",{ad:ad.r,page:type})}catch(e){}});
slot.appendChild(a);slot.hidden=false;
var seen=false;function imp(){if(seen)return;seen=true;send("impression")}
if("IntersectionObserver" in window){var io=new IntersectionObserver(function(es){for(var k=0;k<es.length;k++){if(es[k].isIntersecting){imp();io.disconnect()}}},{threshold:.5});io.observe(slot)}else imp();
})();