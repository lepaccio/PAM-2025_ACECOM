import os
import markdown
from pathlib import Path

def md_a_html():
    """Convierte todos los archivos MD a HTML con estilo"""
    
    # CSS para hacer los perfiles más bonitos
    css_style = """
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            max-width: 800px; 
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
        }
        h2 { 
            color: #34495e; 
            margin-top: 25px;
            margin-bottom: 10px;
            padding: 8px 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 5px;
        }
        p { 
            margin-bottom: 15px; 
            text-align: justify;
        }
        hr { 
            border: none; 
            height: 2px; 
            background: linear-gradient(to right, #3498db, #e74c3c);
            margin: 20px 0;
        }
        .nav-buttons {
            text-align: center;
            margin: 20px 0;
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
    </style>
    """
    
    carpeta_md = 'perfiles_md'
    carpeta_html = 'perfiles_html'
    
    # Crear carpeta HTML si no existe
    if not os.path.exists(carpeta_html):
        os.makedirs(carpeta_html)
        print(f"📁 Carpeta '{carpeta_html}' creada")
    
    # Obtener lista de archivos MD
    archivos_md = [f for f in os.listdir(carpeta_md) if f.endswith('.md')]
    archivos_convertidos = 0
    
    # Generar índice HTML
    html_index = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Perfiles ACECOM PAM 2025</title>
        {css_style}
    </head>
    <body>
        <div class="container">
            <h1>🎓 Perfiles de Postulantes ACECOM</h1>
            <p><strong>Total de postulantes:</strong> {len(archivos_md)}</p>
            <hr>
            <h2>📋 Lista de Perfiles</h2>
    """
    
    # Convertir cada archivo MD a HTML
    for archivo_md in sorted(archivos_md):
        nombre_sin_ext = archivo_md.replace('.md', '')
        archivo_html = f"{nombre_sin_ext}.html"
        
        try:
            # Leer archivo MD
            with open(os.path.join(carpeta_md, archivo_md), 'r', encoding='utf-8') as f:
                contenido_md = f.read()
            
            # Convertir MD a HTML
            md = markdown.Markdown(extensions=['extra'])
            contenido_html = md.convert(contenido_md)
            
            # Crear botones de navegación
            botones_nav = '<div class="nav-buttons">'
            botones_nav += '<a href="index.html" class="nav-button">🏠 Inicio</a>'
            
            # Botón anterior
            idx_actual = archivos_md.index(archivo_md)
            if idx_actual > 0:
                archivo_anterior = archivos_md[idx_actual - 1].replace('.md', '.html')
                botones_nav += f'<a href="{archivo_anterior}" class="nav-button">⬅️ Anterior</a>'
            
            # Botón siguiente
            if idx_actual < len(archivos_md) - 1:
                archivo_siguiente = archivos_md[idx_actual + 1].replace('.md', '.html')
                botones_nav += f'<a href="{archivo_siguiente}" class="nav-button">➡️ Siguiente</a>'
            
            botones_nav += '</div>'
            
            # HTML completo
            html_completo = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Perfil - {nombre_sin_ext.replace('_', ' ')}</title>
                {css_style}
            </head>
            <body>
                <div class="container">
                    {botones_nav}
                    {contenido_html}
                    {botones_nav}
                </div>
            </body>
            </html>
            """
            
            # Escribir archivo HTML
            with open(os.path.join(carpeta_html, archivo_html), 'w', encoding='utf-8') as f:
                f.write(html_completo)
            
            # Agregar al índice
            nombre_display = nombre_sin_ext.replace('_', ' ')
            html_index += f'<p>👤 <a href="{archivo_html}" class="nav-button" style="display:inline; padding:5px 10px; margin:2px;">{nombre_display}</a></p>\n'
            
            archivos_convertidos += 1
            print(f"✅ Convertido: {archivo_html}")
            
        except Exception as e:
            print(f"❌ Error al convertir {archivo_md}: {e}")
    
    # Finalizar índice
    html_index += """
            </div>
        </body>
        </html>
    """
    
    # Escribir índice
    with open(os.path.join(carpeta_html, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_index)
    
    print(f"\n🎉 ¡Conversión completada!")
    print(f"📁 Archivos HTML generados: {archivos_convertidos + 1}")
    print(f"📂 Ubicación: ./{carpeta_html}/")
    print(f"🌐 Abre 'index.html' en tu navegador para ver todos los perfiles")
    
    # Mostrar cómo abrir
    ruta_index = os.path.abspath(os.path.join(carpeta_html, 'index.html'))
    print(f"📋 Comando para abrir: firefox {ruta_index}")

if __name__ == "__main__":
    md_a_html()