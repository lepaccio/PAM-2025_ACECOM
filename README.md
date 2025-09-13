# 🎓 Sistema de Perfiles PAM 2025 - ACECOM

Sistema automatizado para procesar y organizar perfiles de postulantes al Proceso de Admisión de Miembros (PAM) 2025 de ACECOM.

## 📋 Descripción

Este proyecto procesa datos de formularios CSV y genera perfiles individuales organizados por área de interés, con indicadores visuales de disponibilidad de tiempo.

## ✨ Características

- **Generación automática de perfiles** en formato Markdown y HTML
- **Organización por áreas** (Inteligencia Artificial, Seguridad Informática, Desarrollo Web)
- **Indicadores visuales** de disponibilidad:
  - 🟢 Sin problemas de tiempo
  - 🟡 Con dudas sobre disponibilidad
- **Navegación web** con índices y enlaces entre perfiles
- **Limpieza automática** de datos de prueba

## 🚀 Instalación

### Usando pip:
```bash
pip install -r requirements.txt
```

### Usando conda:
```bash
conda env create -f environment.yml
conda activate pam-2025
```

## 💻 Uso

1. **Organizar perfiles básicos:**
   ```bash
   python organizador.py
   ```

2. **Convertir a HTML:**
   ```bash
   python convertir_html.py
   ```

3. **Organizar por áreas:**
   ```bash
   python organizar_por_areas.py
   ```

4. **Añadir indicadores visuales:**
   ```bash
   python añadir_indicadores.py
   ```

## 📊 Estructura de Datos

- **Entrada:** `PAM 2025_2.csv` (formulario de postulación)
- **Salidas:**
  - `perfiles_md/` - Perfiles en Markdown
  - `perfiles_html/` - Perfiles en HTML
  - `perfiles_por_area_*/` - Organizados por área
  - `resultados_ordenados.xlsx` - Excel tradicional

## 📁 Estructura del Proyecto

```
├── organizador.py              # Script principal
├── convertir_html.py          # Conversión MD → HTML
├── organizar_por_areas.py     # Organización por áreas
├── añadir_indicadores.py      # Indicadores visuales
├── PAM 2025_2.csv            # Datos de entrada
├── requirements.txt          # Dependencias Python
├── environment.yml           # Entorno conda
└── README.md                # Documentación
```

## 🎯 Estadísticas PAM 2025

- **Total candidatos:** 23
- **Áreas:**
  - Inteligencia Artificial: 9 candidatos
  - Seguridad Informática: 8 candidatos  
  - Desarrollo Web: 6 candidatos
- **Disponibilidad:**
  - 🟢 17 candidatos sin problemas (74%)
  - 🟡 6 candidatos con dudas (26%)

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Proyecto interno de ACECOM - UNI

---
*Generado automáticamente el 12 de septiembre de 2025*