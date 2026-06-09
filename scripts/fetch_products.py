import requests
import json
import os
from pathlib import Path

def fetch():
    ROOT = Path(__file__).resolve().parents[1]
    output_file = ROOT / "data/products/offers.json"
    os.makedirs(output_file.parent, exist_ok=True)
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    queries = ["celular", "iphone", "ps5", "tv", "notebook", "air fryer", "fone", "geladeira"]
    all_products = []
    seen_ids = set()
    
    for q in queries:
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={q}&limit=50"
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                data = r.json()
                for item in data.get("results", []):
                    if len(all_products) >= 170: break
                    mid = item.get("id")
                    if mid not in seen_ids:
                        seen_ids.add(mid)
                        img_id = item.get("thumbnail_id")
                        img = f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp" if img_id else item.get("thumbnail")
                        price = item.get("price")
                        old = item.get("original_price") or (price * 1.2)
                        all_products.append({
                            "title": item.get("title"),
                            "price": price,
                            "original_price": old,
                            "thumbnail": img,
                            "permalink": item.get("permalink") + "?matt_tool=60566305",
                            "custom_discount_pct": int((1 - price/old)*100) if old > price else 0
                        })
            else:
                print(f"⚠️ Erro na API ({r.status_code}) para {q}")
        except Exception as e:
            print(f"⚠️ Erro de conexão: {e}")
            
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4)
    print(f"✅ Sucesso: {len(all_products)} produtos.")

if __name__ == "__main__":
    fetch()
