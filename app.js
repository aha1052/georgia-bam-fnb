'use strict';
document.querySelector('#print').addEventListener('click',()=>window.print());
const toc=document.querySelector('#toc');
const mobileQuery=window.matchMedia('(max-width:900px)');
toc.open=!mobileQuery.matches;
mobileQuery.addEventListener('change',e=>{toc.open=!e.matches;});
const navLinks=[...document.querySelectorAll('nav a')];
function active(id){navLinks.forEach(a=>{if(a.hash==='#'+id)a.setAttribute('aria-current','true');else a.removeAttribute('aria-current');});}
function updateActive(){const sections=[...document.querySelectorAll('main section')];let current=sections[0];for(const section of sections){if(section.getBoundingClientRect().top<=160)current=section;}if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-10)current=sections.at(-1);if(current)active(current.id);}
let waiting=false;window.addEventListener('scroll',()=>{if(!waiting){waiting=true;requestAnimationFrame(()=>{updateActive();waiting=false;});}},{passive:true});
navLinks.forEach(a=>a.addEventListener('click',()=>{if(window.matchMedia('(max-width:900px)').matches)toc.open=false;}));
updateActive();
