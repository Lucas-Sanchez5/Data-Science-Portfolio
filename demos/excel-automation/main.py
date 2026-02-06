"""
Excel Automation - Demo Freelance
Limpia y transforma datos crudos del scraper
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os
import re


class ExcelAutomation:
    def __init__(self, input_file):
        self.input_file = input_file
        self.df = None
        self.reporte = []
        self.eliminados = []  # Para log de duplicados
        
    def cargar_datos(self):
        """Carga CSV del scraper"""
        try:
            self.df = pd.read_csv(self.input_file)
            self.reporte.append(f"✓ CSV cargado: {len(self.df)} registros")
            return True
        except Exception as e:
            self.reporte.append(f"✗ Error cargando CSV: {e}")
            return False
    
    def limpieza_basica(self):
        """Limpieza conservadora - elimina solo duplicados exactos por link"""
        if self.df is None:
            return
        
        # 1. Eliminar filas COMPLETAMENTE vacías
        filas_antes = len(self.df)
        self.df.dropna(how='all', inplace=True)
        filas_despues = len(self.df)
        
        if filas_antes != filas_despues:
            self.reporte.append(f"✓ Eliminadas {filas_antes - filas_despues} filas vacías")
        
        # 2. Eliminar duplicados por LINK (mismo producto, no mismo título/precio)
        dup_antes = len(self.df)
        
        # Guardar cuáles se eliminaron para log
        duplicados = self.df[self.df.duplicated(subset=['link'], keep=False)]
        if not duplicados.empty:
            self.eliminados = duplicados[['titulo', 'precio_crudo', 'link']].to_dict('records')
        
        self.df.drop_duplicates(subset=['link'], keep='first', inplace=True)
        dup_despues = len(self.df)
        
        eliminados_count = dup_antes - dup_despues
        if eliminados_count > 0:
            self.reporte.append(f"✓ Eliminados {eliminados_count} duplicados por link idéntico")
        else:
            self.reporte.append(f"✓ Sin duplicados por link")
        
        # 3. Limpiar espacios en texto
        for col in self.df.select_dtypes(include=['object']).columns:
            self.df[col] = self.df[col].str.strip()
        
        self.reporte.append(f"✓ Limpieza de espacios completada")
        self.reporte.append(f"✓ Total final: {len(self.df)} registros únicos")
    
    def estandarizar_precios(self, columna_precio='precio_crudo'):
        """Conversión robusta de precios argentinos a números"""
        if columna_precio not in self.df.columns:
            self.reporte.append(f"⚠ Columna '{columna_precio}' no encontrada")
            return
        
        nueva_col = 'precio_numero'
        
        def convertir_precio(valor):
            """Convierte string argentino a float"""
            if pd.isna(valor) or valor == "":
                return None
            
            try:
                limpio = str(valor).strip()
                
                # Caso 1: Ya es número
                if isinstance(valor, (int, float)):
                    return float(valor)
                
                # Caso 2: Textos especiales
                if limpio.lower() in ['', 'n/a', 'consultar', 'sin precio', 'gratis']:
                    return None
                
                # Caso 3: Eliminar símbolos de moneda y espacios
                limpio = re.sub(r'[^\d.,]', '', limpio)
                
                if not limpio:
                    return None
                
                puntos = limpio.count('.')
                comas = limpio.count(',')
                
                # Formato argentino: "1.234.567,89" (puntos miles, coma decimal)
                if puntos > 0 and comas > 0:
                    parte_entera, parte_decimal = limpio.rsplit(',', 1)
                    parte_entera = parte_entera.replace('.', '')
                    return float(f"{parte_entera}.{parte_decimal}")
                
                # Solo puntos: "1.234.567" (separador de miles)
                elif puntos > 0 and comas == 0:
                    # Verificar si es formato miles (grupos de 3)
                    partes = limpio.split('.')
                    if all(len(p) == 3 for p in partes[1:]) or len(partes) > 1:
                        return float(limpio.replace('.', ''))
                    else:
                        # Punto decimal
                        return float(limpio)
                
                # Solo comas: decimal
                elif comas > 0 and puntos == 0:
                    return float(limpio.replace(',', '.'))
                
                # Sin separadores
                else:
                    return float(limpio)
                    
            except:
                return None
        
        # Aplicar conversión
        self.df[nueva_col] = self.df[columna_precio].apply(convertir_precio)
        
        # Reporte
        convertidos = self.df[nueva_col].notna().sum()
        nulos = self.df[nueva_col].isna().sum()
        total = len(self.df)
        
        self.reporte.append(f"✓ Precios convertidos: {convertidos}/{total} ({convertidos/total*100:.1f}%)")
        
        if nulos > 0:
            # Mostrar ejemplos de precios que no se pudieron convertir
            ejemplos_nulos = self.df[self.df[nueva_col].isna()][columna_precio].unique()[:3]
            self.reporte.append(f"⚠ No convertidos: {nulos} (ej: {list(ejemplos_nulos)})")
    
    def crear_resumen(self):
        """Genera estadísticas del procesamiento"""
        resumen = {
            'Total registros': len(self.df),
            'Registros con precio válido': self.df['precio_numero'].notna().sum(),
            'Registros sin precio': self.df['precio_numero'].isna().sum(),
            'Precio promedio': self.df['precio_numero'].mean() if 'precio_numero' in self.df.columns else None,
            'Precio mínimo': self.df['precio_numero'].min() if 'precio_numero' in self.df.columns else None,
            'Precio máximo': self.df['precio_numero'].max() if 'precio_numero' in self.df.columns else None,
            'Fecha procesamiento': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        
        # Estadísticas detalladas
        stats = self.df['precio_numero'].describe() if 'precio_numero' in self.df.columns else pd.Series()
        
        return resumen, stats
    
    def exportar(self, output_name="datos_procesados"):
        """Exporta a Excel con múltiples hojas"""
        if self.df is None:
            print("No hay datos para exportar")
            return
        
        excel_file = f"{output_name}.xlsx"
        
        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
            # Hoja 1: Todos los datos, incluyendo precios crudos y convertidos
            self.df.to_excel(writer, sheet_name='Datos Completos', index=False)
            
            # Hoja 2: Solo registros con precio válido (por si alguna publicidad se descargó sin el precio o con formato no convertible)
            df_validos = self.df[self.df['precio_numero'].notna()].copy()
            df_validos.to_excel(writer, sheet_name='Precios Válidos', index=False)
            
            # Hoja 3: Resumen ejecutivo
            resumen, stats = self.crear_resumen()
            df_resumen = pd.DataFrame([
                {'Métrica': k, 'Valor': f"{v:,.2f}" if isinstance(v, float) else str(v)}
                for k, v in resumen.items()
            ])
            df_resumen.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hoja 4: Estadísticas descriptivas
            if not stats.empty:
                stats_df = stats.to_frame(name='Valor')
                stats_df.to_excel(writer, sheet_name='Estadísticas')
            
            # Hoja 5: Log de duplicados eliminados, solamente si hay registros eliminados
            if self.eliminados:
                df_dup = pd.DataFrame(self.eliminados)
                df_dup.to_excel(writer, sheet_name='Duplicados Eliminados', index=False)
        
        # Reporte final
        print(f"\n💾 Archivo generado: {excel_file}")
        print(f"\n📋 REPORTE DE PROCESAMIENTO:")
        print("-" * 50)
        for item in self.reporte:
            print(f"  {item}")
        
        print(f"\n📊 HOJAS EN EXCEL:")
        print(f"  1. Datos Completos ({len(self.df)} registros)")
        print(f"  2. Precios Válidos ({len(df_validos)} registros)")
        print(f"  3. Resumen Ejecutivo")
        print(f"  4. Estadísticas Descriptivas")
        if self.eliminados:
            print(f"  5. Duplicados Eliminados ({len(self.eliminados)} registros)")
        
        return excel_file


def main():
    """Ejecución principal"""
    print("🚀 EXCEL AUTOMATION - Demo Freelance")
    print("-" * 50)
    
    input_file = "../mercadolibre-scraper/mercadolibre_raw.csv"
    
    if not os.path.exists(input_file):
        print(f"✗ Archivo no encontrado: {input_file}")
        print("→ Ejecutá primero: python ../mercadolibre-scraper/main.py")
        return
    
    auto = ExcelAutomation(input_file)
    
    if auto.cargar_datos():
        auto.limpieza_basica()
        auto.estandarizar_precios('precio_crudo')
        auto.exportar("celulares_procesados")
        print(f"\n✅ Proceso completado exitosamente")
    else:
        print(f"\n✗ No se pudo completar el proceso")


if __name__ == "__main__":
    main()