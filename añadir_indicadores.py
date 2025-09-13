import os
import re

def añadir_indicadores_disponibilidad():
    """Añade círculos de colores según la disponibilidad de tiempo de cada candidato"""
    
    # Clasificación de candidatos según su respuesta sobre compromiso
    candidatos_con_dudas = {
        'Edwin_Arles': 'Creo que sí, pero tendría que organizarme bien',
        'Dante': 'Creo que sí, pero tendría que organizarme bien', 
        'José_Emiliano': 'Creo que sí, pero tendría que organizarme bien',
        'Joaquin_Marcelo': 'Creo que sí, pero tendría que organizarme bien',
        'Jarem_Alexssander': 'Creo que sí, pero tendría que organizarme bien',
        'Luis_Aldair': 'Me preocupa un poco, pero estoy dispuesto/a a intentarlo'
    }
    
    # Indicadores visuales
    circulo_verde = "🟢"  # Sin problemas de tiempo
    circulo_amarillo = "🟡"  # Con dudas sobre tiempo
    
    def procesar_archivo_md(ruta_archivo, nombre_archivo):
        """Procesa un archivo Markdown añadiendo el indicador"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Determinar el indicador
            indicador = circulo_amarillo if nombre_archivo in candidatos_con_dudas else circulo_verde
            
            # Reemplazar el título principal
            patron_titulo = r'^# 👤 Perfil de (.+)$'
            nuevo_titulo = f'# {indicador} 👤 Perfil de \\1'
            contenido_modificado = re.sub(patron_titulo, nuevo_titulo, contenido, flags=re.MULTILINE)
            
            # Escribir archivo modificado
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido_modificado)
            
            return True
        except Exception as e:
            print(f"❌ Error procesando MD {nombre_archivo}: {e}")
            return False
    
    def procesar_archivo_html(ruta_archivo, nombre_archivo):
        """Procesa un archivo HTML añadiendo el indicador"""
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Determinar el indicador
            indicador = circulo_amarillo if nombre_archivo in candidatos_con_dudas else circulo_verde
            
            # Reemplazar el título principal en HTML
            patron_titulo = r'<h1>👤 Perfil de (.+?)</h1>'
            nuevo_titulo = f'<h1>{indicador} 👤 Perfil de \\1</h1>'
            contenido_modificado = re.sub(patron_titulo, nuevo_titulo, contenido)
            
            # También actualizar el título de la página
            patron_title = r'<title>Perfil - (.+?)</title>'
            nuevo_title = f'<title>{indicador} Perfil - \\1</title>'
            contenido_modificado = re.sub(patron_title, nuevo_title, contenido_modificado)
            
            # Escribir archivo modificado
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(contenido_modificado)
            
            return True
        except Exception as e:
            print(f"❌ Error procesando HTML {nombre_archivo}: {e}")
            return False
    
    # Procesar archivos MD principales
    carpeta_md = 'perfiles_md'
    archivos_md_procesados = 0
    
    print("📝 Procesando archivos Markdown...")
    for archivo in os.listdir(carpeta_md):
        if archivo.endswith('.md'):
            nombre_sin_ext = archivo.replace('.md', '')
            ruta_archivo = os.path.join(carpeta_md, archivo)
            
            if procesar_archivo_md(ruta_archivo, nombre_sin_ext):
                indicador = candidatos_con_dudas.get(nombre_sin_ext, 'sin_dudas')
                estado = "🟡 CON DUDAS" if nombre_sin_ext in candidatos_con_dudas else "🟢 SIN PROBLEMAS"
                print(f"  ✅ {archivo} - {estado}")
                archivos_md_procesados += 1
    
    # Procesar archivos HTML principales
    carpeta_html = 'perfiles_html'
    archivos_html_procesados = 0
    
    print("\n🌐 Procesando archivos HTML...")
    for archivo in os.listdir(carpeta_html):
        if archivo.endswith('.html') and archivo != 'index.html':
            nombre_sin_ext = archivo.replace('.html', '')
            ruta_archivo = os.path.join(carpeta_html, archivo)
            
            if procesar_archivo_html(ruta_archivo, nombre_sin_ext):
                estado = "🟡 CON DUDAS" if nombre_sin_ext in candidatos_con_dudas else "🟢 SIN PROBLEMAS"
                print(f"  ✅ {archivo} - {estado}")
                archivos_html_procesados += 1
    
    # Procesar archivos en carpetas por área
    print("\n📁 Procesando archivos por área...")
    
    # MD por área
    carpeta_area_md = 'perfiles_por_area_md'
    for area in os.listdir(carpeta_area_md):
        carpeta_area_completa = os.path.join(carpeta_area_md, area)
        if os.path.isdir(carpeta_area_completa):
            for archivo in os.listdir(carpeta_area_completa):
                if archivo.endswith('.md'):
                    nombre_sin_ext = archivo.replace('.md', '')
                    ruta_archivo = os.path.join(carpeta_area_completa, archivo)
                    
                    if procesar_archivo_md(ruta_archivo, nombre_sin_ext):
                        estado = "🟡 CON DUDAS" if nombre_sin_ext in candidatos_con_dudas else "🟢 SIN PROBLEMAS"
                        print(f"  ✅ {area}/{archivo} - {estado}")
                        archivos_md_procesados += 1
    
    # HTML por área
    carpeta_area_html = 'perfiles_por_area_html'
    for area in os.listdir(carpeta_area_html):
        carpeta_area_completa = os.path.join(carpeta_area_html, area)
        if os.path.isdir(carpeta_area_completa):
            for archivo in os.listdir(carpeta_area_completa):
                if archivo.endswith('.html') and archivo != 'index.html':
                    nombre_sin_ext = archivo.replace('.html', '')
                    ruta_archivo = os.path.join(carpeta_area_completa, archivo)
                    
                    if procesar_archivo_html(ruta_archivo, nombre_sin_ext):
                        estado = "🟡 CON DUDAS" if nombre_sin_ext in candidatos_con_dudas else "🟢 SIN PROBLEMAS"
                        print(f"  ✅ {area}/{archivo} - {estado}")
                        archivos_html_procesados += 1
    
    print(f"\n🎉 ¡Proceso completado!")
    print(f"📝 Archivos MD procesados: {archivos_md_procesados}")
    print(f"🌐 Archivos HTML procesados: {archivos_html_procesados}")
    print(f"\n📊 Leyenda de indicadores:")
    print(f"🟢 = Sin problemas de tiempo (respuesta positiva)")
    print(f"🟡 = Con dudas sobre tiempo disponible")
    print(f"\n📋 Candidatos con dudas identificados:")
    for nombre, respuesta in candidatos_con_dudas.items():
        print(f"  🟡 {nombre.replace('_', ' ')}: '{respuesta}'")

if __name__ == "__main__":
    añadir_indicadores_disponibilidad()