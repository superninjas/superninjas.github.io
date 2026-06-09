import json
import requests
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parents[1]

def is_placeholder(url):
    """Verifica se a URL é de um placeholder conhecido."""
    placeholders = [
        "via.placeholder.com",
        "placeholder.com",
        "dummyimage.com"
    ]
    return any(p in url for p in placeholders)

def check_image_valid(url):
    """Valida se a imagem abre e tem conteúdo."""
    if not url or is_placeholder(url):
        return False
    try:
        # User-agent para evitar bloqueios simples
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        resp = requests.get(url, timeout=5, headers=headers, stream=True)
        if resp.status_code == 200:
            # Verificar se é uma imagem e tem tamanho razoável (> 1kb)
            content_type = resp.headers.get('Content-Type', '')
            content_length = int(resp.headers.get('Content-Length', 0))
            if 'image' in content_type and content_length > 1024:
                return True
        return False
    except:
        return False

def process_file(file_path):
    print(f"🔍 Processando {file_path.name}...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            products = json.load(f)
    except Exception as e:
        print(f"❌ Erro ao ler {file_path.name}: {e}")
        return 0, 0

    original_count = len(products)
    valid_products = []
    
    for p in products:
        img_url = p.get("image") or p.get("thumbnail", "")
        if check_image_valid(img_url):
            valid_products.append(p)
        else:
            print(f"   🗑️ Removendo: {p.get('title', 'Sem título')[:40]}... (Imagem inválida/placeholder)")

    # Salvar apenas os válidos
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(valid_products, f, indent=2, ensure_ascii=False)
    
    removed = original_count - len(valid_products)
    return len(valid_products), removed

def main():
    data_dir = ROOT / "data"
    total_active = 0
    total_removed = 0
    
    # Processar todos os arquivos de produtos
    for json_file in sorted(data_dir.glob("products_*.json")):
        active, removed = process_file(json_file)
        total_active += active
        total_removed += removed
        
    print(f"\n{'='*40}")
    print(f"📊 RESULTADO DA LIMPEZA (FASE 1):")
    print(f"{'='*40}")
    print(f"Produtos Ativos: {total_active}")
    print(f"Produtos Removidos: {total_removed}")
    print(f"Total Processado: {total_active + total_removed}")
    print(f"{'='*40}\n")

if __name__ == "__main__":
    main()
