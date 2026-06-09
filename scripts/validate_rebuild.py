#!/usr/bin/env python3
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import json, re
ROOT = Path(__file__).resolve().parents[1]
BASE = "https://superninjas.github.io/"
html_files = [p for p in ROOT.rglob('*.html') if '.git' not in p.parts]
internal_missing = []
internal_links = set()
external_links = set()
images_missing = []
products = []
for path in html_files:
    soup = BeautifulSoup(path.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
    for img in soup.find_all('img'):
        src = img.get('src','')
        if src.startswith('/') and not (ROOT / src.lstrip('/')).exists():
            images_missing.append({'page': str(path.relative_to(ROOT)), 'src': src})
    for p in soup.select('[itemscope][itemtype="https://schema.org/Product"]'):
        title = p.get_text(' ', strip=True)
        price = p.select_one('[itemprop="price"]')
        img = p.select_one('img')
        a = p.select_one('a[href]')
        products.append({'page': str(path.relative_to(ROOT)), 'has_price': bool(price), 'has_img': bool(img and img.get('src')), 'has_link': bool(a and a.get('href')), 'title': title[:120]})
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        full = urljoin(BASE, href)
        if urlparse(full).netloc == 'superninjas.github.io':
            internal_links.add(urlparse(full).path or '/')
        else:
            external_links.add(full)
for link in internal_links:
    if link.endswith('/'):
        target = ROOT / link.lstrip('/') / 'index.html'
    else:
        target = ROOT / link.lstrip('/')
    if not target.exists():
        internal_missing.append(link)
required = ['/sobre/','/contato/','/privacidade/','/termos/','/cookies/','/noticias/']
sitemap = (ROOT/'sitemap.xml').read_text(encoding='utf-8') if (ROOT/'sitemap.xml').exists() else ''
robots = (ROOT/'robots.txt').read_text(encoding='utf-8') if (ROOT/'robots.txt').exists() else ''
score = 0
checks = {
 'title_meta_canonical_og': all(BeautifulSoup((ROOT/'index.html').read_text(encoding='utf-8'), 'html.parser').find(x) for x in ['title']) and 'rel="canonical"' in (ROOT/'index.html').read_text(encoding='utf-8') and 'og:title' in (ROOT/'index.html').read_text(encoding='utf-8'),
 'sitemap_present': '<loc>' in sitemap,
 'robots_present': 'Sitemap:' in robots,
 'schema_present': 'application/ld+json' in (ROOT/'index.html').read_text(encoding='utf-8'),
 'institutional_pages': all((ROOT/r.strip('/')/'index.html').exists() for r in required),
 'category_pages': len(list((ROOT/'categorias').glob('*/index.html'))) >= 10,
 'news_sections': len(list((ROOT/'noticias').glob('*/index.html'))) >= 5,
 'no_internal_404': len(internal_missing)==0,
 'all_product_cards_complete': all(p['has_price'] and p['has_img'] and p['has_link'] for p in products),
 'sitemap_no_legacy_redirects': all(x not in sitemap for x in ['rankings/','ofertas/','dicas/','comparativos/','alertas/'])
}
score = sum(10 for v in checks.values() if v)
report = {'html_files': len(html_files), 'product_cards': len(products), 'unique_internal_links': len(internal_links), 'external_links': len(external_links), 'missing_internal_links': internal_missing, 'missing_local_images': images_missing, 'sitemap_urls': sitemap.count('<loc>'), 'checks': checks, 'seo_score_after': score}
(ROOT/'validation_after_rebuild.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
