import json
import os
from pathlib import Path

def build():
    ROOT = Path(__file__).resolve().parents[1]
    offers_file = ROOT / "data/products/offers.json"
    template_file = ROOT / "templates/homepage.html"
    output_file = ROOT / "index.html"

    # Criar dados de exemplo se o arquivo não existir para o site não ficar vazio
    if not offers_file.exists():
        os.makedirs(offers_file.parent, exist_ok=True)
        sample_data = [
            {
                "title": "Smartphone Samsung Galaxy S24 Ultra",
                "price": 6499.00,
                "original_price": 7999.00,
                "thumbnail": "https://http2.mlstatic.com/D_NQ_NP_634347-MLA46114829749_052021-O.webp",
                "permalink": "https://www.mercadolivre.com.br/samsung-galaxy-s24-ultra-5g-512gb-12gb-ram-titanium-black/p/MLB23456789"
            }
        ]
        with open(offers_file, "w", encoding="utf-8") as f:
            json.dump(sample_data, f)

    with open(offers_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    html_cards = ""
    for p in products:
        name = p.get("title", "Produto")
        price = p.get("price", 0)
        old_price = p.get("original_price") or price * 1.2
        img = p.get("thumbnail") or p.get("image")
        link = p.get("permalink", "https://mercadolivre.com.br")
        
        # GARANTIR LINK DE AFILIADO
        if "matt_tool" not in link:
            link += "?matt_tool=vendas0nline"
            
        html_cards += f"""
        <div class="card">
            <span class="badge">OFERTA NINJA</span>
            <img src="{img}" alt="{name}">
            <div class="card-info">
                <div class="card-title">{name}</div>
                <div>
                    <span class="old-price">R$ {float(old_price):.2f}</span>
                    <span class="price">R$ {float(price):.2f}</span>
                </div>
                <a href="{link}" class="btn" target="_blank">VER OFERTA NINJA</a>
            </div>
        </div>
        """

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(template.replace("{{products}}", html_cards))
    
    print("✅ Homepage com links de afiliado gerada!")

if __name__ == "__main__":
    build()
