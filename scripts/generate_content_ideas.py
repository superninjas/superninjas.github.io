import json
import random
from datetime import datetime

def generate_seo_metrics():
    return {
        "volume_estimado": random.randint(1000, 10000),
        "dificuldade_estimada": random.randint(40, 80)
    }

def generate_content_ideas():
    categories = {
        "Celulares": [
            "Samsung Galaxy S24", "iPhone 15", "Xiaomi Redmi Note 13 Pro", "Motorola Edge 50 Pro", "Melhor celular custo-benefício 2026",
            "Google Pixel 8 Pro", "OnePlus 12", "Asus ROG Phone 8", "Realme GT 5 Pro", "Oppo Find X7 Ultra"
        ],
        "Games": [
            "PS5 Slim", "Xbox Series X", "Nintendo Switch OLED", "Melhores jogos de RPG 2026", "Acessórios gamer essenciais",
            "PC Gamer de alto desempenho", "Steam Deck", "Meta Quest 3", "Jogos de aventura", "Controles personalizados"
        ],
        "Informática": [
            "Notebook gamer RTX 4090", "MacBook Air M3", "SSD NVMe 4TB", "Monitor ultrawide 144Hz", "Melhor PC para trabalho remoto",
            "Teclado mecânico", "Mouse ergonômico", "Webcam 4K", "Roteador Wi-Fi 7", "Impressora multifuncional"
        ],
        "TVs": [
            "Smart TV 4K Samsung Neo QLED", "TV OLED LG C4", "TV QLED TCL C845", "Melhor TV para games 120Hz", "Soundbar Dolby Atmos",
            "Projetor 4K", "Chromecast com Google TV", "Apple TV 4K", "Suporte de parede para TV", "Antena digital"
        ],
        "Eletrodomésticos": [
            "Geladeira frost free inverse", "Máquina de lavar 15kg", "Air fryer digital 5L", "Robô aspirador inteligente", "Cafeteira expresso automática",
            "Forno elétrico de embutir", "Micro-ondas com grill", "Lava-louças", "Liquidificador de alta potência", "Batedeira planetária"
        ]
    }

    content_types = {
        "Guias Ninja": [
            "Como escolher um {product_type}",
            "Guia completo para comprar {product_type}",
            "Tudo o que você precisa saber sobre {product_type}",
            "{product_type}: O guia definitivo de compra"
        ],
        "Comparativos": [
            "{product_type_1} vs {product_type_2}: Qual o melhor?",
            "Comparativo: {product_type_1} ou {product_type_2}?",
            "{product_type_1} vs {product_type_2}: Análise completa"
        ],
        "Alertas de Compra": [
            "{product_type} em promoção: Comprar agora ou esperar?",
            "Melhor preço histórico de {product_type}",
            "{product_type} vale a pena? Análise de preço"
        ],
        "Rankings": [
            "Melhores {product_type} até R$ X em 2026",
            "Top 10 {product_type} de 2026",
            "{product_type} com melhor custo-benefício"
        ]
    }

    all_content_ideas = []
    generated_titles = set()

    # Target 100 articles per content type, total 400
    target_per_type = 100
    
    # Calculate how many articles of each content_type should come from each category
    # 100 articles per content type / 5 categories = 20 articles per content type per category
    target_per_category_content_type = target_per_type // len(categories)

    for category, products in categories.items():
        for content_type, templates in content_types.items():
            current_count_for_pair = 0
            attempts = 0
            max_attempts = 200 # Increased attempts to ensure uniqueness

            while current_count_for_pair < target_per_category_content_type and attempts < max_attempts:
                template = random.choice(templates)
                title = ""

                if "{product_type_1}" in template:
                    if len(products) >= 2:
                        p1, p2 = random.sample(products, 2)
                        title = template.format(product_type_1=p1, product_type_2=p2)
                    else:
                        attempts += 1
                        continue # Not enough products for comparison
                elif "{product_type}" in template:
                    product = random.choice(products)
                    if "R$ X" in template:
                        price = random.choice(["1.000", "2.000", "3.000", "5.000", "10.000"])
                        title = template.format(product_type=product, X=price)
                    else:
                        title = template.format(product_type=product)
                else:
                    title = template # Fallback for templates without placeholders

                if title and title not in generated_titles:
                    seo_metrics = generate_seo_metrics()
                    all_content_ideas.append({
                        "categoria": category,
                        "tipo_conteudo": content_type,
                        "titulo": title,
                        "palavra_chave_alvo": title.lower().replace(" ", "-").replace("r$-x", "preco").replace("r$", "").replace("-", " ").strip(),
                        "volume_estimado": seo_metrics["volume_estimado"],
                        "dificuldade_estimada": seo_metrics["dificuldade_estimada"]
                    })
                    generated_titles.add(title)
                    current_count_for_pair += 1
                attempts += 1

    return all_content_ideas

if __name__ == "__main__":
    ideas = generate_content_ideas()
    # Sort by category and then content type for better readability
    ideas_sorted = sorted(ideas, key=lambda x: (x["categoria"], x["tipo_conteudo"], x["titulo"])) # Added title to sort key
    print(json.dumps(ideas_sorted, indent=2, ensure_ascii=False))
