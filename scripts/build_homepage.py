import json
import os
import re
import unicodedata
from urllib.parse import urlparse

BASE_URL = "https://superninjas.github.io/"
DEFAULT_INPUT = "data/products/offers.json"
DEFAULT_TEMPLATE = "templates/homepage.html"
DEFAULT_OUTPUT = "index.html"
CONFIG_PATH = "data/ROBO4_CONFIG.json"

def normalize_text(value):
    value = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode("ascii")
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()

def normalize_slug(value):
    return normalize_text(value).replace(" ", "-")

def format_price(value):
    return f"{float(value or 0):.2f}"

def build_homepage(input_path, template_path, output_path):
    if not os.path.exists(template_path):
        print(f"❌ Template {template_path} não encontrado!")
        return

    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    products = []
    if os.path.exists(input_path):
        with open(input_path, "r", encoding="utf-8") as f:
            products = json.load(f)

    products_html = ""
    for p in products[:24]:
        name = p.get("title") or p.get("name") or "Oferta Ninja"
        price = p.get("price", 0)
        link = p.get("custom_affiliate_url") or p.get("permalink")
        img = p.get("thumbnail") or p.get("image")
        
        products_html += f"""
        <div class="product-card">
            <img src="{img}" alt="{name}" loading="lazy">
            <h3>{name[:60]}...</h3>
            <p class="price">R$ {format_price(price)}</p>
            <a href="{link}" class="btn-buy" target="_blank">Ver Oferta Ninja</a>
        </div>"""

    if not products_html:
        products_html = "<p>Buscando as melhores ofertas para você... Volte em instantes!</p>"

    content = template.replace("{{products}}", products_html)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Homepage gerada com {len(products)} produtos: {output_path}")

if __name__ == "__main__":
    build_homepage(DEFAULT_INPUT, DEFAULT_TEMPLATE, DEFAULT_OUTPUT)
