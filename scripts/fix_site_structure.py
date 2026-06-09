import os
from bs4 import BeautifulSoup

def fix_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # 1. Fix Duplicated Branding in Title
    if soup.title:
        title_text = soup.title.string
        if title_text and "| Radar Ninja | Radar Ninja" in title_text:
            soup.title.string = title_text.replace("| Radar Ninja | Radar Ninja", "| Radar Ninja")
        elif title_text and title_text.count("| Radar Ninja") > 1:
            parts = title_text.split("| Radar Ninja")
            soup.title.string = parts[0].strip() + " | Radar Ninja"

    # 2. Fix Header Menu Links
    # Standardize to the new portal structure
    nav = soup.find('nav')
    if nav:
        for a in nav.find_all('a', href=True):
            href = a['href']
            # Remove legacy category links
            if '/categorias/' in href:
                if 'celular' in href: a['href'] = '/guias/'
                elif 'games' in href: a['href'] = '/comparativos/'
                else: a['href'] = '/'
            
            # Fix section links
            if href == '/guias-ninja/': a['href'] = '/guias/'
            if href == '/alertas-de-compra/': a['href'] = '/alertas/'
            if href == '/economia/': a['href'] = '/dicas/'

    # 3. Fix Breadcrumbs in JSON-LD
    scripts = soup.find_all('script', type='application/ld+json')
    for script in scripts:
        try:
            import json
            data = json.loads(script.string)
            if data.get('@type') == 'BreadcrumbList':
                for item in data.get('itemListElement', []):
                    item_url = item.get('item')
                    if item_url:
                        # Clean up malformed URLs in schema
                        new_url = item_url.replace(':', '').replace('?', '').replace('$', '').replace(' ', '-')
                        item['item'] = new_url
            script.string = json.dumps(data, ensure_ascii=False, indent=2)
        except:
            pass

    # 4. Remove placeholders like R$ X
    for element in soup.find_all(string=True):
        if 'R$ X' in element:
            new_text = element.replace('R$ X', 'preços competitivos')
            element.replace_with(new_text)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

def process_directory(base_path):
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Fixing: {file_path}")
                fix_html_file(file_path)

if __name__ == "__main__":
    process_directory('/home/ubuntu/superninjas.github.io')
