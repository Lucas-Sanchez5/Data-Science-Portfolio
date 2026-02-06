"""
MercadoLibre Scraper - Demo Freelance
Extrae datos CRUDOS sin procesar para demostrar capacidad de limpieza posterior
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime


class MercadoLibreScraper:
    def __init__(self):
        self.base_url = "https://listado.mercadolibre.com.ar"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.0'
        }
        self.datos = []
    
    def construir_url(self, busqueda, pagina=1):
        """Construye URL de búsqueda"""
        query = busqueda.replace(" ", "-")
        if pagina == 1:
            return f"{self.base_url}/{query}"
        else:
            return f"{self.base_url}/{query}_Desde_{(pagina-1)*50+1}"
    
    def scrapear_pagina(self, url):
        """Extrae datos CRUDOS de una página"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            items = soup.find_all('li', class_='ui-search-layout__item')
            if not items:
                items = soup.find_all('div', class_='poly-card')
            
            resultados = []
            
            for item in items:
                try:
                    # Título crudo
                    titulo_tag = item.find('a', class_='poly-component__title') or \
                                item.find('h2', class_='ui-search-item__title') or \
                                item.find('a', {'title': True})
                    titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""
                    
                    # Precio crudo igual al que aparece en la web 
                    precio_tag = item.find('span', class_='andes-money-amount__fraction') or \
                                item.find('span', class_='price-tag-fraction')
                    precio_crudo = precio_tag.get_text(strip=True) if precio_tag else ""
                    
                    # Link
                    link_tag = item.find('a', href=True)
                    link = link_tag['href'] if link_tag else ""
                    
                    # Condición (ejemplos: nuevo, usado, etc.)
                    condicion_tag = item.find('span', class_='poly-component__item-condition') or \
                                   item.find('span', class_='ui-search-item__condition')
                    condicion = condicion_tag.get_text(strip=True) if condicion_tag else ""
                    
                    resultados.append({
                        'titulo': titulo,
                        'precio_crudo': precio_crudo,  
                        'condicion': condicion,
                        'link': link,
                        'fecha_extraccion': datetime.now().strftime('%Y-%m-%d %H:%M')
                    })
                    
                except Exception as e:
                    continue
            
            print(f"✓ Extraídos {len(resultados)} productos")
            return resultados
            
        except Exception as e:
            print(f"✗ Error: {e}")
            return []
    
    def scrapear_busqueda(self, busqueda, max_paginas=2):
        """Scrapea múltiples páginas"""
        print(f"\n🔍 Buscando: '{busqueda}'")
        print(f"📄 Páginas: {max_paginas}")
        print("-" * 50)
        
        for pagina in range(1, max_paginas + 1):
            url = self.construir_url(busqueda, pagina)
            resultados = self.scrapear_pagina(url)
            
            if not resultados:
                break
                
            self.datos.extend(resultados)
            
            if pagina < max_paginas:
                time.sleep(2)
        
        print(f"\n✅ Total: {len(self.datos)} productos")
        return self.datos
    
    def guardar_csv(self, nombre_archivo="mercadolibre_raw"):
        """Guarda CSV CRUDO (sin Excel, sin procesar)"""
        if not self.datos:
            print("⚠ No hay datos")
            return
        
        csv_file = f"{nombre_archivo}.csv"
        
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=['titulo', 'precio_crudo', 'condicion', 'link', 'fecha_extraccion'])
            writer.writeheader()
            writer.writerows(self.datos)
        
        print(f"💾 CSV crudo guardado: {csv_file}")
        print(f"   Registros: {len(self.datos)}")
        
        print(f"\n📊 Muestra de precios crudos extraídos:")
        for i, item in enumerate(self.datos[:5], 1):
            print(f"   {i}. '{item['precio_crudo']}'")


def main():
    scraper = MercadoLibreScraper()
    scraper.scrapear_busqueda("celular samsung", max_paginas=2)
    scraper.guardar_csv("mercadolibre_raw")
    print(f"\n🎯 Ahora ejecutá: python ../excel-automation/main.py")


if __name__ == "__main__":
    main()