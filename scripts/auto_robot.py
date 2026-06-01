import subprocess
import os
import sys

def run_script(script_name):
    print(f"🚀 Iniciando: {script_name}")
    try:
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✅ Finalizado: {script_name}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {script_name}:")
        print(e.stderr)
        # Não interrompe o processo total se um script falhar, a menos que seja crítico
        if script_name in ["fetch_products.py", "sanitize_offers.py"]:
            sys.exit(1)

def main():
    scripts = [
        "fetch_products.py",
        "sanitize_offers.py",
        "generate_categories.py",
        "build_homepage.py",
        "generate_deep_blog.py",
        "generate_legal_pages.py",
        "generate_sitemap.py"
    ]
    
    for script in scripts:
        run_script(script)
    
    print("🎯 Processo completo do Super Ninja finalizado!")

if __name__ == "__main__":
    main()
