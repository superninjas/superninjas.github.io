import json
import os
from datetime import datetime

def generate_article_html(idea):
    title = idea["titulo"]
    category = idea["categoria"]
    content_type = idea["tipo_conteudo"]
    keyword = idea["palavra_chave_alvo"]

    # Generate a slug from the title
    slug = title.lower().replace(" ", "-").replace("r$-x", "preco").replace("r$", "").replace("-", " ").strip().replace(" ", "-")
    
    # Basic content structure
    html_content = f"""
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Radar Ninja</title>
    <meta name="description" content="Descubra tudo sobre {title} no Radar Ninja. Análises, comparativos e as melhores ofertas para você economizar.">
    <meta name="keywords" content="{keyword}, {category}, {content_type}, Radar Ninja, ofertas, economia, comprar, melhor preço">
    
    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://superninjas.github.io/{content_type.lower().replace(' ', '-')}/{slug}/">
    <meta property="og:title" content="{title} - Radar Ninja">
    <meta property="og:description" content="Descubra tudo sobre {title} no Radar Ninja. Análises, comparativos e as melhores ofertas para você economizar.">
    <meta property="og:image" content="https://superninjas.github.io/assets/images/radar-ninja-logo.png"> <!-- Placeholder image -->

    <!-- Twitter -->
    <meta property="twitter:card" content="summary_large_image">
    <meta property="twitter:url" content="https://superninjas.github.io/{content_type.lower().replace(' ', '-')}/{slug}/">
    <meta property="twitter:title" content="{title} - Radar Ninja">
    <meta property="twitter:description" content="Descubra tudo sobre {title} no Radar Ninja. Análises, comparativos e as melhores ofertas para você economizar.">
    <meta property="twitter:image" content="https://superninjas.github.io/assets/images/radar-ninja-logo.png"> <!-- Placeholder image -->

    <link rel="stylesheet" href="/assets/css/style.css">
    <link rel="icon" href="/assets/images/favicon.ico">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{title}",
      "image": [
        "https://superninjas.github.io/assets/images/radar-ninja-logo.png"
       ],
      "datePublished": "{datetime.now().isoformat()}",
      "dateModified": "{datetime.now().isoformat()}",
      "author": [{{
        "@type": "Person",
        "name": "Manus AI",
        "url": "https://manus.im"
      }}],
      "publisher": {{
        "@type": "Organization",
        "name": "Radar Ninja",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://superninjas.github.io/assets/images/radar-ninja-logo.png"
        }}
      }},
      "description": "Descubra tudo sobre {title} no Radar Ninja. Análises, comparativos e as melhores ofertas para você economizar.",
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "https://superninjas.github.io/{content_type.lower().replace(' ', '-')}/{slug}/"
      }},
      "articleBody": "Este é um artigo detalhado sobre {title}, abordando os principais pontos e ajudando você a tomar a melhor decisão de compra. Fique atento às nossas dicas e análises para economizar de verdade."
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [{{
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": "https://superninjas.github.io/"
      }},{{
        "@type": "ListItem",
        "position": 2,
        "name": "{content_type}",
        "item": "https://superninjas.github.io/{content_type.lower().replace(' ', '-')}/"
      }},{{
        "@type": "ListItem",
        "position": 3,
        "name": "{title}",
        "item": "https://superninjas.github.io/{content_type.lower().replace(' ', '-')}/{slug}/"
      }}]
    }}
    </script>
</head>
<body>
    <header>
        <nav>
            <a href="/">Home</a>
            <a href="/ofertas/">Ofertas do Dia</a>
            <a href="/alertas/">Alertas de Preço</a>
            <a href="/comparativos/">Comparativos Rápidos</a>
            <a href="/guias/">Guias Ninja</a>
            <a href="/rankings/">Rankings</a>
            <a href="/dicas/">Dicas de Economia</a>
            <a href="/sobre/">Sobre Nós</a>
        </nav>
    </header>
    <main>
        <article>
            <h1>{title}</h1>
            <p>Publicado em: {datetime.now().strftime("%d/%m/%Y")}</p>
            
            <h2>Introdução</h2>
            <p>Bem-vindo ao Radar Ninja! Neste artigo, vamos explorar em detalhes o tema: <strong>{title}</strong>. Nosso objetivo é fornecer informações valiosas para que você faça as melhores escolhas e economize de verdade.</p>
            
            <h2>O que você vai aprender</h2>
            <ul>
                <li>Análise aprofundada sobre {title}</li>
                <li>Dicas essenciais para sua decisão de compra</li>
                <li>Como encontrar as melhores ofertas</li>
            </ul>

            <h2>Análise Detalhada sobre {title}</h2>
            <p>Aqui, mergulhamos nos aspectos mais importantes de {title}. Consideramos as especificações, o desempenho, o custo-benefício e as opiniões de especialistas e usuários para trazer uma visão completa.</p>
            
            <h3>Aspectos a Considerar</h3>
            <p>Ao pensar em {title}, é crucial avaliar:</p>
            <ul>
                <li><strong>Funcionalidades:</strong> O que ele oferece?</li>
                <li><strong>Preço:</strong> Está dentro do seu orçamento?</li>
                <li><strong>Durabilidade:</strong> É um bom investimento a longo prazo?</li>
                <li><strong>Avaliações:</strong> O que outros consumidores dizem?</li>
            </ul>

            <h2>Conclusão e Recomendação</h2>
            <p>Após uma análise cuidadosa, o Radar Ninja recomenda que você considere {title} se busca [benefício principal]. Lembre-se de sempre comparar preços e ficar atento às nossas ofertas!</p>

            <div class="cta-box">
                <h3>🔥 Não perca as melhores ofertas!</h3>
                <p>Clique aqui para ver as ofertas mais recentes de {category} no Mercado Livre!</p>
                <a href="https://www.mercadolivre.com.br/ofertas?matt_tool=vendas0nline" class="cta-button">Ver Ofertas Agora!</a>
            </div>

            <h2>Perguntas Frequentes (FAQ)</h2>
            <div class="faq">
                <details>
                    <summary>O que é {title}?</summary>
                    <p>{title} é um tópico relevante no universo de {category}, que aborda [breve explicação].</p>
                </details>
                <details>
                    <summary>Como o Radar Ninja me ajuda a economizar em {title}?</summary>
                    <p>Nós fornecemos análises detalhadas, comparativos e alertas de preço para garantir que você faça a melhor compra possível, evitando gastos desnecessários.</p>
                </details>
                <details>
                    <summary>Onde posso encontrar as melhores ofertas de {category}?</summary>
                    <p>Fique de olho em nossa seção de <a href="/ofertas/">Ofertas do Dia</a> e <a href="/alertas/">Alertas de Preço</a> para não perder nenhuma oportunidade!</p>
                </details>
            </div>
        </article>
    </main>
    <footer>
        <p>&copy; {datetime.now().year} Radar Ninja. Todos os direitos reservados.</p>
        <nav>
            <a href="/politica-de-privacidade/">Política de Privacidade</a>
            <a href="/termos-de-uso/">Termos de Uso</a>
            <a href="/contato/">Contato</a>
        </nav>
    </footer>
</body>
</html>
"""
    return html_content

def generate_articles_from_calendar(calendar_file, output_base_dir, limit_month=None):
    with open(calendar_file, 'r', encoding='utf-8') as f:
        calendar_data = json.load(f)

    generated_count = 0

    for month, ideas_list in calendar_data.items():
        if limit_month and month != limit_month:
            continue

        for idea in ideas_list:
            content_type_folder = idea["tipo_conteudo"].lower().replace(" ", "-")
            slug = idea["titulo"].lower().replace(" ", "-").replace("r$-x", "preco").replace("r$", "").replace("-", " ").strip().replace(" ", "-")
            
            # Ensure the slug is valid for a URL (no special chars)
            slug = ''.join(c for c in slug if c.isalnum() or c == '-')

            output_dir = os.path.join(output_base_dir, content_type_folder, slug)
            os.makedirs(output_dir, exist_ok=True)

            file_path = os.path.join(output_dir, "index.html")
            html_content = generate_article_html(idea)

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            generated_count += 1
            print(f"Generated: {file_path}")
    print(f"Total articles generated: {generated_count}")

if __name__ == "__main__":
    # Generate articles for the first month (July 2026)
    generate_articles_from_calendar('calendario_editorial.json', '../')
