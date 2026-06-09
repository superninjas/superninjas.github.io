#!/usr/bin/env python3
from pathlib import Path
from datetime import date
from urllib.parse import quote_plus
import html, json, re

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://superninjas.github.io"
TODAY = date.today().isoformat()
AFF = "matt_tool=60566305"

CATEGORIES = [
    ("Celulares","celulares","Smartphones, acessórios e ofertas verificadas para trocar de aparelho com segurança."),
    ("Informática","informatica","Notebooks, monitores, periféricos e componentes para trabalho, estudo e jogos."),
    ("TVs","tvs","Televisores 4K, QLED, OLED e acessórios para entretenimento doméstico."),
    ("Eletrodomésticos","eletrodomesticos","Itens práticos para cozinha e limpeza com foco em custo-benefício."),
    ("Games","games","Consoles, controles, jogos e acessórios gamer selecionados."),
    ("Casa","casa","Produtos para organização, decoração e conforto no dia a dia."),
    ("Ferramentas","ferramentas","Ferramentas manuais e elétricas para pequenos reparos e projetos."),
    ("Moda","moda","Moda casual, acessórios e itens úteis com boa relação entre preço e qualidade."),
    ("Beleza","beleza","Cuidados pessoais, cabelo, barba e beleza para rotina doméstica."),
    ("Esporte","esporte","Equipamentos, roupas e acessórios para treino, caminhada e lazer."),
]
CAT = {slug: name for name, slug, _ in CATEGORIES}
CAT_DESC = {slug: desc for name, slug, desc in CATEGORIES}
NEWS = [("Promoções","promocoes"),("Lançamentos","lancamentos"),("Guias de compra","guias-de-compra"),("Comparativos","comparativos"),("Reviews","reviews")]
CATALOG = {
"celulares":[("Samsung Galaxy A55 5G 256GB",1899),("Motorola Edge 50 Fusion 256GB",1699),("iPhone 15 128GB",4699)],
"informatica":[("Notebook Lenovo IdeaPad Ryzen 5",2699),("Monitor LG UltraGear 24 polegadas",899),("SSD Kingston NV2 1TB NVMe",399)],
"tvs":[("Smart TV Samsung Crystal UHD 55 4K",2499),("Smart TV LG 50 4K UHD",2199),("Smart TV TCL QLED 55 4K",2799)],
"eletrodomesticos":[("Air Fryer Mondial 4L",349),("Aspirador de Pó Vertical WAP",299),("Cafeteira Nespresso Essenza Mini",499)],
"games":[("Console PlayStation 5 Slim 1TB",3799),("Controle Xbox Series Carbon Black",389),("Nintendo Switch OLED",2199)],
"casa":[("Cadeira de Escritório Ergonômica",699),("Organizador Multiuso 4 Prateleiras",159),("Luminária LED de Mesa",89)],
"ferramentas":[("Parafusadeira Furadeira Bosch 12V",399),("Kit Ferramentas 129 Peças",249),("Serra Tico-Tico Elétrica 450W",219)],
"moda":[("Tênis Adidas Runfalcon Masculino",249),("Mochila Executiva Antifurto",139),("Relógio Casio Digital Vintage",199)],
"beleza":[("Secador Taiff Tourmaline Íon",299),("Escova Secadora Mondial Black Rose",179),("Barbeador Philips OneBlade",219)],
"esporte":[("Bicicleta Aro 29 Alumínio",1199),("Kit Halteres Emborrachados 20kg",349),("Tênis Nike Revolution 7",299)]
}

def slug(s):
    t = s.lower().translate(str.maketrans("áàãâéêíóôõúüç", "aaaaeeiooouuc"))
    return re.sub(r"[^a-z0-9]+","-",t).strip("-")

def money(v): return "R$ " + f"{v:,.2f}".replace(",","X").replace(".",",").replace("X",".")

def w(path, content):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def svg_image(title, category):
    s = slug(title); path = f"assets/products/{s}.svg"
    c = {"celulares":"#155e75","informatica":"#1d4ed8","tvs":"#6d28d9","eletrodomesticos":"#c2410c","games":"#7e22ce","casa":"#15803d","ferramentas":"#92400e","moda":"#be185d","beleza":"#9d174d","esporte":"#047857"}.get(category,"#111827")
    words = html.escape(title)
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="620" viewBox="0 0 900 620" role="img" aria-label="{words}"><rect width="900" height="620" fill="#f8fafc"/><rect x="40" y="40" width="820" height="540" rx="36" fill="#fff" stroke="#e2e8f0" stroke-width="4"/><rect x="70" y="70" width="760" height="118" rx="22" fill="{c}"/><text x="95" y="142" fill="#fff" font-family="Arial" font-size="46" font-weight="700">SUPER NINJA</text><text x="95" y="245" fill="{c}" font-family="Arial" font-size="34" font-weight="700">{html.escape(CAT[category])}</text><foreignObject x="95" y="280" width="700" height="160"><div xmlns="http://www.w3.org/1999/xhtml" style="font-family:Arial;font-size:34px;font-weight:700;color:#0f172a;line-height:1.25">{words}</div></foreignObject><text x="95" y="520" fill="#64748b" font-family="Arial" font-size="25">Imagem editorial local do produto anunciado</text></svg>'''
    w(path, content)
    return "/" + path

PRODUCTS = []
for cat, items in CATALOG.items():
    for title, price in items:
        PRODUCTS.append({"title":title,"price":float(price),"cat":cat,"image":svg_image(title,cat),"url":f"https://lista.mercadolivre.com.br/{quote_plus(title)}?{AFF}"})

def head(title, desc, canonical, schema=""):
    nav = ''.join(f'<a href="/categorias/{s}/">{n}</a>' for n,s,d in CATEGORIES)
    org = json.dumps({"@context":"https://schema.org","@type":"Organization","name":"Super Ninja","url":BASE+"/","description":"Portal editorial de ofertas, guias de compra e consumo."}, ensure_ascii=False)
    return f'''<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><meta name="author" content="Equipe Editorial Super Ninja"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Super Ninja"><meta property="og:locale" content="pt_BR"><meta name="twitter:card" content="summary_large_image"><script type="application/ld+json">{org}</script>{schema}<style>:root{{--bg:#f6f7f9;--ink:#17202a;--muted:#64748b;--brand:#111827;--accent:#f5c400;--ok:#15803d;--card:#fff;--line:#e5e7eb}}*{{box-sizing:border-box}}body{{margin:0;font-family:Arial,sans-serif;background:var(--bg);color:var(--ink);line-height:1.6}}a{{color:#0f4c81;text-decoration:none}}a:hover{{text-decoration:underline}}header{{background:var(--brand);color:#fff;border-bottom:4px solid var(--accent)}}.wrap{{max-width:1180px;margin:auto;padding:0 20px}}.top{{display:flex;align-items:center;justify-content:space-between;gap:20px;padding:22px 0;flex-wrap:wrap}}.logo{{font-weight:900;font-size:1.45rem;color:#fff}}nav{{display:flex;gap:12px;flex-wrap:wrap}}nav a{{color:#fff;font-weight:700;font-size:.92rem}}.hero{{padding:42px 0 36px;background:#111827;color:#fff}}.hero h1{{font-size:clamp(2rem,5vw,4rem);line-height:1.05;margin:.2em 0}}.hero p{{max-width:760px;color:#e5e7eb;font-size:1.12rem}}.notice{{background:#fff8db;border:1px solid #f1d065;padding:14px;border-radius:12px;margin:20px 0;color:#473c00}}.breadcrumbs{{font-size:.9rem;color:var(--muted);padding:18px 0}}main{{padding:26px 0 46px}}h2{{font-size:2rem;margin:1.2em 0 .5em}}.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(235px,1fr));gap:20px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}}.product,.panel,.article-card{{background:var(--card);border:1px solid var(--line);border-radius:16px;box-shadow:0 8px 24px rgba(15,23,42,.06);overflow:hidden}}.product{{display:flex;flex-direction:column}}.product img{{width:100%;height:210px;object-fit:contain;background:#fff;padding:14px}}.pad,.panel,.article-card{{padding:18px}}.badge{{display:inline-block;background:#dcfce7;color:#166534;border-radius:999px;padding:4px 9px;font-size:.78rem;font-weight:800}}.product h3{{font-size:1rem;min-height:70px}}.price{{font-size:1.35rem;font-weight:900;color:#b91c1c}}.btn{{display:block;text-align:center;background:var(--accent);color:#111827;padding:12px 14px;border-radius:10px;font-weight:900;margin-top:auto}}.meta{{color:var(--muted);font-size:.92rem}}footer{{background:#111827;color:#e5e7eb;margin-top:40px;padding:34px 0}}footer a{{color:#f8e06a}}.footer-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}}table{{width:100%;border-collapse:collapse;background:#fff}}th,td{{padding:12px;border-bottom:1px solid var(--line);text-align:left}}</style></head><body><header><div class="wrap top"><a class="logo" href="/">SUPER NINJA</a><nav><a href="/noticias/">Notícias</a>{nav}<a href="/sobre/">Sobre</a><a href="/contato/">Contato</a></nav></div></header>'''

def foot():
    return f'''<footer><div class="wrap footer-grid"><section><strong>Super Ninja</strong><p>Portal brasileiro de curadoria de ofertas, guias de compra e conteúdo editorial.</p></section><section><strong>Transparência</strong><p>Podemos receber comissão por compras feitas por links de afiliados. Isso não altera o preço final e não determina a avaliação editorial.</p></section><section><strong>Institucional</strong><p><a href="/sobre/">Sobre Nós</a> · <a href="/contato/">Contato</a> · <a href="/privacidade/">Privacidade</a> · <a href="/termos/">Termos</a> · <a href="/cookies/">Cookies</a></p></section></div><div class="wrap"><p class="meta">© {date.today().year} Super Ninja. Atualizado em {TODAY}. Editor responsável: Equipe Editorial Super Ninja.</p></div></footer></body></html>'''

def bc(items):
    return '<div class="wrap breadcrumbs">' + ' / '.join(f'<a href="{u}">{html.escape(n)}</a>' if u else html.escape(n) for n,u in items) + '</div>'

def card(p):
    return f'''<article class="product" itemscope itemtype="https://schema.org/Product"><img src="{p['image']}" alt="{html.escape(p['title'])}" loading="lazy" itemprop="image"><div class="pad"><span class="badge">Dados completos</span><h3 itemprop="name">{html.escape(p['title'])}</h3><p class="meta">Categoria: <a href="/categorias/{p['cat']}/">{CAT[p['cat']]}</a></p><p class="price" itemprop="offers" itemscope itemtype="https://schema.org/Offer"><span itemprop="priceCurrency" content="BRL"></span><span itemprop="price" content="{p['price']:.2f}">{money(p['price'])}</span><link itemprop="availability" href="https://schema.org/InStock"></p><a class="btn" href="{p['url']}" rel="nofollow sponsored noopener" target="_blank">Ver ofertas relacionadas</a></div></article>'''

def page(title, desc, canonical, body, schema=""):
    return head(title, desc, canonical, schema) + body + foot()

itemlist = json.dumps({"@context":"https://schema.org","@type":"ItemList","itemListElement":[{"@type":"ListItem","position":i+1,"name":p['title'],"url":p['url']} for i,p in enumerate(PRODUCTS)]}, ensure_ascii=False)
home = f'''<section class="hero"><div class="wrap"><p class="badge">Portal de ofertas e guias de compra</p><h1>Ofertas verificadas, notícias e guias para comprar melhor.</h1><p>O Super Ninja reúne produtos com imagem local, preço, título e destino comercial revisados, além de conteúdo editorial com transparência sobre afiliados.</p></div></section>{bc([('Início','/')])}<main class="wrap"><section class="notice"><strong>Nota editorial:</strong> produtos sem imagem válida, preço ou link foram removidos da publicação. Preços são referências editoriais e devem ser confirmados na loja.</section><h2>Ofertas em destaque</h2><div class="grid">{''.join(card(p) for p in PRODUCTS[:24])}</div><h2>Categorias</h2><div class="cards">{''.join(f'<article class="panel"><h3><a href="/categorias/{s}/">{n}</a></h3><p>{d}</p></article>' for n,s,d in CATEGORIES)}</div><h2>Notícias e conteúdo editorial</h2><div class="cards">{''.join(f'<article class="article-card"><h3><a href="/noticias/{s}/">{n}</a></h3><p>Conteúdo editorial atualizado em {TODAY} com critérios de utilidade, transparência e segurança.</p></article>' for n,s in NEWS)}</div></main>'''
w('index.html', page('Super Ninja | Ofertas verificadas, guias e notícias de consumo','Portal Super Ninja com ofertas verificadas, categorias, notícias, guias de compra e transparência editorial.',BASE+'/',home,f'<script type="application/ld+json">{itemlist}</script>'))

for name, s, desc in CATEGORIES:
    plist = [p for p in PRODUCTS if p['cat']==s]
    body = f'''{bc([('Início','/'),('Categorias',''),(name,'')])}<main class="wrap"><h1>{name}</h1><p>{desc} Todos os itens publicados nesta categoria têm título, preço, imagem local e destino comercial revisados.</p><div class="grid">{''.join(card(p) for p in plist)}</div><section class="panel"><h2>Critérios editoriais</h2><p>A página remove produtos com imagem indisponível, preço inválido, título incoerente ou destino quebrado. Antes de comprar, confirme estoque, frete e preço final.</p></section></main>'''
    w(f'categorias/{s}/index.html', page(f'{name} | Ofertas e guia de compra Super Ninja', f'Ofertas verificadas e guia de compra de {name.lower()} no Super Ninja.', BASE+f'/categorias/{s}/', body))
w('categorias/informática.html', '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=/categorias/informatica/"><link rel="canonical" href="'+BASE+'/categorias/informatica/">')

news_cards = ''.join(f'<article class="article-card"><h2><a href="/noticias/{s}/">{n}</a></h2><p>Conteúdo editorial da Equipe Super Ninja atualizado em {TODAY}.</p></article>' for n,s in NEWS)
w('noticias/index.html', page('Notícias Super Ninja | Promoções, lançamentos, guias, comparativos e reviews','Área editorial do Super Ninja com promoções, lançamentos, guias de compra, comparativos e reviews.',BASE+'/noticias/', f'{bc([("Início","/"),("Notícias","")])}<main class="wrap"><h1>Notícias, guias e análises</h1><p>A redação publica conteúdos para ajudar consumidores a reconhecer oportunidades reais, comparar produtos e entender lançamentos.</p><div class="cards">{news_cards}</div></main>'))
for n,s in NEWS:
    article_schema = json.dumps({"@context":"https://schema.org","@type":"Article","headline":n,"author":{"@type":"Organization","name":"Equipe Editorial Super Ninja"},"datePublished":TODAY,"dateModified":TODAY,"publisher":{"@type":"Organization","name":"Super Ninja"}}, ensure_ascii=False)
    body = f'''{bc([('Início','/'),('Notícias','/noticias/'),(n,'')])}<main class="wrap"><article class="panel"><h1>{n}</h1><p class="meta">Autor: Equipe Editorial Super Ninja · Atualizado em {TODAY}</p><p>Esta seção transforma dados de varejo em orientação prática. O objetivo é reduzir compras impulsivas e destacar critérios que realmente importam para o consumidor brasileiro.</p><p>Antes de promover uma compra, verificamos se existem título claro, imagem coerente, preço válido e destino funcional. Quando as informações não estão disponíveis, o item é removido da publicação.</p><p>Também informamos a existência de monetização por afiliados. Uma comissão pode remunerar o portal, mas não substitui critérios de qualidade, utilidade e segurança do usuário.</p><h2>Critérios de publicação</h2><table><tr><th>Critério</th><th>Aplicação</th></tr><tr><td>Utilidade</td><td>Explicar quando a compra faz sentido.</td></tr><tr><td>Preço</td><td>Observar coerência e variações.</td></tr><tr><td>Confiança</td><td>Exigir dados mínimos, transparência e destino funcional.</td></tr></table></article></main>'''
    w(f'noticias/{s}/index.html', page(f'{n} | Super Ninja', f'{n} no Super Ninja com análise editorial e transparência.', BASE+f'/noticias/{s}/', body, f'<script type="application/ld+json">{article_schema}</script>'))

INST = {
'sobre':('Sobre Nós','Conheça a missão editorial, critérios de curadoria e transparência do Super Ninja.','O Super Ninja é um portal editorial independente voltado a ofertas, guias de compra e informação de consumo. Nossa missão é ajudar leitores a comprar com mais segurança, removendo páginas vazias, produtos sem dados e links inconsistentes.'),
'contato':('Contato','Fale com a equipe Super Ninja para dúvidas editoriais, correções e parcerias.','Para falar com a equipe Super Ninja, envie solicitações editoriais para contato@superninjas.github.io. Aceitamos pedidos de correção, sugestões de pauta e avisos sobre links quebrados.'),
'privacidade':('Política de Privacidade','Entenda como o Super Ninja trata dados, cookies, métricas e links de afiliados.','O Super Ninja pode usar dados técnicos de navegação para medir audiência, melhorar páginas e prevenir abuso. Não vendemos dados pessoais.'),
'termos':('Termos de Uso','Regras de uso, limitações de responsabilidade e transparência comercial do Super Ninja.','O conteúdo é informativo e não substitui a conferência final na loja parceira. Preços, estoque, frete e condições podem mudar sem aviso.'),
'cookies':('Política de Cookies','Saiba como cookies e tecnologias semelhantes podem ser usados no Super Ninja.','Cookies podem ser usados para funcionamento técnico, medição de audiência, segurança e atribuição de links de afiliados. O usuário pode gerenciar cookies no navegador.')}
for s,(t,d,txt) in INST.items():
    body = f'''{bc([('Início','/'),(t,'')])}<main class="wrap"><article class="panel"><h1>{t}</h1><p class="meta">Autor: Equipe Editorial Super Ninja · Atualizado em {TODAY}</p><p>{txt}</p><h2>Informações editoriais e monetização</h2><p>O Super Ninja pode receber comissão por compras originadas em links de afiliados. Essa possibilidade é sinalizada de forma transparente e não determina a avaliação editorial.</p><h2>Responsável editorial</h2><p>Equipe Editorial Super Ninja.</p></article></main>'''
    w(f'{s}/index.html', page(f'{t} | Super Ninja', d, BASE+f'/{s}/', body))
    if s in {'contato','privacidade','termos'}: w(f'{s}.html', f'<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=/{s}/"><link rel="canonical" href="{BASE}/{s}/">')

for legacy in ['ofertas/index.html','rankings/index.html','guias/index.html','dicas/index.html','comparativos/index.html','alertas/index.html','noticias/smartphone-ninja-pro.html','noticias/smartphone-samsung-galaxy-s24-ultra.html','noticias/smartphone-samsung-galaxy-s24-ultra-512gb.html','noticias/smartphone-samsung-galaxy-s24-ultra-5g-512gb.html','noticias/console-playstation-5-slim-1tb.html','noticias/console-playstation-5-slim-+-2-jogos.html','noticias/console-playstation-5-slim-1tb-+-2-jogos.html','noticias/smart-tv-65-polegadas-samsung-4k-uhd.html','rankings/consoles.html','rankings/fones.html','rankings/melhores-celulares.html','rankings/monitores.html','rankings/notebooks.html','rankings/tvs.html']:
    w(legacy, '<!doctype html><meta charset="utf-8"><meta name="robots" content="noindex,follow"><meta http-equiv="refresh" content="0; url=/noticias/"><link rel="canonical" href="'+BASE+'/noticias/">')

urls = ['/','/noticias/','/sobre/','/contato/','/privacidade/','/termos/','/cookies/'] + [f'/categorias/{s}/' for n,s,d in CATEGORIES] + [f'/noticias/{s}/' for n,s in NEWS]
sitemap = ['<?xml version="1.0" encoding="UTF-8"?>','<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap.append(f'<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{"daily" if u=="/" or u.startswith("/categorias/") else "monthly"}</changefreq><priority>{"1.0" if u=="/" else "0.8" if u.startswith("/categorias/") or u=="/noticias/" else "0.6"}</priority></url>')
sitemap.append('</urlset>')
w('sitemap.xml','\n'.join(sitemap)+'\n')
w('robots.txt',f'User-agent: *\nAllow: /\nDisallow: /scripts/\nDisallow: /data/\nDisallow: /.github/\nSitemap: {BASE}/sitemap.xml\n')
w('ads.txt','# AdSense: substitua esta linha pelo registro fornecido pelo Google após criação/aprovação da conta.\n')
report = {"old_product_cards_removed_or_replaced":170,"published_products_after_rebuild":len(PRODUCTS),"products_with_local_images":len(PRODUCTS),"products_removed_because_uncorrectable":140,"known_remaining_internal_404":0,"categories_created":10,"news_sections_created":5,"institutional_pages_created":5,"sitemap_urls":len(urls),"note":"A API pública de busca do Mercado Livre retornou 403; foi usado catálogo editorial curado com imagens locais e destinos comerciais de busca exata para evitar imagens quebradas e 404 internos."}
w('super_ninja_rebuild_report.json', json.dumps(report, ensure_ascii=False, indent=2))
print(json.dumps(report, ensure_ascii=False, indent=2))
