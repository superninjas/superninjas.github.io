#!/usr/bin/env python3
"""
Auditoria rigorosa para aprovação do Google AdSense.
Verifica: densidade de conteúdo, duplicação, originalidade, links, imagens, indexação, URLs órfãs e CWV.
"""
from pathlib import Path
from bs4 import BeautifulSoup
import json, re
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
ISSUES = {
    'low_content_pages': [],
    'duplicate_content': defaultdict(list),
    'products_without_description': [],
    'categories_without_text': [],
    'news_without_content': [],
    'broken_internal_links': [],
    'broken_images': [],
    'orphan_urls': [],
    'indexation_issues': [],
    'cwv_concerns': []
}

def count_words(text):
    """Conta palavras em um texto."""
    return len(re.findall(r'\b\w+\b', text.lower()))

def extract_text_content(soup):
    """Extrai texto limpo de uma página."""
    for script in soup(['script', 'style']):
        script.decompose()
    return soup.get_text(separator=' ', strip=True)

def audit_page(page_path, page_url):
    """Audita uma página individual."""
    try:
        content = page_path.read_text(encoding='utf-8', errors='ignore')
        soup = BeautifulSoup(content, 'html.parser')
        text = extract_text_content(soup)
        word_count = count_words(text)
        
        # 1. Páginas com pouco conteúdo
        if word_count < 800:
            ISSUES['low_content_pages'].append({
                'url': page_url,
                'words': word_count,
                'path': str(page_path.relative_to(ROOT))
            })
        
        # 2. Verificar se há descrição em produtos
        if '/ofertas/' in str(page_path) or '/categorias/' in str(page_path):
            products = soup.select('article.product')
            for prod in products:
                desc = prod.select_one('.product-description, p, .desc')
                if not desc or count_words(desc.get_text()) < 50:
                    ISSUES['products_without_description'].append({
                        'url': page_url,
                        'path': str(page_path.relative_to(ROOT))
                    })
        
        # 3. Verificar categorias sem texto editorial
        if '/categorias/' in str(page_path):
            intro = soup.select_one('.category-intro, .intro, .description')
            if not intro or count_words(intro.get_text()) < 100:
                ISSUES['categories_without_text'].append({
                    'url': page_url,
                    'path': str(page_path.relative_to(ROOT))
                })
        
        # 4. Verificar notícias sem conteúdo próprio
        if '/noticias/' in str(page_path):
            article = soup.select_one('article, .article-content, main')
            if article:
                article_text = count_words(article.get_text())
                if article_text < 300:
                    ISSUES['news_without_content'].append({
                        'url': page_url,
                        'words': article_text,
                        'path': str(page_path.relative_to(ROOT))
                    })
        
        # 5. Links internos quebrados
        for a in soup.select('a[href]'):
            href = a.get('href', '')
            if href.startswith('/') and not href.startswith('//'):
                target = ROOT / href.lstrip('/')
                if not target.exists() and not target.with_name('index.html').exists():
                    ISSUES['broken_internal_links'].append({
                        'from': page_url,
                        'to': href,
                        'path': str(page_path.relative_to(ROOT))
                    })
        
        # 6. Imagens quebradas (verificar atributos)
        for img in soup.select('img[src]'):
            src = img.get('src', '')
            if src.startswith('/'):
                img_path = ROOT / src.lstrip('/')
                if not img_path.exists():
                    ISSUES['broken_images'].append({
                        'url': page_url,
                        'src': src,
                        'path': str(page_path.relative_to(ROOT))
                    })
            # Verificar atributos alt (importante para SEO/acessibilidade)
            if not img.get('alt'):
                ISSUES['cwv_concerns'].append({
                    'type': 'missing_alt_text',
                    'url': page_url,
                    'path': str(page_path.relative_to(ROOT))
                })
        
        # 7. Verificar indexação (robots, canonical)
        robots_meta = soup.select_one('meta[name="robots"]')
        if robots_meta and 'noindex' in robots_meta.get('content', ''):
            ISSUES['indexation_issues'].append({
                'type': 'noindex',
                'url': page_url,
                'path': str(page_path.relative_to(ROOT))
            })
        
        # 8. Verificar canonical
        canonical = soup.select_one('link[rel="canonical"]')
        if not canonical:
            ISSUES['cwv_concerns'].append({
                'type': 'missing_canonical',
                'url': page_url,
                'path': str(page_path.relative_to(ROOT))
            })
        
        return True
    except Exception as e:
        ISSUES['indexation_issues'].append({
            'type': 'parse_error',
            'url': page_url,
            'error': str(e)[:100]
        })
        return False

def find_orphan_urls():
    """Encontra URLs órfãs (não linkadas internamente)."""
    all_urls = set()
    linked_urls = set()
    
    for html_file in ROOT.rglob('index.html'):
        if '.git' in str(html_file):
            continue
        url = '/' + str(html_file.relative_to(ROOT)).replace('index.html', '').replace('\\', '/')
        all_urls.add(url)
        
        try:
            soup = BeautifulSoup(html_file.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
            for a in soup.select('a[href]'):
                href = a.get('href', '').split('#')[0]
                if href.startswith('/'):
                    linked_urls.add(href.rstrip('/') or '/')
        except:
            pass
    
    orphans = all_urls - linked_urls
    for orphan in orphans:
        if orphan not in ['/', '/index.html', '/404.html']:
            ISSUES['orphan_urls'].append({'url': orphan})

def check_duplicate_content():
    """Detecta conteúdo duplicado entre páginas."""
    content_hashes = defaultdict(list)
    
    for html_file in ROOT.rglob('index.html'):
        if '.git' in str(html_file):
            continue
        try:
            soup = BeautifulSoup(html_file.read_text(encoding='utf-8', errors='ignore'), 'html.parser')
            text = extract_text_content(soup)[:500]  # Primeiras 500 chars
            content_hash = hash(text)
            url = '/' + str(html_file.relative_to(ROOT)).replace('index.html', '').replace('\\', '/')
            content_hashes[content_hash].append(url)
        except:
            pass
    
    for hash_val, urls in content_hashes.items():
        if len(urls) > 1:
            ISSUES['duplicate_content'][str(hash_val)] = urls

# Executar auditorias
print("🔍 Auditando páginas...")
for html_file in ROOT.rglob('index.html'):
    if '.git' in str(html_file):
        continue
    url = '/' + str(html_file.relative_to(ROOT)).replace('index.html', '').replace('\\', '/')
    audit_page(html_file, url)

print("🔍 Procurando URLs órfãs...")
find_orphan_urls()

print("🔍 Detectando conteúdo duplicado...")
check_duplicate_content()

# Gerar relatório
report = {
    'timestamp': '2026-06-09',
    'total_issues': sum(len(v) if isinstance(v, list) else len(v) for v in ISSUES.values()),
    'issues': {
        'low_content_pages': {
            'count': len(ISSUES['low_content_pages']),
            'items': ISSUES['low_content_pages']
        },
        'duplicate_content': {
            'count': len(ISSUES['duplicate_content']),
            'items': list(ISSUES['duplicate_content'].values())[:10]  # Top 10
        },
        'products_without_description': {
            'count': len(ISSUES['products_without_description']),
            'items': ISSUES['products_without_description'][:20]
        },
        'categories_without_text': {
            'count': len(ISSUES['categories_without_text']),
            'items': ISSUES['categories_without_text']
        },
        'news_without_content': {
            'count': len(ISSUES['news_without_content']),
            'items': ISSUES['news_without_content']
        },
        'broken_internal_links': {
            'count': len(ISSUES['broken_internal_links']),
            'items': ISSUES['broken_internal_links'][:20]
        },
        'broken_images': {
            'count': len(ISSUES['broken_images']),
            'items': ISSUES['broken_images'][:20]
        },
        'orphan_urls': {
            'count': len(ISSUES['orphan_urls']),
            'items': ISSUES['orphan_urls'][:20]
        },
        'indexation_issues': {
            'count': len(ISSUES['indexation_issues']),
            'items': ISSUES['indexation_issues'][:20]
        },
        'cwv_concerns': {
            'count': len(ISSUES['cwv_concerns']),
            'items': ISSUES['cwv_concerns'][:20]
        }
    }
}

# Salvar relatório
(ROOT / 'adsense_audit_report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
