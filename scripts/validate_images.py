#!/usr/bin/env python3
"""
Script de validação e fallback de imagens para o Radar Ninja.
Garante que todos os produtos tenham imagens válidas antes da publicação.
"""

import json
import requests
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]

# Imagens padrão por categoria (usando URLs públicas confiáveis)
DEFAULT_IMAGES = {
    "celular": "https://via.placeholder.com/300x300?text=Celular",
    "games": "https://via.placeholder.com/300x300?text=Games",
    "tv-e-video": "https://via.placeholder.com/300x300?text=TV",
    "informatica": "https://via.placeholder.com/300x300?text=Notebook",
    "eletrodomesticos": "https://via.placeholder.com/300x300?text=Eletrodomestico",
    "beleza": "https://via.placeholder.com/300x300?text=Beleza",
    "moda": "https://via.placeholder.com/300x300?text=Moda"
}

def is_valid_url(url):
    """Verifica se uma URL é válida."""
    if not url or not isinstance(url, str):
        return False
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except:
        return False

def check_image_accessible(url, timeout=3):
    """Verifica se uma imagem é acessível."""
    if not is_valid_url(url):
        return False
    try:
        resp = requests.head(url, timeout=timeout, allow_redirects=True)
        return resp.status_code < 400
    except:
        return False

def get_fallback_image(category):
    """Retorna a imagem padrão para uma categoria."""
    return DEFAULT_IMAGES.get(category, DEFAULT_IMAGES["celular"])

def validate_product(product):
    """
    Valida um produto e retorna (é_válido, produto_corrigido, motivo).
    """
    # Validar campos obrigatórios
    title = product.get("title") or product.get("name", "").strip()
    price = product.get("price", 0)
    link = product.get("permalink", "").strip()
    category = product.get("custom_category_slug", "celular").strip()
    
    # Verificar título
    if not title or len(title) < 5:
        return False, product, "Título inválido ou muito curto"
    
    # Verificar preço
    try:
        price_float = float(price)
        if price_float <= 0:
            return False, product, "Preço inválido (≤ 0)"
    except:
        return False, product, "Preço não é um número válido"
    
    # Verificar link
    if not is_valid_url(link):
        return False, product, "URL de destino inválida"
    
    # Verificar/corrigir imagem
    img_url = product.get("image") or product.get("thumbnail", "").strip()
    
    if not img_url or not is_valid_url(img_url):
        # Usar fallback
        product["image"] = get_fallback_image(category)
        product["thumbnail"] = product["image"]
        return True, product, "Imagem corrigida com fallback"
    
    # Tentar validar URL da imagem
    if not check_image_accessible(img_url):
        # Usar fallback
        product["image"] = get_fallback_image(category)
        product["thumbnail"] = product["image"]
        return True, product, "Imagem quebrada, usando fallback"
    
    return True, product, "Válido"

def validate_products_file(file_path):
    """Valida todos os produtos em um arquivo JSON."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            products = json.load(f)
    except:
        return [], [], 0

    valid_products = []
    rejected_products = []
    
    for product in products:
        is_valid, corrected_product, reason = validate_product(product)
        if is_valid:
            valid_products.append(corrected_product)
        else:
            rejected_products.append({
                "product": product,
                "reason": reason
            })
    
    # Salvar produtos validados
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(valid_products, f, indent=2, ensure_ascii=False)
    
    return valid_products, rejected_products, len(products)

def main():
    print("🖼️ Validando imagens e dados de produtos...\n")
    
    data_dir = ROOT / "data"
    total_valid = 0
    total_rejected = 0
    total_original = 0
    
    stats_by_category = {}
    
    for json_file in sorted(data_dir.glob("products_*.json")):
        valid, rejected, original = validate_products_file(json_file)
        category = json_file.stem.replace("products_", "")
        
        total_valid += len(valid)
        total_rejected += len(rejected)
        total_original += original
        
        stats_by_category[category] = {
            "valid": len(valid),
            "rejected": len(rejected),
            "original": original
        }
        
        print(f"📁 {category}:")
        print(f"   ✅ Válidos: {len(valid)}")
        print(f"   ❌ Rejeitados: {len(rejected)}")
        if rejected:
            for r in rejected[:2]:
                print(f"      - {r['product'].get('title', 'N/A')[:40]}: {r['reason']}")
        print()
    
    print(f"\n{'='*60}")
    print(f"📊 RESUMO FINAL:")
    print(f"{'='*60}")
    print(f"Total de produtos originais: {total_original}")
    print(f"Produtos válidos: {total_valid}")
    print(f"Produtos rejeitados: {total_rejected}")
    print(f"Taxa de aprovação: {(total_valid/total_original*100):.1f}%" if total_original > 0 else "N/A")
    
    # Salvar estatísticas
    report = {
        "total_original": total_original,
        "total_valid": total_valid,
        "total_rejected": total_rejected,
        "by_category": stats_by_category
    }
    
    with open(ROOT / "validation_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Validação concluída! Relatório salvo em validation_report.json")

if __name__ == "__main__":
    main()
