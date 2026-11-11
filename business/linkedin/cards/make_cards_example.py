import re,json
base=open('card.html').read()
def make(name,tag,kick,big,sub,rows,url,src):
    h=base
    h=re.sub(r'<div class="tag">.*?</div>',f'<div class="tag">{tag}</div>',h)
    h=re.sub(r'<div class="kick">.*?</div>',f'<div class="kick">{kick}</div>',h)
    h=re.sub(r'<div class="big">.*?</div>',f'<div class="big">{big}</div>',h)
    h=re.sub(r'<div class="sub">.*?</div>',f'<div class="sub">{sub}</div>',h)
    h=re.sub(r'<ul>.*?</ul>','<ul>'+''.join(f'<li>{a}<em>{b}</em></li>' for a,b in rows)+'</ul>',h,flags=re.S)
    h=re.sub(r'<div class="url">.*?</div>',f'<div class="url">{url}</div>',h)
    h=re.sub(r'<div class="src">.*?</div>',f'<div class="src">{src}</div>',h)
    open(name+'.html','w').write(h)
make('2026-11-12-buyer-brief','Buyer brief · live','Wanted · ready 3-bed apartment · Dubai','<span>AED</span> 10–12M','At or <b>below</b> the original purchase price',
 [('Where','Marina · Emaar Beachfront · Palm'),('Stock','Completed, ready only'),('Layout','At least two en-suite bedrooms'),('Buyer','High net worth · ready now')],
 'dealdeed.ae/desk#briefs','Agents: submit asking price, original purchase price, size, floor plan and occupancy. Agent to agent. Your client stays yours.')
make('2026-11-13-athlon-townhouse','On the desk · Dubailand','3-bedroom townhouse · Athlon by Aldar','<span>AED</span> 3.05M','<b>AED 167,000 under</b> the 2024 purchase price',
 [('Built-up','2,300 sq ft'),('Plot','2,000 sq ft · larger than most'),('Asking, per sq ft','c. AED 1,326'),('Handover','2028 · balance on Aldar’s plan')],
 'dealdeed.ae/desk','Purchase price checked against the developer’s statement of account before introduction. Figures as published on dealdeed.ae, 11 November 2026.')
