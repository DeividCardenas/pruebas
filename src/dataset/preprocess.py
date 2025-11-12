"""
Módulo de preprocesamiento de imágenes para plantas medicinales.

Incluye:
- Transformaciones de datos
- Data augmentation
- División en train/val/test
"""

import os
import shutil
import random
from pathlib import Path
from typing import Tuple, Dict, List
from PIL import Image
import torch
from torchvision import transforms
from tqdm import tqdm


def get_transforms(image_size: int = 224,
                   augment: bool = True) -> Dict[str, transforms.Compose]:
    """
    Crea transformaciones para entrenamiento y validación.

    Args:
        image_size: Tamaño de la imagen de salida
        augment: Si True, aplica data augmentation para entrenamiento

    Returns:
        Diccionario con 'train' y 'val' transforms
    """
    # Normalización estándar de ImageNet (usada en modelos pre-entrenados)
    normalize = transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )

    if augment:
        # Transformaciones para ENTRENAMIENTO (con data augmentation)
        train_transforms = transforms.Compose([
            transforms.Resize((image_size + 32, image_size + 32)),
            transforms.RandomCrop(image_size),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=15),
            transforms.ColorJitter(
                brightness=0.2,
                contrast=0.2,
                saturation=0.2,
                hue=0.1
            ),
            transforms.RandomAffine(
                degrees=0,
                translate=(0.1, 0.1),
                scale=(0.9, 1.1)
            ),
            transforms.ToTensor(),
            normalize
        ])
    else:
        train_transforms = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            normalize
        ])

    # Transformaciones para VALIDACIÓN/TEST (sin augmentation)
    val_transforms = transforms.Compose([
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        normalize
    ])

    return {
        'train': train_transforms,
        'val': val_transforms,
        'test': val_transforms
    }


def create_data_splits(source_dir: str,
                      output_dir: str,
                      train_ratio: float = 0.7,
                      val_ratio: float = 0.15,
                      test_ratio: float = 0.15,
                      seed: int = 42) -> None:
    """
    Divide el dataset en conjuntos de entrenamiento, validación y test.

    Args:
        source_dir: Directorio con datos organizados por clase
        output_dir: Directorio de salida para los splits
        train_ratio: Proporción para entrenamiento
        val_ratio: Proporción para validación
        test_ratio: Proporción para test
        seed: Semilla para reproducibilidad
    """
    assert abs(train_ratio + val_ratio + test_ratio - 1.0) < 1e-6, \
        "Las proporciones deben sumar 1.0"

    random.seed(seed)

    print(f"\nDividiendo dataset en Train/Val/Test...")
    print(f"  Train: {train_ratio*100:.1f}%")
    print(f"  Val:   {val_ratio*100:.1f}%")
    print(f"  Test:  {test_ratio*100:.1f}%")
    print()

    # Obtener clases
    classes = [d for d in os.listdir(source_dir)
              if os.path.isdir(os.path.join(source_dir, d)) and not d.startswith('.')]

    if len(classes) == 0:
        print(f"Error: No se encontraron clases en {source_dir}")
        return

    # Crear directorios de salida
    for split in ['train', 'val', 'test']:
        for class_name in classes:
            os.makedirs(os.path.join(output_dir, split, class_name), exist_ok=True)

    # Estadísticas
    stats = {'train': 0, 'val': 0, 'test': 0}

    # Procesar cada clase
    for class_name in tqdm(classes, desc="Procesando clases"):
        class_dir = os.path.join(source_dir, class_name)

        # Obtener todas las imágenes
        valid_extensions = {'.jpg', '.jpeg', '.png'}
        images = [f for f in os.listdir(class_dir)
                 if os.path.splitext(f)[1].lower() in valid_extensions]

        # Mezclar aleatoriamente
        random.shuffle(images)

        # Calcular índices de división
        n_total = len(images)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)

        # Dividir imágenes
        train_images = images[:n_train]
        val_images = images[n_train:n_train + n_val]
        test_images = images[n_train + n_val:]

        # Copiar imágenes a los directorios correspondientes
        for img in train_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(output_dir, 'train', class_name, img)
            shutil.copy2(src, dst)
            stats['train'] += 1

        for img in val_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(output_dir, 'val', class_name, img)
            shutil.copy2(src, dst)
            stats['val'] += 1

        for img in test_images:
            src = os.path.join(class_dir, img)
            dst = os.path.join(output_dir, 'test', class_name, img)
            shutil.copy2(src, dst)
            stats['test'] += 1

    print(f"\n✓ Dataset dividido exitosamente:")
    print(f"  Train: {stats['train']} imágenes")
    print(f"  Val:   {stats['val']} imágenes")
    print(f"  Test:  {stats['test']} imágenes")
    print(f"  Total: {sum(stats.values())} imágenes")
    print(f"\nDatos guardados en: {output_dir}")


def verify_images(data_dir: str, fix_corrupted: bool = False) -> Tuple[int, int]:
    """
    Verifica que todas las imágenes se puedan abrir correctamente.

    Args:
        data_dir: Directorio con imágenes
        fix_corrupted: Si True, elimina imágenes corruptas

    Returns:
        Tupla (imágenes válidas, imágenes corruptas)
    """
    print(f"\nVerificando imágenes en {data_dir}...")

    valid_count = 0
    corrupted_count = 0
    corrupted_files = []

    valid_extensions = {'.jpg', '.jpeg', '.png'}

    # Recorrer todos los archivos
    for root, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.splitext(file)[1].lower() in valid_extensions:
                file_path = os.path.join(root, file)

                try:
                    # Intentar abrir y verificar la imagen
                    img = Image.open(file_path)
                    img.verify()  # Verifica que no esté corrupta
                    img.close()

                    # Re-abrir para verificar que se puede cargar
                    img = Image.open(file_path)
                    img.load()
                    img.close()

                    valid_count += 1

                except Exception as e:
                    corrupted_count += 1
                    corrupted_files.append(file_path)
                    print(f"  ⚠ Imagen corrupta: {file_path}")

                    if fix_corrupted:
                        os.remove(file_path)
                        print(f"    → Eliminada")

    print(f"\n✓ Verificación completa:")
    print(f"  Válidas:   {valid_count}")
    print(f"  Corruptas: {corrupted_count}")

    if corrupted_count > 0 and not fix_corrupted:
        print(f"\n  Ejecuta con fix_corrupted=True para eliminar imágenes corruptas")

    return valid_count, corrupted_count


def analyze_dataset(data_dir: str) -> Dict:
    """
    Analiza y muestra estadísticas del dataset.

    Args:
        data_dir: Directorio del dataset

    Returns:
        Diccionario con estadísticas
    """
    print(f"\nAnalizando dataset en {data_dir}...")
    print("=" * 70)

    classes = [d for d in os.listdir(data_dir)
              if os.path.isdir(os.path.join(data_dir, d)) and not d.startswith('.')]

    stats = {
        'num_classes': len(classes),
        'classes': {},
        'total_images': 0,
        'min_images': float('inf'),
        'max_images': 0
    }

    valid_extensions = {'.jpg', '.jpeg', '.png'}

    for class_name in sorted(classes):
        class_dir = os.path.join(data_dir, class_name)
        images = [f for f in os.listdir(class_dir)
                 if os.path.splitext(f)[1].lower() in valid_extensions]

        num_images = len(images)
        stats['classes'][class_name] = num_images
        stats['total_images'] += num_images
        stats['min_images'] = min(stats['min_images'], num_images)
        stats['max_images'] = max(stats['max_images'], num_images)

    # Mostrar estadísticas
    print(f"Número de clases: {stats['num_classes']}")
    print(f"Total de imágenes: {stats['total_images']}")
    print(f"Promedio por clase: {stats['total_images'] / stats['num_classes']:.1f}")
    print(f"Mínimo por clase: {stats['min_images']}")
    print(f"Máximo por clase: {stats['max_images']}")
    print()
    print("Distribución por clase:")
    print("-" * 70)

    for class_name, count in sorted(stats['classes'].items(), key=lambda x: x[1], reverse=True):
        bar_length = int(50 * count / stats['max_images'])
        bar = '█' * bar_length
        print(f"  {class_name:25} {count:4} {bar}")

    print("=" * 70)

    return stats


if __name__ == "__main__":
    # Ejemplo de uso
    print("Ejemplo de transformaciones:")
    transforms_dict = get_transforms(image_size=224, augment=True)
    print(f"Train transforms: {transforms_dict['train']}")
    print(f"Val transforms: {transforms_dict['val']}")
