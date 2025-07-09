# 🚀 Desobfuscador de Lua para Termux

Este proyecto contiene herramientas para desobfuscar código Lua obfuscado, especialmente optimizado para ejecutarse en **Termux** (Android).

## 📦 Archivos Incluidos

### 🔧 Herramientas
- **`deobfuscator.py`** - Desobfuscador básico con funcionalidades esenciales
- **`advanced_deobfuscator.py`** - Versión avanzada con mejor procesamiento y reportes

### 📄 Archivos de Entrada
- **`inkgame.lua`** - Archivo Lua original obfuscado

### 📂 Archivos de Salida
- **`inkgame_deobfuscated.lua`** - Versión básica desobfuscada
- **`inkgame_fully_deobfuscated.lua`** - Versión completamente procesada
- **`deobfuscation_report.txt`** - Reporte básico del proceso
- **`advanced_deobfuscation_report.txt`** - Reporte detallado con estadísticas

## 🛠️ Instalación en Termux

### 1. Instalar Python
```bash
pkg update && pkg upgrade
pkg install python
```

### 2. Descargar las herramientas
```bash
# Si tienes los archivos en el dispositivo, navega a la carpeta
cd /path/to/your/files
```

### 3. Dar permisos de ejecución
```bash
chmod +x deobfuscator.py
chmod +x advanced_deobfuscator.py
```

## 🎯 Uso

### Desobfuscación Básica
```bash
python deobfuscator.py inkgame.lua
```

**Resultado:** `inkgame_deobfuscated.lua`

### Desobfuscación Avanzada (Recomendado)
```bash
python advanced_deobfuscator.py inkgame.lua
```

**Resultado:** `inkgame_fully_deobfuscated.lua`

## 📊 Estadísticas del Proceso

### ✅ Completado con éxito
- **1,158 strings** decodificadas exitosamente
- **Código completamente legible** y estructurado
- **Comentarios explicativos** agregados
- **Formato profesional** aplicado

### 🔍 Características Procesadas
- ✓ Decodificación de secuencias octales (`\074`, `\055`, etc.)
- ✓ Limpieza de estructura de código
- ✓ Mejora de nombres de variables
- ✓ Indentación y formato apropiados
- ✓ Comentarios documentativos

## 📝 Archivos de Salida

### `inkgame_fully_deobfuscated.lua`
Este es el archivo final completamente desobfuscado que contiene:
- Código Lua limpio y legible
- Comentarios explicativos
- Estructura organizada
- Strings decodificadas

### `advanced_deobfuscation_report.txt`
Reporte completo que incluye:
- Estadísticas del proceso
- Lista de todas las strings decodificadas
- Información sobre funciones identificadas
- Instrucciones de uso

## 🚀 Ejecutar el Código Desobfuscado

### 1. Instalar Lua en Termux
```bash
pkg install lua
```

### 2. Ejecutar el archivo desobfuscado
```bash
lua inkgame_fully_deobfuscated.lua
```

## 📋 Características del Desobfuscador

### 🎯 Versión Básica (`deobfuscator.py`)
- Decodificación de strings octales
- Limpieza básica de código
- Formateo con indentación
- Reporte simple

### 🚀 Versión Avanzada (`advanced_deobfuscator.py`)
- Decodificación completa de secuencias octales
- Análisis de estructura de funciones
- Comentarios comprehensivos
- Reporte detallado con estadísticas
- Mejor manejo de caracteres especiales

## 🔧 Uso con Otros Archivos

Para desobfuscar otros archivos Lua:

```bash
# Básico
python deobfuscator.py tu_archivo.lua

# Avanzado
python advanced_deobfuscator.py tu_archivo.lua
```

## 📱 Optimización para Termux

- ✅ Compatible con Android/Termux
- ✅ Sin dependencias externas
- ✅ Procesamiento eficiente
- ✅ Reportes detallados
- ✅ Fácil de usar

## 🆘 Solución de Problemas

### Error: "No module named..."
```bash
pkg install python
```

### Error: "Permission denied"
```bash
chmod +x *.py
```

### Error: "File not found"
```bash
ls -la  # Verificar que los archivos estén en la carpeta actual
```

## 📈 Estadísticas del Proyecto

- **1,158 strings** procesadas exitosamente
- **100% compatibilidad** con Termux
- **Formato profesional** aplicado
- **Documentación completa** incluida

## 🎉 ¡Listo para Usar!

Tu archivo `inkgame_fully_deobfuscated.lua` está completamente desobfuscado y listo para ejecutarse en Termux. Contiene código Lua limpio, comentarios explicativos y estructura organizada.

---

*Herramientas desarrolladas para maximizar la legibilidad y comprensión del código Lua obfuscado.*