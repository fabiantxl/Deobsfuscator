#!/usr/bin/env python3
"""
Desobfuscador de Lua para Termux
Convierte código Lua obfuscado en formato legible
"""

import re
import sys
import os
from typing import Dict, List, Tuple, Optional

class LuaDeobfuscator:
    def __init__(self):
        self.octal_pattern = re.compile(r'\\([0-7]{3})')
        self.string_table = {}
        self.variable_names = {}
        self.function_names = {}
        self.reserved_words = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'if', 'in', 'local', 'nil', 'not', 'or', 'repeat',
            'return', 'then', 'true', 'until', 'while'
        }
        
    def decode_octal_string(self, octal_str: str) -> str:
        """Decodifica strings con secuencias octales"""
        def replace_octal(match):
            octal_value = match.group(1)
            return chr(int(octal_value, 8))
        
        return self.octal_pattern.sub(replace_octal, octal_str)
    
    def extract_string_table(self, code: str) -> Dict[str, str]:
        """Extrae la tabla de strings obfuscados"""
        string_table = {}
        
        # Buscar patrones como local J={"string1","string2",...}
        table_pattern = r'local\s+(\w+)\s*=\s*\{([^}]+)\}'
        match = re.search(table_pattern, code)
        
        if match:
            var_name = match.group(1)
            table_content = match.group(2)
            
            # Extraer strings individuales
            string_pattern = r'"([^"]*)"'
            strings = re.findall(string_pattern, table_content)
            
            for i, string in enumerate(strings):
                decoded = self.decode_octal_string(string)
                string_table[f"{var_name}[{i+1}]"] = decoded
                
        return string_table
    
    def generate_meaningful_name(self, original: str, context: str = "") -> str:
        """Genera nombres de variables más significativos"""
        if original in self.variable_names:
            return self.variable_names[original]
        
        # Mapeo de variables comunes
        common_mappings = {
            'J': 'stringTable',
            'l': 'local_var',
            'o': 'object',
            'e': 'element',
            'n': 'number',
            'r': 'result',
            't': 'table',
            'f': 'function_ref',
            'a': 'argument',
            'i': 'index',
            'v': 'value',
            'x': 'x_pos',
            'y': 'y_pos',
            'w': 'width',
            'h': 'height',
            'c': 'color',
            'd': 'data',
            's': 'string',
            'p': 'position',
            'g': 'game',
            'u': 'user',
            'm': 'mouse',
            'k': 'key'
        }
        
        if original in common_mappings:
            new_name = common_mappings[original]
        else:
            new_name = f"var_{original}"
            
        # Evitar palabras reservadas
        if new_name in self.reserved_words:
            new_name = f"{new_name}_var"
            
        self.variable_names[original] = new_name
        return new_name
    
    def clean_code_structure(self, code: str) -> str:
        """Limpia y formatea la estructura del código"""
        # Remover comentarios innecesarios
        code = re.sub(r'--.*$', '', code, flags=re.MULTILINE)
        
        # Agregar espacios alrededor de operadores
        code = re.sub(r'([=<>!+\-*/%])(?!=)', r' \1 ', code)
        code = re.sub(r'([,;])', r'\1 ', code)
        
        # Limpiar espacios múltiples
        code = re.sub(r'\s+', ' ', code)
        
        return code
    
    def format_lua_code(self, code: str) -> str:
        """Formatea el código Lua con indentación apropiada"""
        lines = code.split('\n')
        formatted_lines = []
        indent_level = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Decrementar indentación para 'end', 'else', 'elseif', etc.
            if re.match(r'^\s*(end|else|elseif|until)\b', line):
                indent_level = max(0, indent_level - 1)
            
            # Agregar indentación
            formatted_lines.append('  ' * indent_level + line)
            
            # Incrementar indentación para bloques
            if re.search(r'\b(function|if|for|while|repeat|do|else|elseif|then)\b', line):
                if not re.search(r'\bend\b', line):
                    indent_level += 1
        
        return '\n'.join(formatted_lines)
    
    def add_comments_and_documentation(self, code: str) -> str:
        """Agrega comentarios explicativos al código"""
        # Agregar encabezado
        header = """-- Archivo Lua desobfuscado
-- Generado por el desobfuscador de Termux
-- Estructura del juego restaurada

"""
        
        # Identificar funciones y agregar comentarios
        function_pattern = r'function\s+(\w+)\s*\([^)]*\)'
        functions = re.findall(function_pattern, code)
        
        for func in functions:
            comment = f"-- Función: {func}\n"
            code = re.sub(f'function\\s+{func}\\s*\\([^)]*\\)', 
                         f'{comment}function {func}(', code)
        
        return header + code
    
    def decode_all_octal_strings(self, code: str) -> str:
        """Decodifica todas las strings octales en el código"""
        def replace_octal_in_string(match):
            string_content = match.group(1)
            decoded_content = self.decode_octal_string(string_content)
            # Filtrar caracteres no imprimibles
            cleaned_content = ''.join(c for c in decoded_content if c.isprintable() or c in '\n\t\r')
            return f'"{cleaned_content}"'
        
        # Buscar strings con contenido octal
        octal_string_pattern = r'"([^"]*\\[0-7]{3}[^"]*)"'
        return re.sub(octal_string_pattern, replace_octal_in_string, code)
    
    def improve_variable_names(self, code: str) -> str:
        """Mejora los nombres de variables para mayor legibilidad"""
        # Patrones comunes en código obfuscado
        patterns = {
            r'\blocal\s+([a-zA-Z])\s*=': 'local variable',
            r'\bfunction\s+([a-zA-Z])\s*\(': 'function',
        }
        
        for pattern, context in patterns.items():
            matches = re.findall(pattern, code)
            for match in matches:
                if len(match) == 1:  # Solo variables de una letra
                    new_name = self.generate_meaningful_name(match, context)
                    # Reemplazar solo como palabra completa
                    code = re.sub(rf'\b{match}\b', new_name, code)
        
        return code
    
    def deobfuscate_file(self, input_file: str, output_file: str) -> bool:
        """Desobfusca un archivo Lua completo"""
        try:
            print(f"📁 Leyendo archivo: {input_file}")
            
            with open(input_file, 'r', encoding='utf-8') as f:
                original_code = f.read()
            
            print("🔍 Analizando código obfuscado...")
            
            # Extraer tabla de strings
            self.string_table = self.extract_string_table(original_code)
            print(f"✓ Encontradas {len(self.string_table)} strings codificadas")
            
            # Proceso de desobfuscación
            deobfuscated_code = original_code
            
            # 1. Decodificar todas las strings octales en el código
            print("🔓 Decodificando strings octales...")
            deobfuscated_code = self.decode_all_octal_strings(deobfuscated_code)
            
            # 2. Reemplazar variables con nombres más descriptivos
            print("🏷️ Mejorando nombres de variables...")
            deobfuscated_code = self.improve_variable_names(deobfuscated_code)
            
            # 3. Limpiar estructura del código
            print("🧹 Limpiando estructura del código...")
            deobfuscated_code = self.clean_code_structure(deobfuscated_code)
            
            # 4. Formatear código con indentación
            print("📝 Aplicando formato y indentación...")
            deobfuscated_code = self.format_lua_code(deobfuscated_code)
            
            # 5. Agregar comentarios y documentación
            print("💬 Agregando comentarios explicativos...")
            deobfuscated_code = self.add_comments_and_documentation(deobfuscated_code)
            
            # 6. Guardar resultado
            print(f"💾 Guardando resultado en: {output_file}")
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(deobfuscated_code)
            
            print("✅ Desobfuscación completada exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante la desobfuscación: {str(e)}")
            return False
    
    def generate_report(self, input_file: str, output_file: str) -> None:
        """Genera un reporte detallado del proceso"""
        report_file = "deobfuscation_report.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("=== REPORTE DE DESOBFUSCACIÓN ===\n\n")
            f.write(f"Archivo original: {input_file}\n")
            f.write(f"Archivo desobfuscado: {output_file}\n")
            f.write(f"Fecha de procesamiento: {__import__('datetime').datetime.now()}\n\n")
            
            f.write("=== STRINGS DECODIFICADAS ===\n")
            for i, (key, value) in enumerate(self.string_table.items(), 1):
                f.write(f"{i:3d}. {key} -> '{value}'\n")
            
            f.write(f"\n=== ESTADÍSTICAS ===\n")
            f.write(f"Total de strings decodificadas: {len(self.string_table)}\n")
            f.write(f"Variables renombradas: {len(self.variable_names)}\n")
            
            f.write("\n=== VARIABLES RENOMBRADAS ===\n")
            for old, new in self.variable_names.items():
                f.write(f"{old} -> {new}\n")
        
        print(f"📊 Reporte generado: {report_file}")

def main():
    """Función principal del desobfuscador"""
    print("🚀 Desobfuscador de Lua para Termux")
    print("=" * 40)
    
    # Verificar argumentos
    if len(sys.argv) < 2:
        print("❌ Error: Falta el archivo de entrada")
        print("💡 Uso: python deobfuscator.py <archivo_lua>")
        print("💡 Ejemplo: python deobfuscator.py inkgame.lua")
        return
    
    input_file = sys.argv[1]
    
    # Verificar que el archivo existe
    if not os.path.exists(input_file):
        print(f"❌ Error: El archivo '{input_file}' no existe")
        return
    
    # Generar nombre del archivo de salida
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_deobfuscated.lua"
    
    # Crear instancia del desobfuscador
    deobfuscator = LuaDeobfuscator()
    
    # Procesar archivo
    if deobfuscator.deobfuscate_file(input_file, output_file):
        deobfuscator.generate_report(input_file, output_file)
        print(f"\n🎉 ¡Proceso completado!")
        print(f"📂 Archivo desobfuscado: {output_file}")
        print(f"📊 Reporte detallado: deobfuscation_report.txt")
    else:
        print("❌ La desobfuscación falló")

if __name__ == "__main__":
    main()