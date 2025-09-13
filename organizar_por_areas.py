import pandas as pd
import os
import shutil
from collections import defaultdict

def organizar_por_areas():
    """Organiza los perfiles HTML y MD por área principal de interés"""
    
    # Leer el CSV para obtener las áreas de interés
    archivo_csv = 'PAM 2025_2.csv'
    try:
        df = pd.read_csv(archivo_csv, sep=';')
        print(f"✅ Archivo CSV leído correctamente. Total de registros: {len(df)}")
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_csv}'.")
        return

    # Limpiar datos
    columna_nombres = 'Nombres:\n'
    columna_area = '¿A qué área de ACECOM te gustaría postular? Principal interes.\n'
    
    df_limpio = df.dropna(subset=[columna_nombres, columna_area])
    df_limpio = df_limpio[df_limpio[columna_nombres].str.strip() != '']
    df_limpio = df_limpio[df_limpio[columna_nombres] != 'asdas']
    
    # Agrupar por área de interés
    areas_candidatos = defaultdict(list)
    
    for index, row in df_limpio.iterrows():
        nombre = str(row[columna_nombres]).strip()
        area = str(row[columna_area]).strip() if pd.notna(row[columna_area]) else 'Sin especificar'
        
        # Limpiar y normalizar nombres de área
        area_limpia = area.replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_')
        
        if len(nombre) >= 2 and nombre.lower() not in ['i', 'j', 'asdas']:
            nombre_archivo = nombre.replace(' ', '_').replace('/', '_').replace('\\', '_').replace('*', '_').replace('?', '_').replace('[', '_').replace(']', '_')
            areas_candidatos[area_limpia].append({
                'nombre': nombre,
                'nombre_archivo': nombre_archivo,
                'area_original': area
            })
    
    print(f"📋 Áreas encontradas: {len(areas_candidatos)}")
    for area, candidatos in areas_candidatos.items():
        print(f"   • {area}: {len(candidatos)} candidatos")
    
    # Crear estructura de carpetas por área
    carpeta_base_html = 'perfiles_por_area_html'
    carpeta_base_md = 'perfiles_por_area_md'
    
    # Limpiar carpetas existentes si existen
    for carpeta in [carpeta_base_html, carpeta_base_md]:
        if os.path.exists(carpeta):
            shutil.rmtree(carpeta)
        os.makedirs(carpeta)
    
    # Copiar archivos por área
    total_copiados_html = 0
    total_copiados_md = 0
    
    for area, candidatos in areas_candidatos.items():
        # Crear subcarpetas para cada área
        carpeta_area_html = os.path.join(carpeta_base_html, area)
        carpeta_area_md = os.path.join(carpeta_base_md, area)
        
        os.makedirs(carpeta_area_html, exist_ok=True)
        os.makedirs(carpeta_area_md, exist_ok=True)
        
        print(f"\n📁 Procesando área: {area}")
        
        for candidato in candidatos:
            nombre_archivo = candidato['nombre_archivo']
            
            # Copiar archivo HTML
            archivo_html_origen = os.path.join('perfiles_html', f"{nombre_archivo}.html")
            archivo_html_destino = os.path.join(carpeta_area_html, f"{nombre_archivo}.html")
            
            if os.path.exists(archivo_html_origen):
                shutil.copy2(archivo_html_origen, archivo_html_destino)
                total_copiados_html += 1
                print(f"  ✅ HTML: {candidato['nombre']}")
            else:
                print(f"  ❌ HTML no encontrado: {nombre_archivo}")
            
            # Copiar archivo MD
            archivo_md_origen = os.path.join('perfiles_md', f"{nombre_archivo}.md")
            archivo_md_destino = os.path.join(carpeta_area_md, f"{nombre_archivo}.md")
            
            if os.path.exists(archivo_md_origen):
                shutil.copy2(archivo_md_origen, archivo_md_destino)
                total_copiados_md += 1
            else:
                print(f"  ❌ MD no encontrado: {nombre_archivo}")
    
    # Crear índices HTML por área
    crear_indices_por_area(areas_candidatos, carpeta_base_html)
    
    # Crear índice general
    crear_indice_general(areas_candidatos, carpeta_base_html)
    
    print(f"\n🎉 ¡Organización completada!")
    print(f"📁 Archivos HTML organizados: {total_copiados_html}")
    print(f"📁 Archivos MD organizados: {total_copiados_md}")
    print(f"📂 Ubicación HTML: ./{carpeta_base_html}/")
    print(f"📂 Ubicación MD: ./{carpeta_base_md}/")
    print(f"🌐 Abre 'index_general.html' para ver la organización por áreas")

def crear_indices_por_area(areas_candidatos, carpeta_base_html):
    """Crea un índice HTML para cada área"""
    
    css_style = """
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 900px; 
            margin: 0 auto; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f8f9fa;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 10px;
            text-align: center;
        }
        h2 { 
            color: #34495e; 
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .area-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
        .candidatos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .candidato-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
            transition: transform 0.2s;
        }
        .candidato-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .nav-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px;
            background: #3498db;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav-button:hover {
            background: #2980b9;
        }
        .stats {
            background: #e8f4fd;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
    </style>
    """
    
    for area, candidatos in areas_candidatos.items():
        carpeta_area = os.path.join(carpeta_base_html, area)
        
        html_area = f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Área: {area} - ACECOM PAM 2025</title>
            {css_style}
        </head>
        <body>
            <div class="container">
                <h1>🎯 Área: {area}</h1>
                
                <div class="area-header">
                    <h2>📋 Candidatos Postulantes</h2>
                </div>
                
                <div class="stats">
                    <strong>📊 Total de candidatos en esta área: {len(candidatos)}</strong>
                </div>
                
                <div class="candidatos-grid">
        """
        
        for candidato in sorted(candidatos, key=lambda x: x['nombre']):
            nombre_display = candidato['nombre']
            nombre_archivo = candidato['nombre_archivo']
            
            html_area += f"""
                    <div class="candidato-card">
                        <h3>👤 {nombre_display}</h3>
                        <a href="{nombre_archivo}.html" class="nav-button">Ver Perfil</a>
                    </div>
            """
        
        html_area += f"""
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="../index_general.html" class="nav-button">🏠 Volver al Índice General</a>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Escribir índice del área
        with open(os.path.join(carpeta_area, 'index.html'), 'w', encoding='utf-8') as f:
            f.write(html_area)
        
        print(f"  📄 Índice creado para área: {area}")

def crear_indice_general(areas_candidatos, carpeta_base_html):
    """Crea el índice general con todas las áreas"""
    
    css_style = """
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 1000px; 
            margin: 0 auto; 
            padding: 20px; 
            line-height: 1.6;
            background-color: #f8f9fa;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 { 
            color: #2c3e50; 
            border-bottom: 3px solid #3498db; 
            padding-bottom: 10px;
            text-align: center;
        }
        .areas-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        .area-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
            transition: transform 0.3s;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .area-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }
        .area-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .area-count {
            font-size: 2em;
            font-weight: bold;
            margin: 15px 0;
        }
        .nav-button {
            display: inline-block;
            padding: 10px 20px;
            margin: 10px 5px;
            background: rgba(255,255,255,0.2);
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .nav-button:hover {
            background: rgba(255,255,255,0.3);
        }
        .stats-summary {
            background: #e8f4fd;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }
        .total-stat {
            font-size: 1.5em;
            color: #2c3e50;
            font-weight: bold;
        }
    </style>
    """
    
    total_candidatos = sum(len(candidatos) for candidatos in areas_candidatos.values())
    
    html_general = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Perfiles por Área - ACECOM PAM 2025</title>
        {css_style}
    </head>
    <body>
        <div class="container">
            <h1>🎓 Perfiles ACECOM PAM 2025 - Organizados por Área</h1>
            
            <div class="stats-summary">
                <div class="total-stat">📊 Total de Candidatos: {total_candidatos}</div>
                <div>📁 Áreas de Interés: {len(areas_candidatos)}</div>
                <div>📅 Fecha: 12 de septiembre de 2025</div>
            </div>
            
            <div class="areas-grid">
    """
    
    # Ordenar áreas por número de candidatos (descendente)
    areas_ordenadas = sorted(areas_candidatos.items(), key=lambda x: len(x[1]), reverse=True)
    
    for area, candidatos in areas_ordenadas:
        html_general += f"""
            <div class="area-card">
                <div class="area-title">🎯 {area}</div>
                <div class="area-count">{len(candidatos)}</div>
                <div>candidatos</div>
                <a href="{area}/index.html" class="nav-button">Ver Candidatos</a>
            </div>
        """
    
    html_general += """
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <h3>🔗 Enlaces adicionales</h3>
                <a href="../perfiles_html/index.html" class="nav-button" style="background: #3498db; color: white;">📋 Ver Todos los Perfiles</a>
                <a href="../resultados_ordenados.xlsx" class="nav-button" style="background: #27ae60; color: white;">📊 Descargar Excel</a>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Escribir índice general
    with open(os.path.join(carpeta_base_html, 'index_general.html'), 'w', encoding='utf-8') as f:
        f.write(html_general)
    
    print(f"📄 Índice general creado")

if __name__ == "__main__":
    organizar_por_areas()