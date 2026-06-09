import os
import sys
import subprocess
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('self_healing')

def run_script(script):
    try:
        logger.info(f"🚀 Iniciando {script}...")
        result = subprocess.run([sys.executable, f"scripts/{script}"], capture_output=True, text=True)
        if result.returncode == 0:
            return True
        else:
            logger.error(f"❌ Erro em {script}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"⚠️ Falha ao rodar {script}: {str(e)}")
        return False

def main():
    scripts = [
        "fetch_products.py",
        "sanitize_offers.py",
        "generate_categories.py",
        "build_homepage.py",
        "generate_deep_blog.py",
        "generate_sitemap.py"
    ]
    for s in scripts:
        if os.path.exists(f"scripts/{s}"):
            run_script(s)

if __name__ == "__main__":
    main()
