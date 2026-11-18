from pathlib import Path
import re, html
root=Path(__file__).parent

def inline(s):
 s=html.escape(s)
 s=re.sub(r'https://[^\s<]+',lambda m:f'<a href="{m[0]}" target="_blank" rel="noopener noreferrer">{m[0]}</a>',s)
 return re.sub(r'(?<!\w)\[([1-7])\]',r'<a class="citation" href="#ref-\1">[\1]</a>',s)

def build(lang):
 en=lang=='en'
 text=(root/f'business-plan.{lang}.md').read_text()
 sections=[];current=None;lines=text.splitlines();i=0
 while i<len(lines):
  line=lines[i].strip()
  if line.startswith('## '):
   title=line[3:];sid='references' if title in ['참고자료','References'] else 'sec'+title.split()[0]
   current={'title':title,'id':sid,'parts':[]};sections.append(current)
  elif current and line.startswith('### '):
   title=line[4:];current['parts'].append(f'<h3 id="sub-{title.split()[0]}">{inline(title)}</h3>')
  elif current and line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r':?-+:?',c) for c in cells):rows.append(cells)
    i+=1
   head=rows.pop(0);label=html.escape(current['title'])+(' table' if en else ' 표')
   table=f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in head)+'</tr></thead><tbody>'
   for row in rows:table+='<tr>'+''.join(('<th scope="row">' if k==0 else '<td>')+inline(c)+('</th>' if k==0 else '</td>') for k,c in enumerate(row))+'</tr>'
   current['parts'].append(table+'</tbody></table></div>');continue
  elif current and line:
   para=line
   while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|')):
    i+=1;para+=' '+lines[i].strip()
   ref=re.match(r'\[([1-7])\]',para)
   attr=f' id="ref-{ref[1]}"' if current['id']=='references' and ref else ''
   current['parts'].append(f'<p{attr}>{inline(para)}</p>')
  i+=1
 nav=''.join(f'<a href="#{s["id"]}">{html.escape(s["title"])}</a>' for s in sections)
 body=''.join(f'<section id="{s["id"]}" aria-labelledby="heading-{s["id"]}"><h2 id="heading-{s["id"]}">{html.escape(s["title"])}</h2>'+''.join(s['parts'])+'</section>' for s in sections)
 title='Georgia BAM Project: F&B Business Plan' if en else '조지아 BAM 프로젝트 : F&B 사업계획서'
 subtitle='Envoy Rooftop Bistro Cafe' if en else '엔보이 루프탑 Bistro Cafe'
 toc='Contents' if en else '목차 보기'
 skip='Skip to content' if en else '본문으로 이동'
 printlabel='Save as PDF' if en else 'PDF 저장'
 back='Back to top' if en else '맨 위로'
 description='Business, menu, operations, marketing and financial plan for the Envoy Rooftop Bistro Cafe.' if en else '엔보이 루프탑 Bistro Cafe의 사업 전략, 메뉴, 운영, 마케팅 및 재무 계획.'
 languages='<div class="language-switch" role="group" aria-label="Language / 언어">'+''.join(f'<a class="language" href="{href}" lang="{code}" hreflang="{code}"'+(' aria-current="page"' if code==lang else '')+f'>{label}</a>' for code,href,label in [('ko','./','한국어'),('en','en.html','English')])+'</div>'
 page=f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{description}"><meta name="robots" content="noindex,nofollow"><title>{html.escape(title)}</title><link rel="alternate" hreflang="ko" href="./"><link rel="alternate" hreflang="en" href="en.html"><link rel="stylesheet" href="styles.css"></head><body id="top"><a class="skip" href="#main">{skip}</a><header class="topbar"><a class="brand" href="#top">Georgia BAM Project · F&B</a><div class="actions">{languages}<button id="print" type="button">{printlabel}</button></div></header><div class="layout"><aside aria-label="{toc}"><div class="version"><span>Last Updated · 2026.11.16</span></div><details id="toc" open><summary>{toc}</summary><nav aria-label="{toc}">{nav}</nav></details></aside><main id="main"><div class="cover"><div class="eyebrow">Georgia BAM Project</div><h1>{html.escape(title)}</h1><div class="subtitle">{subtitle}</div><div class="badges"><span>Last Updated · 2026.11.16</span></div></div>{body}<footer>Georgia BAM Project · F&B Business Plan · 2026.11.16</footer></main></div><a class="back-top" href="#top" aria-label="{back}">↑</a><script src="app.js"></script></body></html>'''
 output='en.html' if en else 'index.html'
 (root/output).write_text(page)
 print({'page':output,'sections':len(sections),'tables':page.count('<table>'),'paragraphs':page.count('<p')})
for lang in ['ko','en']:build(lang)
