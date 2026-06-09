import json
import re
from collections import defaultdict
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_PATH = ROOT / "data/products/offers.json"

SITE_URL = "https://superninjas.github.io"
AFFILIATE_NOTE = (
    "O Radar Ninja participa do Programa de Afiliados do Mercado Livre. "
    "Podemos receber comissão quando você compra por nossos links, sem custo adicional para você."
)

CATEGORY_SLUGS = {
    "Celulares": "celulares",
    "TV e Vídeo": "tv-e-video",
    "Casa & Eletro": "casa-e-eletro",
    "Ferramentas": "ferramentas",
    "Beleza & Saúde": "beleza-e-saude",
    "Tecnologia": "tecnologia",
    "Informática": "informatica",
    "Games": "games",
    "Colecionáveis": "colecionaveis",
    "Ofertas Gerais": "ofertas-gerais",
}


def brl(value):
    if value in (None, ""):
        return ""
    return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def slugify(text):
    text = text.lower()
    repl = {
        "á": "a", "à": "a", "ã": "a", "â": "a", "é": "e", "ê": "e", "í": "i",
        "ó": "o", "ô": "o", "õ": "o", "ú": "u", "ç": "c", "&": "e"
    }
    for a, b in repl.items():
        text = text.replace(a, b)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "ofertas"


def load_products():
    products = json.loads(PRODUCTS_PATH.read_text(encoding="utf-8"))
    for p in products:
        cat = p.get("custom_category") or "Ofertas Gerais"
        p["custom_category"] = cat
        p["custom_category_slug"] = CATEGORY_SLUGS.get(cat, slugify(cat))
        if not p.get("custom_discount_pct") and p.get("original_price") and p.get("price"):
            try:
                original = float(p["original_price"])
                price = float(p["price"])
                p["custom_discount_pct"] = int(round(((original - price) / original) * 100)) if original > price else 0
            except Exception:
                p["custom_discount_pct"] = 0
    return products


def product_card(p, secondary=True):
    title = escape(p.get("title", "Produto verificado"))
    img = escape(p.get("thumbnail") or p.get("image") or "")
    link = escape(p.get("permalink") or "#")
    cat = escape(p.get("custom_category") or "Ofertas")
    discount = int(p.get("custom_discount_pct") or 0)
    original = p.get("original_price")
    price = p.get("price")
    savings = ""
    if original and price and float(original) > float(price):
        savings = f'<div class="savings">Economia estimada: {brl(float(original) - float(price))}</div>'
    badge = f'<span class="badge">{discount}% OFF</span>' if discount >= 5 else '<span class="badge badge-green">Oferta verificada</span>'
    old_price = f'<span class="old-price">De {brl(original)}</span>' if original and float(original) > float(price) else ''
    installments = f'<div class="price-installments">Preço consultado em referência pública; pode variar no varejista.</div>'
    analysis_link = f'/ofertas/{slugify(p.get("title", "produto"))}/'
    secondary_html = f'<a href="{analysis_link}" class="btn btn-outline-card">Ver análise</a>' if secondary else ""
    return f'''
    <article class="card" itemscope itemtype="https://schema.org/Product">
        {badge}
        <div class="card-img-wrap"><img src="{img}" alt="{title}" loading="lazy" itemprop="image"></div>
        <div class="card-info">
            <span class="category-tag">{cat}</span>
            <h3 class="card-title" itemprop="name">{title}</h3>
            {savings}
            <div class="price-wrap" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                {old_price}
                <div class="price" itemprop="price" content="{float(price):.2f}">{brl(price)}</div>
                <meta itemprop="priceCurrency" content="BRL">
                <meta itemprop="availability" content="https://schema.org/InStock">
                {installments}
            </div>
            <div class="product-actions-local">
                <a href="{link}" class="btn" target="_blank" rel="nofollow sponsored noopener" itemprop="url">Ver Oferta Ninja</a>
                {secondary_html}
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
<link rel="canonical" href="{SITE_URL}{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{SITE_URL}{canonical}">
<meta name="google-adsense-account" content="ca-pub-4896859041377751">
<meta name="google-site-verification" content="googlee894f61326f42819">
<link rel="stylesheet" href="/assets/css/style.css">
<style>
.commercial-strip {{ background:#111827; color:#fff; padding:10px 20px; text-align:center; font-size:13px; }}
.hero-actions {{ display:flex; justify-content:center; gap:14px; flex-wrap:wrap; margin-top:24px; }}
.hero-actions .btn {{ display:inline-block; max-width:260px; background:#fff; color:var(--ninja-purple); }}
.section-tight {{ padding:54px 20px; }}
.section-soft {{ background:#fff; }}
.product-actions-local {{ display:grid; gap:10px; margin-top:auto; }}
.btn-outline-card {{ background:#fff; color:var(--ninja-purple); border:1px solid var(--ninja-purple-light); box-shadow:none; }}
.comparison-table {{ width:100%; border-collapse:collapse; background:#fff; border-radius:16px; overflow:hidden; box-shadow:var(--shadow-md); }}
.comparison-table th,.comparison-table td {{ padding:14px; border-bottom:1px solid var(--ninja-gray-light); text-align:left; font-size:14px; }}
.comparison-table th {{ background:var(--ninja-purple); color:#fff; }}
.notice-box {{ max-width:var(--max-width); margin:24px auto; background:#fff8e7; border-left:4px solid var(--ninja-orange); padding:18px 20px; border-radius:12px; color:var(--ninja-dark); }}
.mini-rank {{ max-width:var(--max-width); margin:0 auto; display:grid; gap:14px; padding:0 20px; }}
.rank-row {{ display:grid; grid-template-columns:52px 1fr auto; gap:16px; align-items:center; background:#fff; padding:16px; border-radius:14px; box-shadow:var(--shadow-sm); }}
.rank-pos {{ width:42px; height:42px; display:grid; place-items:center; background:var(--ninja-purple); color:#fff; border-radius:50%; font-weight:900; }}
@media (max-width:700px) {{ .rank-row {{ grid-template-columns:42px 1fr; }} .rank-row .btn {{ grid-column:1/-1; }} .nav {{ display:none; }} }}
</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebSite","name":"Radar Ninja","url":"{SITE_URL}/","description":"Radar de ofertas reais com links afiliados e curadoria de produtos."}}</script>
</head>
<body>
<div class="commercial-strip">Radar Ninja voltou ao modo comercial: produtos reais, links de afiliado, fotos verificadas e CTAs de compra.</div>
<header class="header"><div class="header-inner"><a class="logo" href="/"><span class="logo-icon">🥷</span><span class="logo-text"><span class="logo-title">Radar Ninja</span><span class="logo-subtitle">Ofertas verificadas</span></span></a><nav class="nav" aria-label="Navegação principal"><a href="/ofertas/">Ofertas</a><a href="/categorias/celulares/">Categorias</a><a href="/rankings/">Rankings</a><a href="/comparativos/">Comparativos</a><a href="/guias/">Guias</a><a class="nav-cta" href="#ofertas">Comprar melhor</a></nav></div></header>'''


def foot():
    return f'''<div class="notice-box"><strong>Transparência comercial:</strong> {AFFILIATE_NOTE} Os preços podem mudar sem aviso e devem ser confirmados na página final do vendedor.</div>
<footer class="footer"><div class="footer-grid"><div class="footer-brand"><h3>Radar Ninja</h3><p>Curadoria independente de ofertas, rankings e comparativos com foco em economia real.</p></div><div><h4>Comprar</h4><ul><li><a href="/ofertas/">Ofertas</a></li><li><a href="/rankings/">Rankings</a></li><li><a href="/comparativos/">Comparativos</a></li></ul></div><div><h4>Categorias</h4><ul><li><a href="/categorias/celulares/">Celulares</a></li><li><a href="/categorias/casa-e-eletro/">Casa & Eletro</a></li><li><a href="/categorias/beleza-e-saude/">Beleza & Saúde</a></li></ul></div><div><h4>Institucional</h4><ul><li><a href="/sobre/">Sobre</a></li><li><a href="/privacidade/">Privacidade</a></li><li><a href="/contato/">Contato</a></li></ul></div></div><div class="footer-bottom"><p>© 2026 Radar Ninja. Algumas ofertas podem gerar comissão de afiliado.</p></div></footer>
</body></html>'''


def section_header(label, title, subtitle):
    return f'''<div class="section-header"><span class="section-label">{label}</span><h2 class="section-title">{title}</h2><p class="section-subtitle">{subtitle}</p></div>'''


def grid(products):
    return '<div class="product-grid">' + "\n".join(product_card(p) for p in products) + '</div>'


def write(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")


def build_home(products):
    featured = sorted(products, key=lambda p: p.get("custom_discount_pct") or 0, reverse=True)[:12]
    week = products[6:18]
    popular = [p for p in products if p.get("custom_category") in {"Celulares", "Casa & Eletro", "Beleza & Saúde", "Ferramentas"}][:8]
    categories = defaultdict(list)
    for p in products:
        categories[p["custom_category"]].append(p)
    cat_cards = "".join(f'<a class="category-card" href="/categorias/{CATEGORY_SLUGS.get(cat, slugify(cat))}/"><span class="category-icon">{len(items)}</span><span class="category-name">{escape(cat)}</span><span class="category-count">produtos reais verificados</span></a>' for cat, items in sorted(categories.items()))
    html = head("Radar Ninja | Ofertas reais, rankings e produtos com link afiliado", "Produtos reais em destaque, ofertas da semana, rankings e comparativos com CTAs de compra e links afiliados verificados.")
    html += f'''<section class="hero"><div class="hero-content"><div class="hero-badge">Curadoria comercial ativa</div><h1>Ofertas reais para comprar melhor hoje</h1><p>O Radar Ninja compara produtos verificáveis, fotos funcionando e links afiliados para ajudar você a decidir com rapidez e segurança.</p><div class="hero-stats"><div class="hero-stat"><span class="hero-stat-number">{len(products)}</span><span class="hero-stat-label">Produtos reais</span></div><div class="hero-stat"><span class="hero-stat-number">{len(products)}</span><span class="hero-stat-label">Links afiliados</span></div><div class="hero-stat"><span class="hero-stat-number">100%</span><span class="hero-stat-label">Com foto e CTA</span></div></div><div class="hero-actions"><a class="btn" href="#ofertas">Ver ofertas</a><a class="btn" href="/rankings/">Ver rankings</a></div></div></section>
<section class="section-tight section-soft"><div class="container">{section_header('Categorias de compra', 'Escolha uma categoria com produtos reais', 'Nada de páginas vazias: cada categoria abaixo contém ofertas com foto, preço e CTA de compra.')}<div class="categories-grid">{cat_cards}</div></div></section>
<section id="ofertas" class="section-tight">{section_header('Produtos em destaque', 'Ofertas Ninja do Momento', 'Seleção inicial com produtos reais, links Mercado Livre e imagens verificáveis.')} {grid(featured)}</section>
<section class="section-tight section-soft">{section_header('Ofertas da semana', 'Boas oportunidades para acompanhar', 'Curadoria menor e mais confiável, priorizando qualidade em vez de volume falso.')} {grid(week[:8])}</section>
<section class="section-tight">{section_header('Mais procurados', 'Produtos populares com intenção de compra', 'Itens de categorias com alta demanda: celulares, casa, saúde, ferramentas e tecnologia.')} {grid(popular)}</section>
<section class="section-tight section-soft"><div class="container">{section_header('Rankings e comparativos', 'Decisão de compra com produto e CTA', 'O conteúdo editorial volta a servir à compra, não a substituir a oferta.')}</div><div class="mini-rank">'''
    for i, p in enumerate(featured[:5], 1):
        html += f'<div class="rank-row"><div class="rank-pos">{i}</div><div><strong>{escape(p["title"])}</strong><br><span>{escape(p["custom_category"])} · {brl(p["price"])} · {p.get("custom_discount_pct", 0)}% OFF</span></div><a class="btn" href="{escape(p["permalink"])}" target="_blank" rel="nofollow sponsored noopener">Ver oferta</a></div>'
    html += '</div></section>' + foot()
    write(ROOT / "index.html", html)


def build_offers(products):
    html = head("Ofertas Radar Ninja | Produtos reais com CTA de compra", "Lista de ofertas reais com fotos, preços, descontos e links afiliados verificados.", "/ofertas/")
    html += f'<section class="hero"><div class="hero-content"><div class="hero-badge">Ofertas verificadas</div><h1>Ofertas do Radar Ninja</h1><p>Todos os cards abaixo têm foto, preço, link afiliado e CTA de compra.</p></div></section><section class="section-tight">{section_header("Lista comercial", "Todos os produtos reais", "Base menor e verificável, sem produtos fictícios.")} {grid(products)}</section>' + foot()
    write(ROOT / "ofertas/index.html", html)


def build_categories(products):
    groups = defaultdict(list)
    for p in products:
        groups[p["custom_category"]].append(p)
    for cat, items in groups.items():
        slug = CATEGORY_SLUGS.get(cat, slugify(cat))
        html = head(f"{cat} em oferta | Radar Ninja", f"Produtos reais de {cat} com foto, preço, CTA de compra e link afiliado.", f"/categorias/{slug}/")
        html += f'<section class="hero"><div class="hero-content"><div class="hero-badge">Categoria comercial</div><h1>{escape(cat)} com produtos reais</h1><p>Ofertas selecionadas com imagens funcionando, preços e CTAs de compra.</p></div></section><section class="section-tight">{section_header("Produtos da categoria", f"Ofertas de {escape(cat)}", "Cards comerciais com verificação visual e link de compra.")} {grid(items)}</section>' + foot()
        write(ROOT / f"categorias/{slug}/index.html", html)


def build_rankings(products):
    top = sorted(products, key=lambda p: p.get("custom_discount_pct") or 0, reverse=True)[:10]
    html = head("Rankings Radar Ninja | Top ofertas com produtos reais", "Rankings de produtos reais com preços, fotos e CTAs afiliados.", "/rankings/")
    html += f'<section class="hero"><div class="hero-content"><div class="hero-badge">Ranking comercial</div><h1>Top 10 ofertas verificadas</h1><p>Ranking baseado em desconto informado nas referências públicas e presença de foto/link funcionando.</p></div></section><section class="section-tight"><div class="mini-rank">'
    for i, p in enumerate(top, 1):
        html += f'<div class="rank-row"><div class="rank-pos">{i}</div><div><strong>{escape(p["title"])}</strong><br><span>{escape(p["custom_category"])} · De {brl(p.get("original_price"))} por {brl(p["price"])} · {p.get("custom_discount_pct",0)}% OFF</span></div><a class="btn" href="{escape(p["permalink"])}" target="_blank" rel="nofollow sponsored noopener">Ver oferta</a></div>'
    html += '</div></section>' + grid(top[:6]) + foot()
    write(ROOT / "rankings/index.html", html)


def build_comparisons(products):
    selected = products[:8]
    rows = "".join(f'<tr><td>{escape(p["title"][:70])}</td><td>{escape(p["custom_category"])}</td><td>{brl(p.get("original_price"))}</td><td><strong>{brl(p["price"])}</strong></td><td>{p.get("custom_discount_pct",0)}%</td><td><a href="{escape(p["permalink"])}" target="_blank" rel="nofollow sponsored noopener">Ver oferta</a></td></tr>' for p in selected)
    html = head("Comparativos Radar Ninja | Produtos reais lado a lado", "Comparativos com produtos reais, preço, desconto, categoria e CTA de compra.", "/comparativos/")
    html += f'<section class="hero"><div class="hero-content"><div class="hero-badge">Comparativo comercial</div><h1>Comparar antes de comprar</h1><p>Produtos lado a lado com preço, desconto e link afiliado.</p></div></section><section class="section-tight"><div class="container">{section_header("Tabela de decisão", "Comparativo rápido de ofertas", "Escolha com base em preço, categoria e desconto.")}<table class="comparison-table"><thead><tr><th>Produto</th><th>Categoria</th><th>Preço anterior</th><th>Preço atual</th><th>Desconto</th><th>CTA</th></tr></thead><tbody>{rows}</tbody></table></div></section>{grid(selected[:4])}' + foot()
    write(ROOT / "comparativos/index.html", html)


def build_product_pages(products):
    for p in products:
        slug = slugify(p["title"])
        html = head(f"{p['title']} | Oferta Radar Ninja", f"Análise curta, preço e link de compra para {p['title']}.", f"/ofertas/{slug}/")
        html += f'<section class="hero"><div class="hero-content"><div class="hero-badge">Produto verificado</div><h1>{escape(p["title"])}</h1><p>{escape(p["custom_category"])} · preço atual {brl(p["price"])} · link afiliado disponível.</p></div></section><section class="section-tight">{grid([p])}<div class="container"><h2>Resumo Ninja</h2><p>Este produto foi publicado porque possui foto funcionando, preço identificado e link de compra no Mercado Livre com parâmetro de afiliado. Antes de finalizar a compra, confirme o preço, o frete e a reputação do vendedor na página do varejista.</p></div></section>' + foot()
        write(ROOT / f"ofertas/{slug}/index.html", html)


def build_sitemap(products):
    urls = ["/", "/ofertas/", "/rankings/", "/comparativos/"]
    cats = sorted({CATEGORY_SLUGS.get(p["custom_category"], slugify(p["custom_category"])) for p in products})
    urls += [f"/categorias/{c}/" for c in cats]
    urls += [f"/ofertas/{slugify(p['title'])}/" for p in products]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        xml += f"  <url><loc>{SITE_URL}{u}</loc></url>\n"
    xml += "</urlset>\n"
    write(ROOT / "sitemap.xml", xml)


def main():
    products = load_products()
    build_home(products)
    build_offers(products)
    build_categories(products)
    build_rankings(products)
    build_comparisons(products)
    build_product_pages(products)
    build_sitemap(products)
    print(f"Radar Ninja comercial gerado com {len(products)} produtos reais, {len(products)} CTAs e {len(products)} links afiliados principais.")


if __name__ == "__main__":
    main()
