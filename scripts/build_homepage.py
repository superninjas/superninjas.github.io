import json
import os
from pathlib import Path

def build_homepage():
    ROOT = Path(__file__).resolve().parents[1]
    offers_file = ROOT / "data/products/offers.json"
    template_file = ROOT / "templates/homepage.html"
    output_file = ROOT / "index.html"

    products = []
    if offers_file.exists():
        with open(offers_file, "r", encoding="utf-8") as f:
            products = json.load(f)

    products_html = ""
    for p in products[:32]:
        name = p.get("title") or p.get("name") or "Oferta Ninja"
        price = p.get("price", 0)
        # Garantir link de afiliado com o seu matt_tool
        link = p.get("permalink", "https://mercadolivre.com.br")
        if "matt_tool" not in link:
            link += "?matt_tool=vendas0nline"
        
        img = p.get("thumbnail") or p.get("image")
        
        products_html += f"""
        <div class="card">
            <div class="card-image">
                <img src="{img}" alt="{name}" loading="lazy">
            </div>
            <div class="card-content">
                <h3 class="card-title">{name}</h3>
                <span class="price-current">R$ {float(price):.2f}</span>
                <a href="{link}" class="btn-cta" target="_blank">VER OFERTA NINJA</a>
            </div>
        </div>"""

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    final_html = template.replace("{{products}}", products_html)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(final_html)
    print("✅ Homepage com links de afiliado gerada!")

if __name__ == "__main__":
    build_homepage()
