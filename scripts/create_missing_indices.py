import os

sections = {
    "ofertas": "Ofertas do Dia",
    "rankings": "Rankings de Produtos",
    "dicas": "Dicas de Economia",
    "alertas": "Alertas de Preço",
    "guias": "Guias Ninja"
}

template = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Radar Ninja</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body class="bg-gray-50 text-gray-900 font-sans">
    <header class="bg-white shadow-sm">
        <nav class="container mx-auto px-4 py-4 flex justify-between items-center">
            <a href="/" class="text-2xl font-extrabold text-red-600">🥷 Radar Ninja</a>
            <div class="space-x-6 font-semibold">
                <a href="/ofertas/" class="hover:text-red-600">Ofertas</a>
                <a href="/comparativos/" class="hover:text-red-600">Comparativos</a>
                <a href="/guias/" class="hover:text-red-600">Guias</a>
                <a href="/rankings/" class="hover:text-red-600">Rankings</a>
                <a href="/dicas/" class="hover:text-red-600">Economia</a>
            </div>
        </nav>
    </header>
    <main class="container mx-auto px-4 py-12">
        <h1 class="text-4xl font-bold mb-8">{title}</h1>
        <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="content-grid">
            <!-- Conteúdo será listado aqui -->
            <p class="text-gray-600">Explore nossos artigos e análises sobre {title} para economizar de verdade.</p>
        </div>
    </main>
    <footer class="bg-gray-900 text-white py-12 mt-12">
        <div class="container mx-auto px-4 text-center">
            <p>© 2026 Radar Ninja. Inteligência para suas compras.</p>
        </div>
    </footer>
</body>
</html>
"""

def create_indices():
    for folder, title in sections.items():
        path = f"/home/ubuntu/superninjas.github.io/{folder}"
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, "index.html")
        
        # Simple check: if index doesn't exist or is small, create/overwrite
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(template.format(title=title))
        print(f"Created/Updated index for: {folder}")

if __name__ == "__main__":
    create_indices()
