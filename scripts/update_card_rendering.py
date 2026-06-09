#!/usr/bin/env python3
"""
Script para atualizar a renderização dos cards para o padrão premium (FASE 2).
Injeta a economia estimada e melhora a estrutura HTML.
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def update_generate_categories():
    """Atualizar o script de geração de categorias com novo card HTML"""
    file_path = ROOT / "scripts/generate_categories.py"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Substituir o template do card
    old_card = '''                products_html += f"""
                <div class="card" itemscope itemtype="https://schema.org/Product">
                    {badge_html}
                    <div class="card-img-wrap">
                        <img src="{p_image}" alt="{p_name}" loading="lazy" itemprop="image">
                    </div>
                    <div class="card-info">
                        <span class="category-tag">{cat_name.upper()}</span>
                        <h3 class="card-title" itemprop="name">{p_name[:80]}</h3>
                        <div class="price-wrap" itemprop="offers" itemscope itemtype="https://schema.org/Offer">
                            {old_price_html}
                            <div class="price" itemprop="price" content="{p_price:.2f}">R$ {p_price:.2f}</div>
                            <meta itemprop="priceCurrency" content="BRL">
                            <meta itemprop="availability" content="https://schema.org/InStock">
                            {installments_html}
                        </div>
                        <a href="{p_link}" class="btn" target="_blank" rel="nofollow sponsored" itemprop="url">
                            🛒 Ver Oferta no Mercado Livre
                        </a>
                    </div>
                </div>
                """'''
    
    new_card = '''                # Calcular economia
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
                """'''
    
    content = content.replace(old_card, new_card)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ generate_categories.py atualizado com novo card premium")

def update_build_homepage():
    """Atualizar o script de construção da homepage"""
    file_path = ROOT / "scripts/build_homepage.py"
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    old_card = '''            products_html += f"""
            <div class="card" itemscope itemtype="https://schema.org/Product">
                {badge_html}
                <div class="card-img-wrap">
                    <img src="{image}" alt="{title}" loading="lazy" itemprop="image">
                </div>
                <div class="card-info">
                    <h3 class="card-title" itemprop="name">{title[:80]}</h3>
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
            """'''
    
    new_card = '''            # Calcular economia
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
            """'''
    
    content = content.replace(old_card, new_card)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ build_homepage.py atualizado com novo card premium")

if __name__ == "__main__":
    update_generate_categories()
    update_build_homepage()
    print("\n✨ FASE 2: Cards premium implementados!")
