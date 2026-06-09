import os
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://superninjas.github.io"
TODAY = datetime.now().strftime("%Y-%m-%d")

def generate_sitemap():
    print("🗺️ Gerando sitemap.xml...")

    urls = []

    # Homepage
    urls.append({"loc": f"{BASE_URL}/", "lastmod": TODAY, "changefreq": "hourly", "priority": "1.0"})

    # Blog index
    urls.append({"loc": f"{BASE_URL}/noticias/", "lastmod": TODAY, "changefreq": "daily", "priority": "0.8"})

    # Páginas estáticas
    for page, freq, priority in [("sobre","monthly","0.5"),("contato","monthly","0.5"),("privacidade","yearly","0.3"),("termos","yearly","0.3")]:
        if (ROOT / page / "index.html").exists():
            urls.append({"loc": f"{BASE_URL}/{page}/", "lastmod": TODAY, "changefreq": freq, "priority": priority})

    # Guias
    guias_dir = ROOT / "guias"
    if guias_dir.exists():
        if (guias_dir / "index.html").exists():
            urls.append({"loc": f"{BASE_URL}/guias/", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.8"})
        for d in guias_dir.iterdir():
            if d.is_dir() and (d / "index.html").exists():
                urls.append({"loc": f"{BASE_URL}/guias/{d.name}/", "lastmod": TODAY, "changefreq": "monthly", "priority": "0.8"})

    # Comparativos
    comp_dir = ROOT / "comparativos"
    if comp_dir.exists():
        if (comp_dir / "index.html").exists():
            urls.append({"loc": f"{BASE_URL}/comparativos/", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.7"})
        for d in comp_dir.iterdir():
            if d.is_dir() and (d / "index.html").exists():
                urls.append({"loc": f"{BASE_URL}/comparativos/{d.name}/", "lastmod": TODAY, "changefreq": "monthly", "priority": "0.8"})

    # Categorias
    cats_dir = ROOT / "categorias"
    if cats_dir.exists():
        for d in cats_dir.iterdir():
            if d.is_dir() and (d / "index.html").exists():
                urls.append({"loc": f"{BASE_URL}/categorias/{d.name}/", "lastmod": TODAY, "changefreq": "hourly", "priority": "0.9"})

    # Posts do blog
    noticias_dir = ROOT / "noticias"
    if noticias_dir.exists():
        for post_file in noticias_dir.glob("*.html"):
            if post_file.name != "index.html":
                slug = post_file.stem
                img_url = None
                try:
                    content = post_file.read_text(encoding="utf-8")
                    m = re.search(r'<img[^>]+src=["\']([^"\']+)["\']', content)
                    if m:
                        img_url = m.group(1)
                except Exception:
                    pass
                entry = {"loc": f"{BASE_URL}/noticias/{slug}/", "lastmod": TODAY, "changefreq": "weekly", "priority": "0.7"}
                if img_url and img_url.startswith("http"):
                    entry["image"] = img_url
                    entry["image_title"] = slug.replace("-", " ").title()
                urls.append(entry)

    # Gerar XML
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ]
    for u in urls:
        lines.append("  <url>")
        lines.append(f"    <loc>{u['loc']}</loc>")
        lines.append(f"    <lastmod>{u['lastmod']}</lastmod>")
        lines.append(f"    <changefreq>{u.get('changefreq','weekly')}</changefreq>")
        lines.append(f"    <priority>{u['priority']}</priority>")
        if "image" in u:
            lines.append("    <image:image>")
            lines.append(f"      <image:loc>{u['image']}</image:loc>")
            lines.append(f"      <image:title>{u.get('image_title','')}</image:title>")
            lines.append("    </image:image>")
        lines.append("  </url>")
    lines.append("</urlset>")

    (ROOT / "sitemap.xml").write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ Sitemap gerado com {len(urls)} URLs!")

    # robots.txt
    robots = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml

Disallow: /scripts/
Disallow: /data/
Disallow: /.github/
"""
    (ROOT / "robots.txt").write_text(robots, encoding="utf-8")
    print("✅ robots.txt gerado!")

if __name__ == "__main__":
    generate_sitemap()
