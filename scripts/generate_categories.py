import os
import json
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = text.lower().replace(" ", "-")
    return "".join(c for c in text if c.isalnum() or c == "-")

# Guias de compra por categoria
BUYING_GUIDES = {
    "celular": """
    <section class="buying-guide">
        <h2>📱 Guia de Compra: Como Escolher o Melhor Celular</h2>
        <p>Comprar um celular pode ser uma decisão difícil com tantas opções disponíveis. Nosso guia vai te ajudar a escolher o smartphone ideal para o seu perfil e orçamento.</p>
        <h3>O que avaliar antes de comprar</h3>
        <ul class="checklist">
            <li><strong>Processador:</strong> Para uso básico, qualquer processador serve. Para jogos e multitarefa, prefira Snapdragon 8 Gen ou equivalente.</li>
            <li><strong>Memória RAM:</strong> Mínimo 6GB para uso confortável. 8GB ou mais para jogos e apps pesados.</li>
            <li><strong>Armazenamento:</strong> 128GB é o mínimo recomendado hoje. Prefira 256GB se possível.</li>
            <li><strong>Câmera:</strong> Megapixels não são tudo. Avalie abertura da lente, estabilização e processamento de imagem.</li>
            <li><strong>Bateria:</strong> Mínimo 4.500mAh para durar o dia todo. Verifique a velocidade de carregamento.</li>
            <li><strong>Sistema:</strong> Android oferece mais personalização; iOS é mais fluido e recebe atualizações por mais tempo.</li>
        </ul>
        <h3>Melhores marcas em 2026</h3>
        <p>Samsung lidera o mercado brasileiro com ótimo custo-benefício. Apple domina o premium. Motorola é excelente para quem quer bom desempenho por menos. Xiaomi oferece ótimas câmeras e bateria por preços competitivos.</p>
        <div class="alert alert-info">
            💡 <strong>Dica Ninja:</strong> Evite comprar o lançamento mais recente. Modelos do ano anterior costumam ter ótimo custo-benefício com descontos de 20-40%.
        </div>
        <p><a href="/guias/como-comprar-celular/">Leia o guia completo de celulares →</a></p>
    </section>
    """,
    "games": """
    <section class="buying-guide">
        <h2>🎮 Guia de Compra: Como Escolher seu Console</h2>
        <p>PlayStation, Xbox ou Nintendo? Cada console tem seus pontos fortes. Veja qual é o ideal para você.</p>
        <h3>Comparativo dos principais consoles</h3>
        <table class="comparison-table">
            <thead>
                <tr><th>Console</th><th>Preço Médio</th><th>Exclusivos</th><th>Online</th><th>Ideal Para</th></tr>
            </thead>
            <tbody>
                <tr class="best"><td>PlayStation 5</td><td>R$ 3.500</td><td class="check">★★★★★</td><td>PlayStation Plus</td><td>Exclusivos Sony</td></tr>
                <tr><td>Xbox Series X</td><td>R$ 3.800</td><td class="check">★★★★</td><td>Game Pass</td><td>Variedade + PC</td></tr>
                <tr><td>Nintendo Switch</td><td>R$ 2.200</td><td class="check">★★★★★</td><td>Nintendo Online</td><td>Família e portátil</td></tr>
            </tbody>
        </table>
        <div class="alert alert-success">
            🎯 <strong>Melhor custo-benefício:</strong> PS5 Slim para quem quer os melhores exclusivos. Nintendo Switch para famílias.
        </div>
        <p><a href="/guias/console-games/">Leia o guia completo de consoles →</a></p>
    </section>
    """,
    "tv-e-video": """
    <section class="buying-guide">
        <h2>📺 Guia de Compra: Como Escolher a Smart TV Certa</h2>
        <p>Tamanho, resolução, tecnologia de painel... entenda o que realmente importa na hora de comprar uma Smart TV.</p>
        <h3>Qual tamanho escolher?</h3>
        <ul class="checklist">
            <li><strong>Até 43":</strong> Ideal para quartos ou salas pequenas (até 15m²)</li>
            <li><strong>50" a 55":</strong> Perfeito para salas médias (15 a 25m²)</li>
            <li><strong>65" ou mais:</strong> Para salas grandes (acima de 25m²) ou home theater</li>
        </ul>
        <h3>Tecnologias de painel</h3>
        <table class="comparison-table">
            <thead>
                <tr><th>Tecnologia</th><th>Qualidade</th><th>Preço</th><th>Melhor Para</th></tr>
            </thead>
            <tbody>
                <tr><td>LED/LCD</td><td>Boa</td><td>Acessível</td><td>Uso geral</td></tr>
                <tr class="best"><td>QLED</td><td>Muito boa</td><td>Médio</td><td>Cores vibrantes</td></tr>
                <tr><td>OLED</td><td>Excelente</td><td>Premium</td><td>Cinema em casa</td></tr>
            </tbody>
        </table>
        <p><a href="/guias/smart-tv-4k/">Leia o guia completo de Smart TVs →</a></p>
    </section>
    """,
    "informatica": """
    <section class="buying-guide">
        <h2>💻 Guia de Compra: Como Escolher o Melhor Notebook</h2>
        <p>Trabalho, estudo ou games? Cada uso exige configurações diferentes. Veja o que avaliar.</p>
        <h3>Por tipo de uso</h3>
        <ul class="checklist">
            <li><strong>Uso básico (internet, Office):</strong> Intel Core i3/i5 ou Ryzen 3/5, 8GB RAM, 256GB SSD</li>
            <li><strong>Trabalho criativo:</strong> Intel Core i5/i7 ou Ryzen 5/7, 16GB RAM, 512GB SSD, tela Full HD+</li>
            <li><strong>Games:</strong> Intel Core i7/i9 ou Ryzen 7/9, 16-32GB RAM, RTX 3060+, 512GB SSD</li>
        </ul>
        <div class="alert alert-warning">
            ⚠️ <strong>Atenção:</strong> Prefira sempre SSD ao HD. A diferença de velocidade é enorme e impacta diretamente a experiência de uso.
        </div>
        <p><a href="/guias/melhor-notebook/">Leia o guia completo de notebooks →</a></p>
    </section>
    """,
    "eletrodomesticos": """
    <section class="buying-guide">
        <h2>🏠 Guia de Compra: Eletrodomésticos com Melhor Custo-Benefício</h2>
        <p>Geladeira, fogão, lavadora ou ar-condicionado? Saiba o que avaliar antes de comprar.</p>
        <h3>Dicas gerais para eletrodomésticos</h3>
        <ul class="checklist">
            <li><strong>Eficiência energética:</strong> Prefira produtos com selo Procel A. Economizam até 40% na conta de luz.</li>
            <li><strong>Capacidade:</strong> Calcule pelo número de pessoas na casa. Não compre maior do que precisa.</li>
            <li><strong>Garantia:</strong> Prefira marcas com assistência técnica na sua cidade.</li>
            <li><strong>Instalação:</strong> Verifique se o produto precisa de instalação especializada (ar-condicionado, fogão a gás).</li>
        </ul>
        <p><a href="/noticias/">Veja mais dicas no nosso blog →</a></p>
    </section>
    """,
    "beleza": """
    <section class="buying-guide">
        <h2>💄 Guia de Compra: Produtos de Beleza e Cuidados Pessoais</h2>
        <p>Perfumes, maquiagem, cuidados com o cabelo... saiba como identificar as melhores ofertas.</p>
        <h3>O que verificar antes de comprar</h3>
        <ul class="checklist">
            <li><strong>Autenticidade:</strong> Compre sempre de vendedores oficiais no Mercado Livre.</li>
            <li><strong>Validade:</strong> Verifique a data de validade do produto.</li>
            <li><strong>Avaliações:</strong> Leia os comentários de outros compradores.</li>
            <li><strong>Ingredientes:</strong> Verifique se não há ingredientes que você tem alergia.</li>
        </ul>
        <p><a href="/noticias/">Veja mais dicas no nosso blog →</a></p>
    </section>
    """,
    "moda": """
    <section class="buying-guide">
        <h2>👟 Guia de Compra: Moda e Acessórios Online</h2>
        <p>Comprar roupas e acessórios online tem suas vantagens e cuidados. Veja nossas dicas.</p>
        <h3>Dicas para comprar moda online</h3>
        <ul class="checklist">
            <li><strong>Tabela de medidas:</strong> Sempre consulte a tabela de medidas do vendedor.</li>
            <li><strong>Material:</strong> Verifique a composição do tecido na descrição.</li>
            <li><strong>Avaliações com foto:</strong> Priorize avaliações com fotos reais do produto.</li>
            <li><strong>Política de troca:</strong> Verifique se o vendedor aceita trocas por tamanho.</li>
        </ul>
        <p><a href="/noticias/">Veja mais dicas no nosso blog →</a></p>
    </section>
    """
}

# Descrições de categoria para SEO
CATEGORY_DESCRIPTIONS = {
    "celular": "Encontre os melhores preços em smartphones Samsung, iPhone, Motorola, Xiaomi e muito mais. Nosso robô monitora o Mercado Livre 24h para garantir que você pague menos.",
    "games": "As melhores ofertas em consoles PlayStation, Xbox, Nintendo, jogos e acessórios gamer. Preços verificados e atualizados a cada hora.",
    "tv-e-video": "Smart TVs 4K, OLED, QLED e LED com os melhores preços. Samsung, LG, Sony e mais marcas com descontos reais encontrados pelo nosso robô.",
    "informatica": "Notebooks, desktops, periféricos e acessórios de informática com preços imperdíveis. Monitore e compare antes de comprar.",
    "eletrodomesticos": "Geladeiras, lavadoras, fogões, ar-condicionado e muito mais. Os melhores eletrodomésticos com preços monitorados pelo Radar Ninja.",
    "beleza": "Perfumes, maquiagem, cuidados com o cabelo e produtos de beleza com os melhores preços do Mercado Livre.",
    "moda": "Tênis, roupas, relógios, bolsas e acessórios de moda com descontos reais. Encontre as melhores ofertas de moda no Mercado Livre."
}

def generate_categories():
    print("🎨 Iniciando geração de categorias premium...")

    db_path = ROOT / "data/products/offers.json"
    template_path = ROOT / "templates/category_template.html"
    config_path = ROOT / "data/ROBO4_CONFIG.json"

    # Verificar arquivos necessários
    if not template_path.exists():
        print(f"❌ Template não encontrado: {template_path}")
        return

    if not config_path.exists():
        print(f"❌ Config não encontrada: {config_path}")
        return

    # Carregar template
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Carregar config
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    # Carregar produtos de todas as fontes
    all_products = []

    # Tentar carregar offers.json
    if db_path.exists():
        with open(db_path, "r", encoding="utf-8") as f:
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

    print(f"📦 Total de produtos únicos: {len(unique_products)}")

    categories_config = {cat["id"]: cat["nome"] for cat in config["categorias"]}

    for cat_slug, cat_name in categories_config.items():
        # Filtrar produtos desta categoria (aceitar variações de slug)
        cat_products = [
            p for p in unique_products
            if p.get("custom_category_slug", "").replace("s", "") == cat_slug.replace("s", "")
            or p.get("custom_category_slug", "") == cat_slug
            or p.get("category", "") == cat_slug
        ]

        products_html = ""
        schema_items = []

        if not cat_products:
            products_html = """
            <div style="grid-column: 1/-1; text-align: center; padding: 60px 20px;">
                <div style="font-size: 48px; margin-bottom: 20px;">🔍</div>
                <h3 style="font-size: 20px; color: var(--ninja-dark); margin-bottom: 10px;">Buscando ofertas...</h3>
                <p style="color: var(--ninja-gray);">Nosso robô está monitorando o Mercado Livre. Novas ofertas em breve!</p>
            </div>
            """
        else:
            for i, p in enumerate(cat_products[:30]):  # Máximo 30 produtos por página
                p_name = p.get("name") or p.get("title", "Produto")
                p_price = p.get("price", 0)
                p_original = p.get("originalPrice") or p.get("original_price", 0)
                p_image = p.get("image") or p.get("thumbnail", "")
                p_link = p.get("permalink", "#")
                discount = p.get("custom_discount_pct", 0)

                if not discount and p_original and p_original > p_price:
                    discount = int(((p_original - p_price) / p_original) * 100)

                # Link de afiliado
                if "mercadolivre.com.br" in p_link and "matt_tool" not in p_link:
                    p_link = p_link + ("&" if "?" in p_link else "?") + "matt_tool=vendas0nline"

                badge_html = f'<span class="badge">↓ {discount}% OFF</span>' if discount >= 5 else ""
                old_price_html = f'<span class="old-price">De R$ {p_original:.2f}</span>' if p_original and p_original > p_price else ""
                installments = int(p_price / 12) if p_price >= 120 else 0
                installments_html = f'<div class="price-installments">ou 12x de R$ {installments:.0f}</div>' if installments else ""

                # Calcular economia
                savings = int(p_original - p_price) if p_original and p_original > p_price else 0
                savings_html = f'<div class="savings">💰 Economize R$ {savings:.0f}</div>' if savings > 0 else ""
                
                products_html += f"""
                <div class="card" itemscope itemtype="https://schema.org/Product">
                    {badge_html}
                    <div class="card-img-wrap">
                        <img src="{p_image}" alt="{p_name}" loading="lazy" itemprop="image">
                    </div>
                    <div class="card-info">
                        <span class="category-tag">{cat_name.upper()}</span>
                        <h3 class="card-title" itemprop="name">{p_name[:80]}</h3>
                        {savings_html}
                        <div class="price-wrap" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                            {old_price_html}
                            <div class="price" itemprop="price" content="{p_price:.2f}">R$ {p_price:.2f}</div>
                            <meta itemprop="priceCurrency" content="BRL">
                            <meta itemprop="availability" content="https://schema.org/InStock">
                            {installments_html}
                        </div>
                        <a href="{p_link}" class="btn" target="_blank" rel="nofollow sponsored" itemprop="url">
                            🛒 Ver Oferta
                        </a>
                    </div>
                </div>
                """

                # Schema.org para o produto
                schema_items.append(f'{{"@type":"ListItem","position":{i+1},"name":"{p_name[:60]}","url":"{p_link}"}}')

        # Schema items JSON
        schema_json = "[" + ",".join(schema_items) + "]" if schema_items else "[]"

        # Guia de compra da categoria
        buying_guide = BUYING_GUIDES.get(cat_slug, "")

        # Descrição da categoria
        cat_description = CATEGORY_DESCRIPTIONS.get(cat_slug, f"As melhores ofertas de {cat_name} encontradas pelo Radar Ninja no Mercado Livre.")

        # Montar conteúdo
        content = template
        content = content.replace("{{category.name}}", cat_name)
        content = content.replace("{{category.products}}", products_html)
        content = content.replace("{{category.description}}", cat_description)
        content = content.replace("{{category.count}}", str(len(cat_products)))
        content = content.replace("{{schema.items}}", schema_json)
        content = content.replace("{{seo.title}}", f"Melhores Ofertas de {cat_name} em 2026 | Radar Ninja")
        content = content.replace("{{meta.description}}", f"Confira as melhores ofertas de {cat_name} com preços verificados pelo Radar Ninja. {cat_description[:100]}")
        content = content.replace("{{canonical.url}}", f"https://superninjas.github.io/categorias/{cat_slug}/")
        content = content.replace("{{buying_guide}}", buying_guide)

        # Salvar arquivo
        out_dir = ROOT / f"categorias/{cat_slug}"
        out_dir.mkdir(parents=True, exist_ok=True)
        with open(out_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Categoria '{cat_name}' gerada com {len(cat_products)} produtos.")

    print("✅ Todas as categorias geradas com sucesso!")

if __name__ == "__main__":
    generate_categories()
