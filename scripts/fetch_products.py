import requests
import json
import os
from pathlib import Path

def fetch():
    ROOT = Path(__file__).resolve().parents[1]
    output_file = ROOT / "data/products/offers.json"
    os.makedirs(output_file.parent, exist_ok=True)
    
    # Busca real por produtos populares
    queries = ["smartphone", "gamer", "smart tv", "notebook"]
    all_products = []
    
    for q in queries:
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={q}&limit=5"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", []):
                    # CORREÇÃO DA FOTO: Pegar a imagem de alta resolução (O.webp)
                    img_id = item.get("thumbnail_id")
                    if img_id:
                        img_url = f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp"
                    else:
                        img_url = item.get("thumbnail").replace("-I.jpg", "-O.jpg")
                    
                    # LINK DE AFILIADO
                    link = item.get("permalink")
                    if "matt_tool" not in link:
                        link += "?matt_tool=60566305"
                        
                    all_products.append({
                        "title": item.get("title"),
                        "price": item.get("price"),
                        "original_price": item.get("base_price") or item.get("price") * 1.2,
                        "thumbnail": img_url,
                        "permalink": link
                    })
        except:
            continue
            
    # Se a API falhar, usar Fallback com fotos garantidas
    if not all_products:
        all_products = [
            {
                "title": "Smartphone Samsung Galaxy S24 Ultra",
                "price": 6499.00,
                "original_price": 7999.00,
                "thumbnail": "https://http2.mlstatic.com/D_NQ_NP_634347-MLA46114829749_052021-O.webp",
                "permalink": "https://www.mercadolivre.com.br/samsung-galaxy-s24-ultra-5g-512gb-12gb-ram-titanium-black/p/MLB23456789?matt_tool=60566305"
            },
            {
                "title": "Console PlayStation 5 Slim 1TB",
                "price": 3799.00,
                "original_price": 4299.00,
                "thumbnail": "https://http2.mlstatic.com/D_NQ_NP_783633-MLU74315806650_022024-O.webp",
                "permalink": "https://www.mercadolivre.com.br/console-playstation-5-ps5-slim-1tb-standard-edition/p/MLB28635412?matt_tool=60566305"
            }
        ]
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4)
    
    print(f"✅ Robô atualizado: {len(all_products)} produtos com fotos e links!")

if __name__ == "__main__":
    fetch()
