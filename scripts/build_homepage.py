import json
import os
from pathlib import Path

def build():
    ROOT = Path(__file__).resolve().parents[1]
    template_file = ROOT / "templates/homepage.html"
    offers_file = ROOT / "data/products/offers.json"
    output_file = ROOT / "index.html"

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    with open(offers_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    products_html = ""
    for p in products:
        title = p.get("title", "Produto")
        price = p.get("price", 0)
        original = p.get("original_price", 0)
        image = p.get("thumbnail", "").replace("-O.webp", "-O.jpg") # Voltar para JPG que é mais seguro
        link = p.get("permalink", "#")
        discount = p.get("custom_discount_pct", 0)

        badge_discount = f'<div class="badge-discount">-{discount}%</div>' if discount > 5 else ""
        
        products_html += f"""
        <div class="card">
            <span class="badge-verified">✓ OFERTA VERIFICADA 2026</span>
            {badge_discount}
            <div class="card-img-wrap">
                <img src="{image}" alt="{title}" onerror="this.src='https://http2.mlstatic.com/D_NQ_NP_634347-MLA46114829749_052021-O.jpg'">
            </div>
            <div class="card-info">
                <h3 class="card-title">{title}</h3>
                <div class="price-wrap">
                    <span class="old-price">De R$ {original:,.2f}</span>
                    <div class="price">R$ {price:,.2f}</div>
                </div>
                <a href="{link}" class="btn" target="_blank">🛒 Ver Oferta</a>
            </div>
        </div>
        """

    final_html = template.replace("{{products}}", products_html)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)

if __name__ == "__main__":
    build()
