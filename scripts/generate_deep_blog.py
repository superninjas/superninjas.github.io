import json
import os
from pathlib import Path

def generate_blog():
    ROOT = Path(__file__).resolve().parents[1]
    offers_file = ROOT / "data/products/offers.json"
    blog_dir = ROOT / "noticias"
    template_file = ROOT / "templates/blog_post.html"
    
    os.makedirs(blog_dir, exist_ok=True)

    products = []
    if offers_file.exists():
        with open(offers_file, "r", encoding="utf-8") as f:
            products = json.load(f)

    for p in products[:10]:
        name = p.get("title") or p.get("name")
        price = p.get("price", 0)
        img = p.get("image") or p.get("thumbnail")
        link = p.get("permalink", "https://mercadolivre.com.br")
        if "matt_tool" not in link:
            link += "?matt_tool=vendas0nline"
            
        slug = name.lower().replace(" ", "-")[:50]
        post_file = blog_dir / f"{slug}.html"
        
        content = f"""
        <article class="blog-post">
            <h1>Vale a pena comprar o {name}?</h1>
            <img src="{img}" alt="{name}" style="max-width:100%; border-radius:15px;">
            <p>Analisamos o {name} e descobrimos que ele é uma das melhores opções do mercado atualmente.</p>
            <div class="price-tag">Preço Ninja: R$ {float(price):.2f}</div>
            <a href="{link}" class="btn-cta" target="_blank">COMPRAR AGORA COM DESCONTO</a>
        </article>
        """
        
        with open(post_file, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"✅ Blog gerado com {len(products[:10])} postagens com fotos!")

if __name__ == "__main__":
    generate_blog()
