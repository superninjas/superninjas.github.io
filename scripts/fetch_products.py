import requests
import json
import os
from pathlib import Path

def fetch():
    ROOT = Path(__file__).resolve().parents[1]
    output_file = ROOT / "data/products/offers.json"
    os.makedirs(output_file.parent, exist_ok=True)
    
    queries = [
        "smartphone", "iphone 15", "samsung s24", "playstation 5", "xbox", "nintendo switch",
        "notebook gamer", "macbook air", "smart tv 4k", "geladeira duplex", "ar condicionado",
        "fritadeira air fryer", "maquina de lavar", "fone bluetooth", "caixa de som jbl",
        "monitor curvo", "teclado mecanico", "cadeira gamer", "aspirador robo", "perfume"
    ]
    
    all_products = []
    seen_ids = set()
    target_count = 170
    
    for q in queries:
        if len(all_products) >= target_count:
            break
            
        url = f"https://api.mercadolibre.com/sites/MLB/search?q={q}&limit=20"
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", []):
                    if len(all_products) >= target_count:
                        break
                        
                    ml_id = item.get("id")
                    if ml_id in seen_ids:
                        continue
                    seen_ids.add(ml_id)
                    
                    img_id = item.get("thumbnail_id")
                    img_url = f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp" if img_id else item.get("thumbnail").replace("-I.jpg", "-O.jpg")
                    
                    price = item.get("price")
                    original = item.get("original_price") or item.get("base_price") or (price * 1.2)
                    link = item.get("permalink")
                    link = link + ("&" if "?" in link else "?") + "matt_tool=60566305"
                    
                    all_products.append({
                        "id": ml_id,
                        "title": item.get("title"),
                        "price": price,
                        "original_price": original,
                        "thumbnail": img_url,
                        "permalink": link,
                        "custom_discount_pct": int(((original - price) / original) * 100) if original > price else 0
                    })
        except:
            continue
            
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_products, f, indent=4, ensure_ascii=False)
    
    print(f"✅ Robô Ninja: {len(all_products)} produtos REAIS capturados!")

if __name__ == "__main__":
    fetch()
