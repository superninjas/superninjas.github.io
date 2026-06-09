import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def audit_site(base_url):
    visited = set()
    to_visit = [base_url]
    errors_404 = []
    broken_links = []
    published_pages = []
    menu_errors = []

    print(f"Iniciando auditoria em {base_url}...")

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        
        visited.add(url)
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                errors_404.append(url)
                continue
            
            if response.status_code == 200:
                published_pages.append(url)
                
                # Analyze content
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Check links
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(url, href)
                    
                    # Check if it's an internal link
                    if urlparse(full_url).netloc == urlparse(base_url).netloc:
                        if full_url not in visited and full_url not in to_visit:
                            to_visit.append(full_url)
                    
                    # Verify if the link is broken (optional, can be slow)
                    # For this audit, we'll focus on internal navigation
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")

    # Specific check for menus and breadcrumbs would require DOM analysis
    # Let's return the findings
    return {
        "total_visited": len(visited),
        "errors_404": errors_404,
        "published_pages": published_pages,
        "total_404": len(errors_404),
        "total_published": len(published_pages)
    }

if __name__ == "__main__":
    base_url = "https://superninjas.github.io"
    results = audit_site(base_url)
    print(json.dumps(results, indent=2, ensure_ascii=False))
