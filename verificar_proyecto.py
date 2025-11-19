#!/usr/bin/env python
"""
Script de verificación completa del proyecto
Verifica que todos los componentes estén correctamente configurados
"""

import os
import sys
import json
from pathlib import Path

# Colores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check(condition, message):
    """Verifica una condición e imprime resultado"""
    if condition:
        print(f"{GREEN}✓{RESET} {message}")
        return True
    else:
        print(f"{RED}✗{RESET} {message}")
        return False

def warn(message):
    """Imprime una advertencia"""
    print(f"{YELLOW}⚠{RESET} {message}")

print("=" * 70)
print("VERIFICACIÓN DEL PROYECTO - CLASIFICADOR DE PLANTAS MEDICINALES")
print("=" * 70)
print()

total_checks = 0
passed_checks = 0

# 1. Estructura de Directorios
print("1. Estructura de Directorios:")
dirs_to_check = [
    'src', 'src/dataset', 'src/models', 'src/utils',
    'app', 'app/templates', 'app/static', 'app/static/css', 'app/static/js',
    'data', 'config', 'notebooks', 'docs', 'models', 'tests'
]

for dir_path in dirs_to_check:
    total_checks += 1
    if check(os.path.isdir(dir_path), f"Directorio '{dir_path}' existe"):
        passed_checks += 1

print()

# 2. Archivos Python Esenciales
print("2. Archivos Python Esenciales:")
py_files = [
    'src/__init__.py',
    'src/dataset/__init__.py',
    'src/dataset/download.py',
    'src/dataset/preprocess.py',
    'src/dataset/dataset.py',
    'src/models/__init__.py',
    'src/models/classifier.py',
    'src/models/train.py',
    'src/utils/__init__.py',
    'src/utils/helpers.py',
    'app/__init__.py',
    'app/app.py'
]

for file_path in py_files:
    total_checks += 1
    if check(os.path.isfile(file_path), f"Archivo '{file_path}' existe"):
        passed_checks += 1

print()

# 3. Archivos de Configuración
print("3. Archivos de Configuración:")
config_files = [
    'config/config.yaml',
    'data/plantas_info.json',
    'requirements.txt',
    '.gitignore',
    'README.md'
]

for file_path in config_files:
    total_checks += 1
    if check(os.path.isfile(file_path), f"Archivo '{file_path}' existe"):
        passed_checks += 1

print()

# 4. Notebooks
print("4. Notebooks Jupyter:")
notebooks = [
    'notebooks/01_exploracion_datos.ipynb',
    'notebooks/02_entrenamiento_modelo.ipynb',
    'notebooks/03_evaluacion_modelo.ipynb'
]

for nb in notebooks:
    total_checks += 1
    if check(os.path.isfile(nb), f"Notebook '{nb}' existe"):
        passed_checks += 1

print()

# 5. Frontend (HTML/CSS/JS)
print("5. Archivos Frontend:")
frontend_files = [
    'app/templates/index.html',
    'app/static/css/style.css',
    'app/static/js/main.js'
]

for file_path in frontend_files:
    total_checks += 1
    if check(os.path.isfile(file_path), f"Archivo '{file_path}' existe"):
        passed_checks += 1

print()

# 6. Validación de config.yaml
print("6. Validación de Configuración:")
try:
    import yaml
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    total_checks += 1
    if check('dataset' in config, "Config tiene sección 'dataset'"):
        passed_checks += 1

    total_checks += 1
    if check('model' in config, "Config tiene sección 'model'"):
        passed_checks += 1

    total_checks += 1
    if check('training' in config, "Config tiene sección 'training'"):
        passed_checks += 1

except Exception as e:
    total_checks += 3
    check(False, f"Error al cargar config.yaml: {e}")

print()

# 7. Validación de plantas_info.json
print("7. Validación de Base de Conocimientos:")
try:
    with open('data/plantas_info.json', 'r', encoding='utf-8') as f:
        plantas = json.load(f)

    total_checks += 1
    if check('plantas_medicinales' in plantas, "JSON tiene 'plantas_medicinales'"):
        passed_checks += 1
        num_plantas = len(plantas['plantas_medicinales'])
        print(f"   → {num_plantas} plantas registradas")

except Exception as e:
    total_checks += 1
    check(False, f"Error al cargar plantas_info.json: {e}")

print()

# 8. Sintaxis de Python
print("8. Verificación de Sintaxis Python:")
import py_compile

py_modules = [
    'src/utils/helpers.py',
    'src/dataset/download.py',
    'src/dataset/preprocess.py',
    'src/dataset/dataset.py',
    'src/models/classifier.py',
    'src/models/train.py',
    'app/app.py'
]

for module in py_modules:
    total_checks += 1
    try:
        py_compile.compile(module, doraise=True)
        if check(True, f"Sintaxis de '{module}' OK"):
            passed_checks += 1
    except py_compile.PyCompileError as e:
        check(False, f"Error de sintaxis en '{module}': {e}")

print()

# 9. Verificación de Dependencias
print("9. Dependencias (requirements.txt):")
try:
    with open('requirements.txt', 'r') as f:
        requirements = f.read()

    critical_packages = [
        'torch', 'torchvision', 'Flask', 'opencv-python',
        'numpy', 'pandas', 'matplotlib', 'pyyaml'
    ]

    for package in critical_packages:
        total_checks += 1
        if check(package in requirements, f"Dependencia '{package}' en requirements.txt"):
            passed_checks += 1

except Exception as e:
    check(False, f"Error al leer requirements.txt: {e}")

print()

# Resumen Final
print("=" * 70)
print("RESUMEN DE LA VERIFICACIÓN")
print("=" * 70)
percentage = (passed_checks / total_checks * 100) if total_checks > 0 else 0
print(f"Verificaciones pasadas: {passed_checks}/{total_checks} ({percentage:.1f}%)")
print()

if percentage == 100:
    print(f"{GREEN}✓ PROYECTO COMPLETAMENTE CORRECTO{RESET}")
    print("  Todos los archivos y configuraciones están en su lugar.")
elif percentage >= 90:
    print(f"{GREEN}✓ PROYECTO EN EXCELENTE ESTADO{RESET}")
    print("  La mayoría de componentes están correctos.")
elif percentage >= 70:
    print(f"{YELLOW}⚠ PROYECTO FUNCIONAL CON ADVERTENCIAS{RESET}")
    print("  Algunos componentes necesitan atención.")
else:
    print(f"{RED}✗ PROYECTO NECESITA CORRECCIONES{RESET}")
    print("  Varios componentes tienen problemas.")

print()
print("=" * 70)
print("SIGUIENTE PASO:")
print("=" * 70)

if percentage >= 90:
    print("1. Instalar dependencias:")
    print("   pip install -r requirements.txt")
    print()
    print("2. Descargar dataset:")
    print("   kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset")
    print()
    print("3. Ejecutar notebooks en orden:")
    print("   jupyter notebook notebooks/01_exploracion_datos.ipynb")
else:
    print("1. Revisar los errores marcados arriba")
    print("2. Corregir los archivos faltantes")
    print("3. Ejecutar este script nuevamente")

print("=" * 70)
