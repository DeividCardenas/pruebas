"""
Módulo para descarga y organización de datasets de plantas medicinales.

Este módulo proporciona funciones para:
- Descargar datasets de ejemplo desde fuentes públicas
- Organizar imágenes en la estructura correcta
- Verificar y validar datasets
"""

import os
import shutil
import requests
from pathlib import Path
from typing import Optional, List
from tqdm import tqdm


def download_sample_dataset(output_dir: str = "data/raw",
                           source: str = "kaggle") -> None:
    """
    Descarga un dataset de plantas medicinales de ejemplo.

    NOTA: Esta función crea un dataset de ejemplo con estructura de carpetas.
    Para usar datasets reales, recomendamos:

    1. Kaggle Datasets:
       - Indian Medicinal Leaves Dataset: https://www.kaggle.com/datasets/aryashah2k/indian-medicinal-leaves-dataset
       - Medicinal Plant Dataset: https://www.kaggle.com/datasets/swastikadutta/medicinal-plant-dataset

    2. GitHub Datasets:
       - https://github.com/Shubham-Das-Coder/PlantNet300K

    3. PlantNet API o iNaturalist

    Args:
        output_dir: Directorio de salida
        source: Fuente del dataset ('kaggle', 'github', 'custom')
    """
    print("=" * 70)
    print("DESCARGA DE DATASET DE PLANTAS MEDICINALES")
    print("=" * 70)
    print()
    print("Para este proyecto, necesitas descargar un dataset real.")
    print()
    print("OPCIÓN 1 - Kaggle (Recomendado):")
    print("-" * 70)
    print("1. Dataset: 'Indian Medicinal Leaves Dataset'")
    print("   URL: https://www.kaggle.com/datasets/aryashah2k/indian-medicinal-leaves-dataset")
    print()
    print("   Pasos:")
    print("   a) Instala kaggle CLI: pip install kaggle")
    print("   b) Configura tus credenciales en ~/.kaggle/kaggle.json")
    print("   c) Descarga:")
    print("      kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset")
    print("   d) Descomprime en data/raw/")
    print()
    print("2. Dataset alternativo: 'Medicinal Plant Dataset'")
    print("   URL: https://www.kaggle.com/datasets/swastikadutta/medicinal-plant-dataset")
    print()
    print("OPCIÓN 2 - Crear tu propio dataset:")
    print("-" * 70)
    print("Si quieres crear un dataset personalizado:")
    print("1. Crea carpetas en data/raw/ con nombres de plantas:")
    print("   data/raw/aloe_vera/")
    print("   data/raw/manzanilla/")
    print("   data/raw/menta/")
    print("   etc.")
    print()
    print("2. Coloca al menos 50-100 imágenes por clase")
    print("3. Formatos soportados: .jpg, .jpeg, .png")
    print()
    print("OPCIÓN 3 - Web Scraping (con precaución):")
    print("-" * 70)
    print("Puedes recopilar imágenes de:")
    print("- Google Images (uso educativo)")
    print("- iNaturalist API")
    print("- PlantNet API")
    print()
    print("=" * 70)

    # Crear estructura de ejemplo
    os.makedirs(output_dir, exist_ok=True)

    # Crear un archivo README en data/raw
    readme_path = os.path.join(output_dir, "README.md")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("""# Dataset de Plantas Medicinales

## Estructura Requerida

Organiza tus imágenes en la siguiente estructura:

```
data/raw/
├── aloe_vera/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
├── manzanilla/
│   ├── img_001.jpg
│   ├── img_002.jpg
│   └── ...
├── menta/
│   ├── img_001.jpg
│   └── ...
└── ...
```

## Datasets Recomendados

### 1. Indian Medicinal Leaves Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/aryashah2k/indian-medicinal-leaves-dataset
- **Clases**: 40 plantas medicinales indias
- **Imágenes**: ~1000 imágenes de alta calidad
- **Formato**: Hojas escaneadas con fondo blanco

### 2. Medicinal Plant Dataset (Kaggle)
- **URL**: https://www.kaggle.com/datasets/swastikadutta/medicinal-plant-dataset
- **Clases**: 30 plantas medicinales
- **Imágenes**: Variadas

### 3. PlantCLEF / PlantNet
- APIs disponibles para descargar imágenes
- Requiere registro

## Instrucciones de Descarga

### Usando Kaggle CLI:

```bash
# Instalar Kaggle CLI
pip install kaggle

# Configurar credenciales (obtener de kaggle.com/account)
mkdir -p ~/.kaggle
# Copiar kaggle.json a ~/.kaggle/

# Descargar dataset
kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset

# Descomprimir
unzip indian-medicinal-leaves-dataset.zip -d data/raw/
```

## Validación

Después de organizar el dataset, verifica:
- Cada clase tiene al menos 50 imágenes
- Los nombres de carpetas son consistentes
- Los formatos son .jpg, .jpeg o .png
- No hay imágenes corruptas

Usa el script de validación:
```bash
python -c "from src.dataset.download import validate_dataset; validate_dataset('data/raw')"
```
""")

    print(f"\nREADME creado en: {readme_path}")
    print("\nSigue las instrucciones anteriores para descargar un dataset real.")


def validate_dataset(data_dir: str,
                     min_images_per_class: int = 10) -> bool:
    """
    Valida que el dataset tenga la estructura correcta.

    Args:
        data_dir: Directorio del dataset
        min_images_per_class: Número mínimo de imágenes por clase

    Returns:
        True si el dataset es válido, False en caso contrario
    """
    if not os.path.exists(data_dir):
        print(f"❌ Error: El directorio {data_dir} no existe")
        return False

    classes = [d for d in os.listdir(data_dir)
              if os.path.isdir(os.path.join(data_dir, d)) and not d.startswith('.')]

    if len(classes) == 0:
        print(f"❌ Error: No se encontraron clases en {data_dir}")
        return False

    print(f"\n✓ Se encontraron {len(classes)} clases:")
    print()

    valid_extensions = {'.jpg', '.jpeg', '.png'}
    all_valid = True

    for class_name in sorted(classes):
        class_dir = os.path.join(data_dir, class_name)
        images = [f for f in os.listdir(class_dir)
                 if os.path.splitext(f)[1].lower() in valid_extensions]

        num_images = len(images)
        status = "✓" if num_images >= min_images_per_class else "⚠"

        print(f"  {status} {class_name:25} - {num_images:4} imágenes")

        if num_images < min_images_per_class:
            all_valid = False
            print(f"      Advertencia: Menos de {min_images_per_class} imágenes")

    print()
    if all_valid:
        print("✓ Dataset válido - Todas las clases tienen suficientes imágenes")
    else:
        print("⚠ Advertencia: Algunas clases tienen pocas imágenes")
        print(f"  Se recomienda al menos {min_images_per_class} imágenes por clase")

    return all_valid


def organize_dataset(source_dir: str,
                    target_dir: str,
                    file_extensions: List[str] = None) -> None:
    """
    Organiza un dataset en la estructura correcta.

    Args:
        source_dir: Directorio fuente con imágenes
        target_dir: Directorio destino organizado
        file_extensions: Extensiones de archivo permitidas
    """
    if file_extensions is None:
        file_extensions = ['.jpg', '.jpeg', '.png']

    print(f"Organizando dataset de {source_dir} a {target_dir}...")

    if not os.path.exists(source_dir):
        print(f"Error: {source_dir} no existe")
        return

    os.makedirs(target_dir, exist_ok=True)

    # Buscar todas las imágenes
    all_images = []
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in file_extensions):
                all_images.append(os.path.join(root, file))

    print(f"Encontradas {len(all_images)} imágenes")

    # Copiar imágenes manteniendo la estructura
    for img_path in tqdm(all_images, desc="Copiando imágenes"):
        # Obtener el nombre de la clase (carpeta padre)
        class_name = os.path.basename(os.path.dirname(img_path))

        # Crear directorio de clase si no existe
        class_dir = os.path.join(target_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)

        # Copiar imagen
        target_path = os.path.join(class_dir, os.path.basename(img_path))
        shutil.copy2(img_path, target_path)

    print(f"✓ Dataset organizado en {target_dir}")


def create_sample_structure(output_dir: str = "data/raw") -> None:
    """
    Crea una estructura de carpetas de ejemplo para el dataset.

    Args:
        output_dir: Directorio de salida
    """
    sample_classes = [
        "aloe_vera",
        "manzanilla",
        "menta",
        "lavanda",
        "romero",
        "jengibre",
        "calendula",
        "eucalipto",
        "equinacea",
        "valeriana"
    ]

    print("Creando estructura de carpetas de ejemplo...")

    for class_name in sample_classes:
        class_dir = os.path.join(output_dir, class_name)
        os.makedirs(class_dir, exist_ok=True)

    print(f"✓ Estructura creada en {output_dir}")
    print(f"  Ahora coloca imágenes en cada carpeta de clase")
    print(f"  Clases creadas: {', '.join(sample_classes)}")


if __name__ == "__main__":
    # Ejemplo de uso
    download_sample_dataset()
    validate_dataset("data/raw")
