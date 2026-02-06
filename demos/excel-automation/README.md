# Excel Automation - Demo Freelance

Automatización de limpieza y transformación de datos en Excel.

## 🎯 ¿Qué hace?

- **Recibe datos crudos** (ej: del scraper de MercadoLibre) y los transforma
- Elimina duplicados por link idéntico (conserva variaciones de precios entre vendedores)
- Estandariza formatos de precios argentinos ("1.234.567" → 1234567)
- Genera resumen estadístico automático (promedio, mínimo, máximo, mediana)
- Exporta múltiples hojas: datos completos, precios válidos, resumen, estadísticas

## 🔗 Integración
Este script está diseñado para procesar la salida de `mercadolibre-scraper`, pero puede adaptarse a cualquier CSV con columnas: `titulo`, `precio_crudo`, `condicion`, `link`.

## 💼 Casos de uso
- Actualización de listas de precios
- Limpieza de bases de datos de clientes
- Unificación de formatos de distintas fuentes
- Reportes mensuales automatizados

## 🚀 Uso rápido

```bash
pip install -r requirements.txt
python main.py
```

## 📫 Contacto
- **LinkedIn:** https://linkedin.com/in/lucas-sanchez-323bb1354
- **Email:** lucassanchez01234@gmail.com