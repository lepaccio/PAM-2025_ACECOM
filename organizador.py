import pandas as pd
import os
import re

def limpiar_texto(texto):
    """Limpia y formatea el texto básico"""
    if pd.isna(texto) or texto == '':
        return texto
    
    # Convertir a string y limpiar espacios extra
    texto = str(texto).strip()
    # Limpiar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    return texto

def limpiar_nombre_archivo(nombre):
    """Limpia el nombre para usarlo como nombre de archivo"""
    nombre = str(nombre).strip()
    # Remover caracteres no válidos para nombres de archivo
    nombre = re.sub(r'[<>:"/\\|?*]', '', nombre)
    # Reemplazar espacios con guiones bajos
    nombre = re.sub(r'\s+', '_', nombre)
    return nombre

def generar_perfil_md(persona_data, nombre_persona):
    """Genera el contenido Markdown para el perfil de una persona"""
    
    # Mapeo de columnas a preguntas legibles
    preguntas_map = {
        'Código Universitario:\n': '🎓 Código Universitario',
        'Ciclo Relativo': '📚 Ciclo Relativo',
        'Correo Electrónico:\n': '📧 Correo Electrónico',
        'Teléfono (WhatsApp):\n': '📱 Teléfono (WhatsApp)',
        '¿Qué piensas que hacemos en ACECOM?\n': '🤔 ¿Qué piensas que hacemos en ACECOM?',
        '¿Como consideras que ACECOM puede mejorar para ser más atractivo para la población estudiantil de la facultad?': '💡 ¿Cómo consideras que ACECOM puede mejorar para ser más atractivo para la población estudiantil de la facultad?',
        'Dentro del contexto de mejora ¿Siendo tu parte de ACECOM que acciones tomarías para mejorar esta situación? \n': '🚀 Dentro del contexto de mejora ¿Siendo tu parte de ACECOM qué acciones tomarías para mejorar esta situación?',
        '¿Qué te motiva a unirte a ACECOM y no a otro grupo estudiantil? ¿Qué esperas aportar y qué esperas aprender aquí?': '💪 ¿Qué te motiva a unirte a ACECOM y no a otro grupo estudiantil? ¿Qué esperas aportar y qué esperas aprender aquí?',
        'Cuéntanos sobre un proyecto PERSONAL (no un curso) que hayas iniciado por tu cuenta. Puede ser de programación, investigación, un blog, un negocio, etc. Describe qué te impulsó a empezarlo, qué desafí': '🛠️ Cuéntanos sobre un proyecto PERSONAL que hayas iniciado por tu cuenta',
        'Fuera de las clases obligatorias de la universidad, ¿qué estás aprendiendo por tu cuenta actualmente? (Ej: un lenguaje de programación, un framework, sobre inteligencia artificial, etc.). ¿Qué recurso': '📖 ¿Qué estás aprendiendo por tu cuenta actualmente?',
        'Menciona un blog, canal de YouTube, perfil de LinkedIn o libro técnico que hayas encontrado últimamente y que te haya parecido interesante. Explícanos por qué lo recomendarías.\n': '🌐 Menciona un recurso técnico que hayas encontrado últimamente y que te haya parecido interesante',
        '¿A qué área de ACECOM te gustaría postular? Principal interes.\n': '🎯 ¿A qué área de ACECOM te gustaría postular? (Principal interés)',
        'Segunda opción de área': '🎯 Segunda opción de área',
        'Áreas de interés adicionales': '🎯 Áreas de interés adicionales',
        'Nuestro reglamento exige a los miembros un compromiso activo, medido por un sistema de puntos mínimo bimestral. ¿Crees que podrás gestionar este compromiso adicional a tu carga académica?\n\n': '⚖️ ¿Crees que podrás gestionar el compromiso adicional a tu carga académica?'
    }
    
    # Inicio del contenido Markdown
    contenido = f"# 👤 Perfil de {nombre_persona}\n\n"
    contenido += f"---\n\n"
    
    # Agregar nombres y apellidos en una sola línea
    nombres = persona_data.get('Nombres:\n', '')
    apellidos = persona_data.get('Apellidos:', '')
    if pd.notna(nombres) and pd.notna(apellidos):
        nombre_completo = f"{limpiar_texto(str(nombres))} {limpiar_texto(str(apellidos))}"
        contenido += f"## 👤 Nombre Completo\n\n"
        contenido += f"{nombre_completo}\n\n"
        contenido += f"---\n\n"
    
    # Procesar cada columna de datos
    for columna, valor in persona_data.items():
        if columna in ['Id', 'Hora de inicio', 'Hora de finalización', 'Nombre', 'Correo electrónico', 'Nombres:\n', 'Apellidos:']:
            continue  # Saltar columnas administrativas y las ya procesadas
            
        # Obtener el título de la pregunta
        titulo_pregunta = preguntas_map.get(columna, columna)
        
        # Limpiar la respuesta
        if pd.notna(valor) and str(valor).strip() != '':
            respuesta_limpia = limpiar_texto(str(valor))
            contenido += f"## {titulo_pregunta}\n\n"
            contenido += f"{respuesta_limpia}\n\n"
            contenido += f"---\n\n"
    
    return contenido

# Configuración principal
archivo_csv = 'PAM 2025_2.csv'
carpeta_perfiles = 'perfiles_md'

# Crear carpeta para los perfiles si no existe
if not os.path.exists(carpeta_perfiles):
    os.makedirs(carpeta_perfiles)
    print(f"📁 Carpeta '{carpeta_perfiles}' creada")

# Leer el archivo CSV
try:
    df = pd.read_csv(archivo_csv, sep=';')
    print(f"✅ Archivo CSV leído correctamente. Total de registros: {len(df)}")
except FileNotFoundError:
    print(f"❌ Error: No se encontró el archivo '{archivo_csv}'.")
    exit()

# Verificar que la columna de nombres exista
columna_nombres = 'Nombres:\n'
if columna_nombres not in df.columns:
    print(f"❌ Error: La columna '{columna_nombres}' no fue encontrada.")
    print("Columnas disponibles:", df.columns.tolist())
    exit()

# Limpiar datos y eliminar registros vacíos o de prueba
df_limpio = df.dropna(subset=[columna_nombres])
df_limpio = df_limpio[df_limpio[columna_nombres].str.strip() != '']
df_limpio = df_limpio[df_limpio[columna_nombres] != 'asdas']  # Eliminar datos de prueba

print(f"📋 Procesando {len(df_limpio)} perfiles válidos...")

# Generar un archivo MD para cada persona
perfiles_generados = 0
for index, row in df_limpio.iterrows():
    nombre_persona = str(row[columna_nombres]).strip()
    
    # Saltar si el nombre es muy corto o parece ser de prueba
    if len(nombre_persona) < 2 or nombre_persona.lower() in ['i', 'j', 'asdas']:
        continue
    
    # Generar contenido del perfil
    contenido_md = generar_perfil_md(row, nombre_persona)
    
    # Crear nombre de archivo
    nombre_archivo = f"{limpiar_nombre_archivo(nombre_persona)}.md"
    ruta_archivo = os.path.join(carpeta_perfiles, nombre_archivo)
    
    # Escribir archivo
    try:
        with open(ruta_archivo, 'w', encoding='utf-8') as f:
            f.write(contenido_md)
        
        perfiles_generados += 1
        print(f"✅ Perfil generado: {nombre_archivo}")
        
    except Exception as e:
        print(f"❌ Error al generar perfil para {nombre_persona}: {e}")

print(f"\n🎉 ¡Proceso completado!")
print(f"📁 Perfiles generados: {perfiles_generados}")
print(f"📂 Ubicación: ./{carpeta_perfiles}/")
print(f"📝 Formato: Markdown (.md) con limpieza básica de texto")
print(f"🔍 Cada archivo contiene el perfil completo de un postulante")