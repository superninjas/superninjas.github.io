import json
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
products = json.loads((ROOT / "data/products/offers.json").read_text(encoding="utf-8"))

summary = {
    "produtos": len(products),
    "links_afiliado_em_json": 0,
    "imagens_validas_json": 0,
    "links_produto_validos_json": 0,
    "ctas_homepage": 0,
    "fotos_homepage": 0,
    "precos_homepage": 0,
    "erros": [],
}

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 RadarNinjaAudit/1.0"})

def ok_url(url):
    try:
        r = session.get(url, timeout=12, allow_redirects=True, stream=True)
        status = r.status_code
        ctype = r.headers.get("content-type", "")
        r.close()
        return status < 400, status, ctype
    except Exception as exc:
        return False, str(exc), ""

for p in products:
    link = p.get("permalink", "")
    img = p.get("thumbnail") or p.get("image") or ""
    if "mercadolivre.com.br" in link and "matt_tool=60566305" in link:
        summary["links_afiliado_em_json"] += 1
    else:
        summary["erros"].append({"tipo": "link_afiliado_ausente", "produto": p.get("title"), "url": link})
    valid_link, status, _ = ok_url(link)
    if valid_link:
        summary["links_produto_validos_json"] += 1
    else:
        summary["erros"].append({"tipo": "link_produto_invalido", "produto": p.get("title"), "status": status, "url": link})
    valid_img, img_status, ctype = ok_url(img)
    if valid_img and "image" in ctype:
        summary["imagens_validas_json"] += 1
    else:
        summary["erros"].append({"tipo": "imagem_invalida", "produto": p.get("title"), "status": img_status, "content_type": ctype, "url": img})

html = (ROOT / "index.html").read_text(encoding="utf-8")
soup = BeautifulSoup(html, "html.parser")
summary["ctas_homepage"] = len([a for a in soup.find_all("a", href=True) if "Ver Oferta Ninja" in a.get_text(" ", strip=True)])
summary["fotos_homepage"] = len(soup.select(".card-img-wrap img"))
summary["precos_homepage"] = html.count('itemprop="price"')
summary["links_afiliado_homepage"] = len([a for a in soup.find_all("a", href=True) if "mercadolivre.com.br" in a["href"] and "matt_tool=60566305" in a["href"]])

(ROOT / "validacao_radar_comercial.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(summary, ensure_ascii=False, indent=2))
