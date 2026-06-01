import json
import os
import re
from pathlib import Path

def format_price(value):
    return f"{float(value or 0):.2f}"

def build_homepage():
    ROOT = Path(__file__).resolve().parents[1]
    config_file = ROOT / "data/ROBO4_CONFIG.json"
    offers_file = ROOT / "data/products/offers.json"
    template_file = ROOT / "templates/homepage.html"
    output_file = ROOT / "index.html"

    if not config_file.exists():
        print("❌ Config não encontrada")
        return

    with open(config_file, "r", encoding="utf-8") as f:
        config = json.load(f)

    products = []
    if offers_file.exists():
        with open(offers_file, "r", encoding="utf-8") as f:
            products = json.load(f)

    products_html = ""
    for p in products[:30]:
        name = p.get("title") or p.get("name") or "Oferta Especial"
        price = p.get("price", 0)
        old_price = p.get("original_price") or price * 1.2
        discount = int(((old_price - price) / old_price) * 100) if old_price > price else 0
        link = p.get("custom_affiliate_url") or p.get("permalink")
        img = p.get("thumbnail") or p.get("image")
        
        products_html += f"""
        <div class="product-card">
            {f'<span class="badge">{discount}% OFF</span>' if discount > 0 else ''}
            <div class="product-img">
                <img src="{img}" alt="{name}" loading="lazy">
            </div>
            <div class="product-info">
                <h3>{name}</h3>
                <div class="price-box">
                    <span class="old-price">R$ {format_price(old_price)}</span>
                    <span class="price">R$ {format_price(price)}</span>
                </div>
                <a href="{link}" class="btn-buy" target="_blank">GARANTIR OFERTA</a>
            </div>
        </div>"""

    if not products_html:
        products_html = "<div style='grid-column: 1/-1; text-align: center; padding: 50px;'><h2>Carregando as melhores ofertas...</h2><p>O Robô Ninja está garimpando o Mercado Livre neste momento.</p></div>"

    if not template_file.exists():
        print("❌ Template não encontrado")
        return

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{products}}", products_html)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    
    print(f"✅ Site Premium gerado com sucesso!")

if __name__ == "__main__":
    build_homepage()
