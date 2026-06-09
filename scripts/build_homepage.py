import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build():
    print("🏠 Construindo homepage premium...")

    offers_file = ROOT / "data/products/offers.json"
    template_file = ROOT / "templates/homepage.html"
    output_file = ROOT / "index.html"

    # Carregar template
    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    # Carregar produtos de todas as fontes
    all_products = []

    # Carregar offers.json principal
    if offers_file.exists():
        with open(offers_file, "r", encoding="utf-8") as f:
            main_products = json.load(f)
            all_products.extend(main_products)

    # Carregar arquivos de categoria individuais
    data_dir = ROOT / "data"
    for cat_file in data_dir.glob("products_*.json"):
        try:
            with open(cat_file, "r", encoding="utf-8") as f:
                cat_products = json.load(f)
                all_products.extend(cat_products)
        except Exception as e:
            print(f"⚠️ Erro ao carregar {cat_file}: {e}")

    # Remover duplicatas por ID
    seen_ids = set()
    unique_products = []
    for p in all_products:
        pid = p.get("id", "")
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            unique_products.append(p)
        elif not pid:
            unique_products.append(p)

    # Ordenar por desconto
    unique_products.sort(key=lambda x: x.get("custom_discount_pct", 0), reverse=True)

    # Gerar HTML dos produtos
    products_html = ""

    if not unique_products:
        products_html = """
        <div style="grid-column: 1/-1; text-align: center; padding: 80px 20px;">
            <div style="font-size: 60px; margin-bottom: 20px;">🥷</div>
            <h2 style="font-size: 24px; font-weight: 800; color: var(--ninja-dark); margin-bottom: 10px;">Robô Buscando Ofertas...</h2>
            <p style="color: var(--ninja-gray); font-size: 16px; max-width: 400px; margin: 0 auto 30px;">
                Nosso robô está monitorando o Mercado Livre. As melhores ofertas aparecerão aqui em breve!
            </p>
            <a href="/categorias/celular/" class="btn" style="display: inline-block; padding: 14px 30px;">
                Ver Celulares →
            </a>
        </div>
        """
    else:
        for p in unique_products[:24]:
            title = p.get("title") or p.get("name", "Produto")
            price = p.get("price", 0)
            original = p.get("original_price") or p.get("originalPrice", 0)
            image = p.get("thumbnail") or p.get("image", "")
            link = p.get("permalink", "#")
            discount = p.get("custom_discount_pct", 0)
            cat_slug = p.get("custom_category_slug", "")

            if not discount and original and original > price:
                discount = int(((original - price) / original) * 100)

            # Link de afiliado
            if "mercadolivre.com.br" in link and "matt_tool" not in link:
                link = link + ("&" if "?" in link else "?") + "matt_tool=vendas0nline"

            badge_html = f'<span class="badge">↓ {discount}% OFF</span>' if discount >= 5 else '<span class="badge badge-green">OFERTA</span>'
            old_price_html = f'<span class="old-price">De R$ {float(original):.2f}</span>' if original and float(original) > float(price) else ""
            installments = int(float(price) / 12) if float(price) >= 120 else 0
            installments_html = f'<div class="price-installments">ou 12x de R$ {installments:.0f}</div>' if installments else ""

            # Calcular economia
            savings = int(float(original) - float(price)) if original and float(original) > float(price) else 0
            savings_html = f'<div class="savings">💰 Economize R$ {savings:.0f}</div>' if savings > 0 else ""
            
            products_html += f"""
            <div class="card" itemscope itemtype="https://schema.org/Product">
                {badge_html}
                <div class="card-img-wrap">
                    <img src="{image}" alt="{title}" loading="lazy" itemprop="image">
                </div>
                <div class="card-info">
                    <h3 class="card-title" itemprop="name">{title[:80]}</h3>
                    {savings_html}
                    <div class="price-wrap" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                        {old_price_html}
                        <div class="price" itemprop="price" content="{float(price):.2f}">R$ {float(price):.2f}</div>
                        <meta itemprop="priceCurrency" content="BRL">
                        <meta itemprop="availability" content="https://schema.org/InStock">
                        {installments_html}
                    </div>
                    <a href="{link}" class="btn" target="_blank" rel="nofollow sponsored" itemprop="url">
                        🛒 Ver Oferta
                    </a>
                </div>
            </div>
            """

    # Substituir no template
    html = template.replace("{{products}}", products_html)

    # Salvar index.html
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Homepage gerada com {len(unique_products)} produtos!")

if __name__ == "__main__":
    build()
