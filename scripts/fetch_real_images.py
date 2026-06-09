import requests
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def get_high_res_image(item):
    """Obtém a imagem de alta resolução do Mercado Livre."""
    img_id = item.get("thumbnail_id")
    if img_id:
        return f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp"
    return item.get("thumbnail", "").replace("-I.jpg", "-O.jpg")

def check_image_accessible(url):
    """Verifica se a imagem é acessível e válida."""
    if not url or "placeholder" in url:
        return False
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resp = requests.head(url, timeout=5, headers=headers, allow_redirects=True)
        return resp.status_code == 200 and 'image' in resp.headers.get('Content-Type', '')
    except:
        return False

def fetch_category(category_config):
    cat_id = category_config["id"]
    ml_id = category_config["ml_id"]
    keywords = category_config["keywords"]
    
    print(f"🚀 Buscando produtos reais para: {category_config['nome']}...")
    
    valid_products = []
    seen_ids = set()
    
    for kw in keywords:
        if len(valid_products) >= 25: # Limite por categoria para esta reconstrução
            break
            
        # Tentar com categoria e depois sem categoria se falhar
        urls = [
            f"https://api.mercadolibre.com/sites/MLB/search?q={kw}&category={ml_id}&limit=50",
            f"https://api.mercadolibre.com/sites/MLB/search?q={kw}&limit=50"
        ]
        
        for url in urls:
            if len(valid_products) >= 25: break
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code != 200:
                continue
                
            results = resp.json().get("results", [])
            for item in results:
                p_id = item.get("id")
                if p_id in seen_ids:
                    continue
                
                img_url = get_high_res_image(item)
                
                # VALIDAÇÃO (FASE 1)
                if not img_url or "placeholder" in img_url:
                    continue
                
                price = item.get("price", 0)
                original_price = item.get("base_price") or price * 1.2
                
                if price <= 0:
                    continue
                
                link = item.get("permalink")
                if "matt_tool" not in link:
                    link += ("&" if "?" in link else "?") + "matt_tool=60566305"
                
                discount = int(((original_price - price) / original_price) * 100) if original_price > price else 0
                
                valid_products.append({
                    "id": p_id,
                    "title": item.get("title"),
                    "name": item.get("title"),
                    "price": price,
                    "original_price": original_price,
                    "image": img_url,
                    "thumbnail": img_url,
                    "permalink": link,
                    "condition": item.get("condition"),
                    "custom_category_slug": cat_id,
                    "custom_discount_pct": discount
                })
                
                seen_ids.add(p_id)
                if len(valid_products) >= 25:
                    break
            
            time.sleep(1) # Cortesia com a API
        except Exception as e:
            print(f"   ⚠️ Erro na busca '{kw}': {e}")
            
    return valid_products

def main():
    with open(ROOT / "data/ROBO4_CONFIG.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    total_new = 0
    for cat in config["categorias"]:
        products = fetch_category(cat)
        file_path = ROOT / f"data/products_{cat['id']}.json"
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
            
        print(f"   ✅ Salvos {len(products)} produtos reais para {cat['nome']}.\n")
        total_new += len(products)
        
    print(f"\n✨ Reconstrução de dados concluída: {total_new} produtos com imagens REAIS.")

if __name__ == "__main__":
    main()
