import os
import json
from pathlib import Path

def generate_blog():
    ROOT = Path(__file__).resolve().parents[1]
    offers_file = ROOT / "data/products/offers.json"
    noticias_dir = ROOT / "noticias"
    os.makedirs(noticias_dir, exist_ok=True)

    with open(offers_file, "r", encoding="utf-8") as f:
        products = json.load(f)

    for p in products[:5]: # Criar 5 posts iniciais
        slug = p['title'].lower().replace(" ", "-")[:50]
        img = p.get("thumbnail") or p.get("image")
        link = p.get("permalink") + "?matt_tool=vendas0nline"
        
        html = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <title>{p['title']} - Vale a pena?</title>
            <link rel="stylesheet" href="/assets/css/style.css">
        </head>
        <body>
            <header class="header"><a href="/" class="logo">🥷 RADAR NINJA</a></header>
            <main style="max-width: 800px; margin: 40px auto; padding: 20px; background: #fff; border-radius: 15px;">
                <h1>Review Ninja: {p['title']}</h1>
                <img src="{img}" style="width: 100%; border-radius: 10px;">
                <p style="font-size: 18px; line-height: 1.6; margin-top: 20px;">
                    Encontramos uma oferta imperdível para o {p['title']}. 
                    Por apenas <strong>R$ {p['price']:.2f}</strong>, este produto se destaca pelo custo-benefício.
                </p>
                <a href="{link}" class="btn" style="max-width: 300px; margin: 30px auto;">COMPRAR COM DESCONTO</a>
            </main>
        </body>
        </html>
        """
        with open(noticias_dir / f"{slug}.html", "w", encoding="utf-8") as f:
            f.write(html)
    
    print("✅ Blog com fotos e links gerado!")

if __name__ == "__main__":
    generate_blog()
