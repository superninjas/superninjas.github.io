#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
import requests, json
ROOT = Path(__file__).resolve().parents[1]
links = []
for p in [ROOT/'index.html'] + list((ROOT/'categorias').glob('*/index.html')):
    if not p.exists():
        continue
    soup = BeautifulSoup(p.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
    for a in soup.select('article.product a[href^="https://lista.mercadolivre.com.br/"]'):
        links.append(a['href'])
unique = sorted(set(links))
results = []
for url in unique:
    try:
        r = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}, timeout=12, allow_redirects=True)
        results.append({'url': url, 'status': r.status_code, 'ok_not_404': r.status_code != 404})
    except Exception as e:
        results.append({'url': url, 'status': 'error', 'ok_not_404': False, 'error': str(e)[:120]})
summary = {'checked_unique_product_destinations': len(unique), 'not_404': sum(1 for x in results if x['ok_not_404']), 'errors_or_404': [x for x in results if not x['ok_not_404']]}
(ROOT/'external_product_link_check.json').write_text(json.dumps({'summary': summary, 'results': results}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
