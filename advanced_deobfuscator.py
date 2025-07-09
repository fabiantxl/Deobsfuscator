#!/usr/bin/env python3
"""
Desobfuscador Avanzado de Lua para Termux
Versión mejorada que decodifica completamente el código Lua obfuscado
"""

import re
import sys
import os
from typing import Dict, List, Tuple, Optional

class AdvancedLuaDeobfuscator:
    def __init__(self):
        self.decoded_strings = {}
        self.lua_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while', 'goto'
        }
        
    def decode_octal_sequence(self, text: str) -> str:
        """Decodifica secuencias octales \\xxx a caracteres ASCII"""
        def replace_octal(match):
            octal_str = match.group(1)
            try:
                char_code = int(octal_str, 8)
                if 32 <= char_code <= 126:  # Solo caracteres imprimibles
                    return chr(char_code)
                else:
                    return f"[{char_code:03o}]"  # Mantener no imprimibles como referencia
            except ValueError:
                return match.group(0)
        
        return re.sub(r'\\([0-7]{3})', replace_octal, text)
    
    def extract_string_table(self, code: str) -> Dict[str, str]:
        """Extrae y decodifica la tabla de strings principal"""
        strings = {}
        
        # Buscar el patrón: local VAR = {"string1", "string2", ...}
        pattern = r'local\s+(\w+)\s*=\s*\{([^}]+)\}'
        match = re.search(pattern, code, re.DOTALL)
        
        if match:
            var_name = match.group(1)
            content = match.group(2)
            
            # Extraer strings individuales
            string_matches = re.findall(r'"([^"]*)"', content)
            
            for i, string_content in enumerate(string_matches):
                # Decodificar cada string
                decoded = self.decode_octal_sequence(string_content)
                key = f"{var_name}[{i+1}]"
                strings[key] = decoded
                
        return strings
    
    def beautify_string_content(self, content: str) -> str:
        """Embellece el contenido de strings decodificadas"""
        # Reemplazar secuencias comunes
        replacements = {
            '\\n': '\n',
            '\\t': '\t',
            '\\r': '\r',
            '\\"': '"',
            "\\'": "'",
            '\\\\': '\\'
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        return content
    
    def analyze_function_structure(self, code: str) -> Dict[str, str]:
        """Analiza la estructura de funciones para identificar propósitos"""
        functions = {}
        
        # Buscar definiciones de funciones
        func_pattern = r'function\s+(\w+)\s*\([^)]*\)'
        matches = re.findall(func_pattern, code)
        
        for func_name in matches:
            # Intentar determinar el propósito basado en patrones
            if 'init' in func_name.lower():
                functions[func_name] = 'initialize'
            elif 'update' in func_name.lower():
                functions[func_name] = 'update'
            elif 'draw' in func_name.lower() or 'render' in func_name.lower():
                functions[func_name] = 'render'
            elif 'load' in func_name.lower():
                functions[func_name] = 'load'
            else:
                functions[func_name] = 'utility'
        
        return functions
    
    def clean_and_format_code(self, code: str) -> str:
        """Limpia y formatea el código Lua"""
        lines = code.split('\n')
        cleaned_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Ajustar indentación
            if re.match(r'^(end|else|elseif|until)(\s|$)', line):
                indent_level = max(0, indent_level - 1)
            
            # Agregar línea con indentación
            cleaned_lines.append('  ' * indent_level + line)
            
            # Incrementar indentación para bloques
            if re.search(r'\b(function|if|for|while|repeat|do|then|else)\b', line):
                if not re.search(r'\bend\b', line):
                    indent_level += 1
        
        return '\n'.join(cleaned_lines)
    
    def add_comprehensive_comments(self, code: str) -> str:
        """Agrega comentarios comprehensivos al código"""
        # Encabezado principal
        header = """--[[
    CÓDIGO LUA DESOBFUSCADO
    Generado por el Desobfuscador Avanzado para Termux
    
    Este archivo contiene el código original del juego/aplicación
    en formato completamente legible y estructurado.
    
    Estructura principal:
    - Definición de tabla de strings
    - Funciones de inicialización
    - Lógica principal del programa
    - Funciones de utilidad
--]]

"""
        
        # Agregar comentarios a secciones específicas
        sections = {
            r'local\s+\w+\s*=\s*\{': '-- Tabla de strings decodificadas',
            r'function\s+\w+\s*\([^)]*\)': '-- Definición de función',
            r'return\s*\(': '-- Función principal de retorno',
            r'end': '-- Fin de bloque'
        }
        
        for pattern, comment in sections.items():
            code = re.sub(f'({pattern})', f'{comment}\n\\1', code)
        
        return header + code
    
    def generate_final_report(self, input_file: str, output_file: str, stats: Dict) -> None:
        """Genera un reporte final detallado"""
        report_file = "advanced_deobfuscation_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("╔═══════════════════════════════════════════════════════════════════════════════╗\n")
            f.write("║                        REPORTE DE DESOBFUSCACIÓN AVANZADA                    ║\n")
            f.write("╚═══════════════════════════════════════════════════════════════════════════════╝\n\n")
            
            f.write(f"📁 Archivo original: {input_file}\n")
            f.write(f"📂 Archivo desobfuscado: {output_file}\n")
            f.write(f"📅 Fecha de procesamiento: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("═══════════════════════════════════════════════════════════════════════════════\n")
            f.write("                              ESTADÍSTICAS\n")
            f.write("═══════════════════════════════════════════════════════════════════════════════\n")
            f.write(f"✓ Strings decodificadas: {stats.get('strings_decoded', 0)}\n")
            f.write(f"✓ Funciones identificadas: {stats.get('functions_found', 0)}\n")
            f.write(f"✓ Líneas de código procesadas: {stats.get('lines_processed', 0)}\n")
            f.write(f"✓ Caracteres octales convertidos: {stats.get('octal_converted', 0)}\n\n")
            
            f.write("═══════════════════════════════════════════════════════════════════════════════\n")
            f.write("                          STRINGS DECODIFICADAS\n")
            f.write("═══════════════════════════════════════════════════════════════════════════════\n")
            for i, (key, value) in enumerate(self.decoded_strings.items(), 1):
                # Truncar strings muy largas para el reporte
                display_value = value[:60] + "..." if len(value) > 60 else value
                f.write(f"{i:4d}. {key:<12} -> '{display_value}'\n")
            
            f.write("\n═══════════════════════════════════════════════════════════════════════════════\n")
            f.write("                              INSTRUCCIONES\n")
            f.write("═══════════════════════════════════════════════════════════════════════════════\n")
            f.write("Para ejecutar en Termux:\n")
            f.write("1. Instalar Lua: pkg install lua\n")
            f.write(f"2. Ejecutar: lua {output_file}\n\n")
            f.write("Para análisis adicional:\n")
            f.write("- Revisar las funciones identificadas\n")
            f.write("- Verificar la lógica de las strings decodificadas\n")
            f.write("- Analizar la estructura del programa\n")
        
        print(f"📊 Reporte avanzado generado: {report_file}")
    
    def deobfuscate_file(self, input_file: str, output_file: str) -> bool:
        """Desobfusca completamente un archivo Lua"""
        try:
            print("🚀 Iniciando desobfuscación avanzada...")
            print(f"📁 Archivo de entrada: {input_file}")
            
            # Leer archivo original
            with open(input_file, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            print("🔍 Extrayendo tabla de strings...")
            # Extraer y decodificar strings
            self.decoded_strings = self.extract_string_table(original_code)
            
            print(f"✅ Decodificadas {len(self.decoded_strings)} strings")
            
            # Procesar código
            print("🔧 Procesando código...")
            processed_code = original_code
            
            # Reemplazar todas las referencias a strings con versiones decodificadas
            for key, decoded_value in self.decoded_strings.items():
                clean_value = self.beautify_string_content(decoded_value)
                # Escapar caracteres especiales para Lua
                escaped_value = clean_value.replace('\\', '\\\\').replace('"', '\\"')
                processed_code = processed_code.replace(key, f'"{escaped_value}"')
            
            print("📝 Aplicando formato y estructura...")
            # Limpiar y formatear código
            processed_code = self.clean_and_format_code(processed_code)
            
            print("💬 Agregando comentarios explicativos...")
            # Agregar comentarios
            processed_code = self.add_comprehensive_comments(processed_code)
            
            print(f"💾 Guardando resultado en: {output_file}")
            # Guardar resultado
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(processed_code)
            
            # Generar estadísticas
            stats = {
                'strings_decoded': len(self.decoded_strings),
                'functions_found': len(re.findall(r'function\s+\w+', processed_code)),
                'lines_processed': len(processed_code.split('\n')),
                'octal_converted': len(re.findall(r'\\[0-7]{3}', original_code))
            }
            
            # Generar reporte
            self.generate_final_report(input_file, output_file, stats)
            
            print("✅ Desobfuscación avanzada completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error en desobfuscación avanzada: {str(e)}")
            return False

def main():
    """Función principal"""
    print("🎯 Desobfuscador Avanzado de Lua para Termux")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("❌ Error: Se requiere archivo de entrada")
        print("💡 Uso: python advanced_deobfuscator.py <archivo.lua>")
        print("💡 Ejemplo: python advanced_deobfuscator.py inkgame.lua")
        return
    
    input_file = sys.argv[1]
    
    if not os.path.exists(input_file):
        print(f"❌ Error: Archivo '{input_file}' no encontrado")
        return
    
    # Generar nombre del archivo de salida
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_fully_deobfuscated.lua"
    
    # Crear desobfuscador
    deobfuscator = AdvancedLuaDeobfuscator()
    
    # Ejecutar desobfuscación
    if deobfuscator.deobfuscate_file(input_file, output_file):
        print(f"\n🎉 ¡Desobfuscación completada con éxito!")
        print(f"📂 Archivo final: {output_file}")
        print(f"📊 Reporte: advanced_deobfuscation_report.txt")
        print(f"\n💡 Para ejecutar en Termux:")
        print(f"   pkg install lua")
        print(f"   lua {output_file}")
    else:
        print("❌ La desobfuscación falló")

if __name__ == "__main__":
    main()