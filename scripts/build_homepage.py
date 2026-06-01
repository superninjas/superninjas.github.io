import json
import os
from pathlib import Path

def build():
    ROOT = Path(__file__).resolve().parents[1]
    offers_file = ROOT / "data/products/offers.json"
    template_file = ROOT / "templates/homepage.html"
    output_file = ROOT / "index.html"

    if not offers_file.exists():
        print("❌ Arquivo de ofertas não encontrado!")
        return

    with open(offers_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    html_cards = ""
    for p in products[:40]:
        name = p.get("title", "Produto Ninja")
        price = p.get("price", 0)
        old_price = p.get("original_price") or price * 1.2
        img = p.get("thumbnail") or p.get("image")
        link = p.get("permalink", "https://mercadolivre.com.br")
        if "matt_tool" not in link:
            link += "?matt_tool=vendas0nline"
            
        html_cards += f"""
        <div class="card">
            <span class="badge">OFERTA</span>
            <img src="{img}" alt="{name}">
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div>
                    <span class="old-price">R$ {float(old_price):.2f}</span>
                    <span class="price">R$ {float(price):.2f}</span>
                </div>
                <a href="{link}" class="btn" target="_blank">GARANTIR OFERTA</a>
            </div>
        </div>
        """

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(template.replace("{{products}}", html_cards))
    
    print("✅ Site restaurado com sucesso!")

if __name__ == "__main__":
    build()
