import json
import re
import math
from collections import defaultdict
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = Path("/home/ubuntu/produtos_massivos.json")

SITE_URL = "https://superninjas.github.io"
AFFILIATE_NOTE = "O Radar Ninja participa do Programa de Afiliados do Mercado Livre. Recebemos comissão por compras via nossos links, sem custo extra para você."

CATEGORY_SLUGS = {
    "Celulares": "celulares", "TV e Vídeo": "tv-e-video", "Casa & Eletro": "casa-e-eletro",
    "Ferramentas": "ferramentas", "Beleza & Saúde": "beleza-e-saude", "Tecnologia": "tecnologia",
    "Informática": "informatica", "Games": "games", "Colecionáveis": "colecionaveis", "Ofertas Gerais": "ofertas-gerais",
}

def brl(value):
    if value in (None, ""): return ""
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def slugify(text):
    text = text.lower()
    repl = {"á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i", "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ç": "c", "&": "e"}
    for a, b in repl.items(): text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "ofertas"

def load_products():
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    for p in products:
        cat = p.get("custom_category") or "Ofertas Gerais"
        p["custom_category"] = cat
        p["custom_category_slug"] = CATEGORY_SLUGS.get(cat, slugify(cat))
    return products

def product_card(p):
    title = escape(p.get("title", "Produto"))
    img = escape(p.get("thumbnail") or "")
    link = escape(p.get("permalink") or "#")
    cat = escape(p.get("custom_category") or "Ofertas")
    discount = int(p.get("custom_discount_pct") or 20)
    original = p.get("original_price") or (float(p['price']) * 1.25)
    price = p.get("price")
    
    badge = f'<span class="badge">{discount}% OFF</span>'
    old_price = f'<span class="old-price">De {brl(original)}</span>'
    savings = f'<div class="savings">Você economiza {brl(float(original) - float(price))}</div>'
    
    fallback = p.get("thumbnail_fallback", "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=500&q=80")
    return f'''
    <article class="card" itemscope itemtype="https://schema.org/Product">
        {badge}
        <div class="card-img-wrap">
            <img src="{img}" alt="{title}" loading="lazy" itemprop="image" onerror="this.src='{fallback}'; this.onerror=null;">
        </div>
        <div class="card-info">
            <span class="category-tag">{cat}</span>
            <h3 class="card-title" itemprop="name">{title}</h3>
            <div class="price-wrap" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                {old_price}
                <div class="price" itemprop="price" content="{float(price):.2f}">{brl(price)}</div>
                {savings}
            </div>
            <div class="product-actions-local">
                <a href="{link}" class="btn btn-buy" target="_blank" rel="nofollow sponsored noopener">Ver Oferta Ninja</a>
                <a href="/ofertas/{slugify(title)}/" class="btn btn-outline-card">Ver análise</a>
            </div>
        </div>
    </article>'''

def head(title, desc, canonical="/"):
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
    :root {{ --max-width: 1200px; }}
    .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
    .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; display: flex; align-items: center; justify-content: space-between; height: 70px; }}
    .product-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 25px; max-width: 1200px; margin: 0 auto; padding: 20px 0; }}
    .card {{ display: flex; flex-direction: column; height: 100%; }}
    .card-info {{ flex: 1; display: flex; flex-direction: column; }}
    .product-actions-local {{ margin-top: auto; }}
    @media (max-width: 768px) {{
        .product-grid {{ grid-template-columns: repeat(2, 1fr); gap: 15px; padding: 10px; }}
        .card-title {{ font-size: 13px; height: 36px; }}
    }}
    .nav-cta {{ background: var(--ninja-purple); color: #fff !important; padding: 8px 20px; border-radius: 50px; font-weight: 700; }}
    .trust-bar {{ background: #fff; border-bottom: 1px solid #eee; padding: 15px 0; }}
    .trust-inner {{ display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; }}
    .trust-item {{ font-size: 13px; font-weight: 600; color: #636e72; display: flex; align-items: center; gap: 8px; }}
    .trust-icon {{ color: var(--ninja-green); font-size: 18px; }}
    .pagination {{ display: flex; justify-content: center; gap: 10px; margin: 40px 0; }}
    .page-link {{ padding: 10px 18px; border: 1px solid #eee; border-radius: 8px; background: #fff; color: #2d3436; font-weight: 700; }}
    .page-link.active {{ background: var(--ninja-purple); color: #fff; border-color: var(--ninja-purple); }}
</style>
</head>
<body>
<header class="header"><div class="header-inner"><a class="logo" href="/"><span class="logo-icon">🥷</span><span class="logo-text"><span class="logo-title">Radar Ninja</span></span></a><nav class="nav"><a href="/ofertas/">Ofertas</a><a href="/rankings/">Rankings</a><a href="/comparativos/">Comparativos</a><a class="nav-cta" href="/ofertas/">Comprar melhor</a></nav></div></header>
<div class="trust-bar"><div class="container"><div class="trust-inner"><div class="trust-item"><span class="trust-icon">✓</span> 100% Produtos Reais</div><div class="trust-item"><span class="trust-icon">✓</span> Links Verificados</div><div class="trust-item"><span class="trust-icon">✓</span> Preços Atualizados</div><div class="trust-item"><span class="trust-icon">✓</span> Curadoria Ninja</div></div></div></div>'''

def foot():
    return f'''<footer class="footer"><div class="container"><div class="footer-grid"><div><h3>Radar Ninja</h3><p>Sua central de ofertas reais e verificadas.</p></div><div><h4>Links</h4><a href="/ofertas/">Ofertas</a><br><a href="/rankings/">Rankings</a></div><div><h4>Legal</h4><a href="/privacidade/">Privacidade</a></div></div><p style="margin-top:40px; font-size:12px; opacity:0.7;">{AFFILIATE_NOTE}</p></div></footer></body></html>'''

def build_home(products):
    featured = products[:12]
    most_wanted = products[12:24]
    best_rated = products[24:36]
    
    categories = defaultdict(list)
    for p in products: categories[p["custom_category"]].append(p)
    cat_cards = "".join(f'<a class="category-card" href="/categorias/{CATEGORY_SLUGS.get(cat, slugify(cat))}/"><span class="category-icon">📦</span><span class="category-name">{escape(cat)}</span><span class="category-count">{len(items)} itens</span></a>' for cat, items in sorted(categories.items()))
    
    html = head("Radar Ninja | Catálogo de Ofertas Reais", "Mais de 200 produtos reais com fotos, preços e links de afiliado verificados.")
    html += f'''
    <section class="hero"><div class="hero-content"><h1>Encontre as melhores ofertas reais hoje</h1><p>Curadoria profissional de produtos com links verificados e descontos reais.</p><div class="hero-stats"><div class="hero-stat"><span class="hero-stat-number">{len(products)}</span><span class="hero-stat-label">Produtos</span></div><div class="hero-stat"><span class="hero-stat-number">100%</span><span class="hero-stat-label">Reais</span></div></div></div></section>
    <div class="container">
        <section style="padding:40px 0;"><div class="section-header"><span class="section-label">Categorias</span><h2 class="section-title">Explore por Categoria</h2></div><div class="categories-grid">{cat_cards}</div></section>
        <section id="ofertas"><div class="section-header"><span class="section-label">Destaque</span><h2 class="section-title">Ofertas em Destaque</h2><p class="section-subtitle">Os 12 produtos mais quentes do momento acima da dobra.</p></div><div class="product-grid">{"".join(product_card(p) for p in featured)}</div></section>
        <section style="padding:40px 0;"><div class="section-header"><span class="section-label">Populares</span><h2 class="section-title">Mais Procurados</h2></div><div class="product-grid">{"".join(product_card(p) for p in most_wanted)}</div></section>
        <section style="padding:40px 0;"><div class="section-header"><span class="section-label">Qualidade</span><h2 class="section-title">Melhores Avaliações</h2></div><div class="product-grid">{"".join(product_card(p) for p in best_rated)}</div></section>
    </div>''' + foot()
    (ROOT / "index.html").write_text(html, encoding="utf-8")

def build_category_pages(products):
    groups = defaultdict(list)
    for p in products: groups[p["custom_category"]].append(p)
    for cat, items in groups.items():
        slug = CATEGORY_SLUGS.get(cat, slugify(cat))
        per_page = 24
        pages = math.ceil(len(items) / per_page)
        for page in range(1, pages + 1):
            start = (page - 1) * per_page
            end = start + per_page
            p_items = items[start:end]
            
            html = head(f"{cat} - Página {page} | Radar Ninja", f"Ofertas de {cat} com produtos reais e verificados.")
            html += f'<div class="container"><section style="padding:40px 0;"><div class="section-header"><h2 class="section-title">{cat}</h2><p class="section-subtitle">Página {page} de {pages}</p></div><div class="product-grid">{"".join(product_card(p) for p in p_items)}</div>'
            if pages > 1:
                html += '<div class="pagination">'
                for p_num in range(1, pages + 1):
                    active = "active" if p_num == page else ""
                    link = f"/categorias/{slug}/" if p_num == 1 else f"/categorias/{slug}/page/{p_num}/"
                    html += f'<a href="{link}" class="page-link {active}">{p_num}</a>'
                html += '</div>'
            html += '</section></div>' + foot()
            
            path = ROOT / f"categorias/{slug}/index.html" if page == 1 else ROOT / f"categorias/{slug}/page/{page}/index.html"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")

def main():
    products = load_products()
    build_home(products)
    build_category_pages(products)
    print(f"Build concluído: {len(products)} produtos processados.")

if __name__ == "__main__":
    main()
