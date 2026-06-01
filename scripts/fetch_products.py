import requests
import json
import os
from pathlib import Path

def fetch():
    ROOT = Path(__file__).resolve().parents[1]
    output_file = ROOT / "data/products/offers.json"
    os.makedirs(output_file.parent, exist_ok=True)
    
    # Categorias do Mercado Livre
    categories = ["MLB1051", "MLB1144", "MLB1000"] # Celulares, Games, Eletrônicos
    all_products = []
    
    for cat in categories:
        url = f"https://api.mercadolibre.com/sites/MLB/search?category={cat}&limit=10"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("results", []):
                # Pegar imagem de alta qualidade
                img_id = item.get("thumbnail_id")
                img_url = f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp" if img_id else item.get("thumbnail")
                
                # Garantir Link de Afiliado
                link = item.get("permalink")
                if "matt_tool" not in link:
                    link += "?matt_tool=vendas0nline"
                
                all_products.append({
                    "title": item.get("title"),
                    "price": item.get("price"),
                    "original_price": item.get("base_price") or item.get("price") * 1.2,
                    "thumbnail": img_url,
                    "permalink": link
                })
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4)
    
    print(f"✅ {len(all_products)} produtos buscados com fotos e links reais!")

if __name__ == "__main__":
    fetch()
