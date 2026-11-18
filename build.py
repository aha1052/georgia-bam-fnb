from pathlib import Path
import re, html, shutil
root=Path(__file__).parent
source=root/'business-plan.ko.md'
text=source.read_text()
def inline(s):
 s=html.escape(s)
 s=re.sub(r'https://[^\s<]+',lambda m:f'<a href="{m[0]}" target="_blank" rel="noopener noreferrer">{m[0]}</a>',s)
 s=re.sub(r'(?<!\w)\[([1-7])\]',r'<a class="citation" href="#ref-\1">[\1]</a>',s)
 return s
sections=[];current=None;parts=[]
lines=text.splitlines();i=0
while i<len(lines):
 line=lines[i].strip()
 if line.startswith('## '):
  title=line[3:];sid='references' if title=='참고자료' else 'sec'+title.split()[0]
  current={'title':title,'id':sid,'parts':[]};sections.append(current)
 elif current and line.startswith('### '):
  title=line[4:];current['parts'].append(f'<h3 id="sub-{title.split()[0]}">{inline(title)}</h3>')
 elif current and line.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   cells=[c.strip() for c in lines[i].strip().strip('|').split('|')]
   if not all(re.fullmatch(r':?-+:?',c) for c in cells):rows.append(cells)
   i+=1
  head=rows.pop(0);table='<div class="table-wrap" tabindex="0" role="region" aria-label="'+html.escape(current['title'])+' 표"><table><thead><tr>'+''.join('<th scope="col">'+inline(c)+'</th>' for c in head)+'</tr></thead><tbody>'
  for row in rows: table+='<tr>'+''.join(('<th scope="row">' if k==0 else '<td>')+inline(c)+('</th>' if k==0 else '</td>') for k,c in enumerate(row))+'</tr>'
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
page='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="엔보이 루프탑 Bistro Cafe의 사업 전략, 메뉴, 운영, 마케팅 및 재무 계획. BAM팀과 오너십 내부 검토용."><meta name="robots" content="noindex,nofollow"><title>조지아 BAM 프로젝트 : F&B 사업계획서</title><link rel="stylesheet" href="styles.css"></head><body id="top"><a class="skip" href="#main">본문으로 이동</a><header class="topbar"><a class="brand" href="#top">Georgia BAM Project · F&B</a><div class="actions"><span class="language" lang="ko">한국어</span><button id="print" type="button">PDF 저장</button></div></header><div class="layout"><aside aria-label="사업계획서 목차"><div class="version"><span>Last Updated · 2026.11.16</span></div><details id="toc" open><summary>목차 보기</summary><nav aria-label="장별 이동">NAV</nav></details></aside><main id="main"><div class="cover"><div class="eyebrow">Georgia BAM Project</div><h1>조지아 BAM 프로젝트 :<br class="mobile-break"> F&B 사업계획서</h1><div class="subtitle">엔보이 루프탑 Bistro Cafe</div><div class="badges"><span>Last Updated · 2026.11.16</span></div></div>BODY<footer>Georgia BAM Project · F&B Business Plan · 2026.11.16</footer></main></div><a class="back-top" href="#top" aria-label="맨 위로">↑</a><script src="app.js"></script></body></html>'''.replace('NAV',nav).replace('BODY',body)
(root/'index.html').write_text(page)
print({'sections':len(sections),'tables':page.count('<table>'),'paragraphs':page.count('<p'),'characters':len(page)})
