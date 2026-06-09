#!/usr/bin/env python3
"""
Script para expandir o catálogo do Radar Ninja para 200 produtos.
Coleta produtos do Mercado Livre com validação rigorosa.
"""

import json
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

ROOT = Path(__file__).resolve().parents[1]

# Configuração de categorias e palavras-chave
CATEGORIES = {
    "celular": {
        "keywords": ["smartphone", "iphone", "samsung galaxy", "xiaomi", "motorola", "realme"],
        "target": 35
    },
    "games": {
        "keywords": ["playstation 5", "xbox series x", "nintendo switch", "ps5", "xbox", "jogo"],
        "target": 30
    },
    "tv-e-video": {
        "keywords": ["smart tv 4k", "smart tv", "tv led", "monitor", "tv samsung", "tv lg"],
        "target": 25
    },
    "informatica": {
        "keywords": ["notebook", "laptop", "macbook", "dell", "lenovo", "asus", "ssd"],
        "target": 35
    },
    "eletrodomesticos": {
        "keywords": ["geladeira", "fogão", "lavadora", "microondas", "ar condicionado"],
        "target": 20
    },
    "beleza": {
        "keywords": ["perfume", "maquiagem", "shampoo", "creme facial", "desodorante"],
        "target": 20
    },
    "moda": {
        "keywords": ["tênis", "relógio", "mochila", "óculos", "camiseta", "jaqueta"],
        "target": 35
    }
}

def is_valid_image_url(url):
    """Verifica se uma URL de imagem é válida e acessível."""
    if not url or not isinstance(url, str):
        return False
    if not url.startswith(("http://", "https://")):
        return False
    try:
        resp = requests.head(url, timeout=2, allow_redirects=True)
        return resp.status_code < 400
    except:
        return False

def fetch_products_from_ml(keyword, category, limit=10):
    """Coleta produtos do Mercado Livre para uma palavra-chave."""
    products = []
    url = f"https://api.mercadolibre.com/sites/MLB/search"
    
    params = {
        "q": keyword,
        "limit": limit,
        "sort": "price_asc"  # Ordenar por preço crescente para variedade
    }
    
    try:
        response = requests.get(url, params=params, timeout=5)
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        for item in data.get("results", []):
            # Extrair imagem de alta resolução
            img_id = item.get("thumbnail_id")
            if img_id:
                img_url = f"https://http2.mlstatic.com/D_NQ_NP_{img_id}-O.webp"
            else:
                img_url = item.get("thumbnail", "").replace("-I.jpg", "-O.jpg")
            
            # Validar imagem
            if not is_valid_image_url(img_url):
                continue
            
            # Extrair dados do produto
            product = {
                "id": item.get("id", ""),
                "title": item.get("title", "").strip(),
                "name": item.get("title", "").strip(),
                "price": float(item.get("price", 0)),
                "original_price": float(item.get("original_price", 0)) or float(item.get("price", 0)),
                "image": img_url,
                "thumbnail": img_url,
                "permalink": item.get("permalink", ""),
                "condition": item.get("condition", "new"),
                "custom_category_slug": category,
                "custom_discount_pct": 0
            }
            
            # Calcular desconto
            if product["original_price"] > product["price"]:
                discount = int(((product["original_price"] - product["price"]) / product["original_price"]) * 100)
                product["custom_discount_pct"] = max(0, min(100, discount))
            
            # Validações
            if not product["title"] or len(product["title"]) < 5:
                continue
            if product["price"] <= 0:
                continue
            if not product["permalink"]:
                continue
            
            products.append(product)
    
    except Exception as e:
        print(f"⚠️ Erro ao buscar '{keyword}': {e}")
    
    return products

def expand_catalog():
    """Expande o catálogo para 200 produtos."""
    print("🚀 Expandindo catálogo do Radar Ninja para 200 produtos...\n")
    
    all_products = {}
    stats = {}
    
    for category, config in CATEGORIES.items():
        print(f"📦 Categoria: {category}")
        category_products = []
        
        for keyword in config["keywords"]:
            print(f"   🔍 Buscando '{keyword}'...")
            products = fetch_products_from_ml(keyword, category, limit=15)
            category_products.extend(products)
            time.sleep(0.5)  # Rate limit
        
        # Remover duplicatas por ID
        seen_ids = set()
        unique_products = []
        for p in category_products:
            if p["id"] not in seen_ids:
                seen_ids.add(p["id"])
                unique_products.append(p)
        
        # Limitar ao target
        unique_products = unique_products[:config["target"]]
        
        all_products[category] = unique_products
        stats[category] = {
            "target": config["target"],
            "collected": len(unique_products),
            "percentage": (len(unique_products) / config["target"] * 100) if config["target"] > 0 else 0
        }
        
        print(f"   ✅ Coletados: {len(unique_products)}/{config['target']}")
        print()
    
    # Salvar produtos por categoria
    data_dir = ROOT / "data"
    total_collected = 0
    
    for category, products in all_products.items():
        file_path = data_dir / f"products_{category}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(products, f, indent=2, ensure_ascii=False)
        total_collected += len(products)
    
    # Gerar relatório
    print(f"\n{'='*60}")
    print(f"📊 RESUMO DA EXPANSÃO:")
    print(f"{'='*60}")
    print(f"Total de produtos coletados: {total_collected}")
    print(f"Meta: 200 produtos")
    print(f"Progresso: {(total_collected/200*100):.1f}%\n")
    
    for category, stat in stats.items():
        print(f"{category:20} {stat['collected']:3}/{stat['target']:3} ({stat['percentage']:5.1f}%)")
    
    # Salvar estatísticas
    report = {
        "total_target": 200,
        "total_collected": total_collected,
        "by_category": stats
    }
    
    with open(ROOT / "expansion_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Catálogo expandido! Relatório salvo em expansion_report.json")

if __name__ == "__main__":
    expand_catalog()
