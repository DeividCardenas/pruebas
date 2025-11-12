"""
Clase Dataset personalizada para plantas medicinales usando PyTorch.
"""

import os
from typing import Tuple, Optional, Callable, List
from PIL import Image
import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms


class MedicinalPlantsDataset(Dataset):
    """
    Dataset personalizado para clasificación de plantas medicinales.

    Args:
        data_dir: Directorio con imágenes organizadas por clase
        transform: Transformaciones a aplicar a las imágenes
        class_names: Lista de nombres de clases (opcional)
    """

    def __init__(self,
                 data_dir: str,
                 transform: Optional[Callable] = None,
                 class_names: Optional[List[str]] = None):
        self.data_dir = data_dir
        self.transform = transform

        # Obtener clases
        if class_names is None:
            self.class_names = sorted([d for d in os.listdir(data_dir)
                                      if os.path.isdir(os.path.join(data_dir, d))
                                      and not d.startswith('.')])
        else:
            self.class_names = class_names

        self.class_to_idx = {cls_name: i for i, cls_name in enumerate(self.class_names)}
        self.idx_to_class = {i: cls_name for cls_name, i in self.class_to_idx.items()}

        # Cargar lista de imágenes
        self.samples = []
        self._load_samples()

    def _load_samples(self):
        """Carga la lista de todas las imágenes y sus etiquetas."""
        valid_extensions = {'.jpg', '.jpeg', '.png'}

        for class_name in self.class_names:
            class_dir = os.path.join(self.data_dir, class_name)

            if not os.path.exists(class_dir):
                continue

            class_idx = self.class_to_idx[class_name]

            for img_name in os.listdir(class_dir):
                if os.path.splitext(img_name)[1].lower() in valid_extensions:
                    img_path = os.path.join(class_dir, img_name)
                    self.samples.append((img_path, class_idx))

    def __len__(self) -> int:
        """Retorna el número total de imágenes."""
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        """
        Obtiene una imagen y su etiqueta.

        Args:
            idx: Índice de la muestra

        Returns:
            Tupla (imagen, etiqueta)
        """
        img_path, label = self.samples[idx]

        # Cargar imagen
        try:
            image = Image.open(img_path).convert('RGB')
        except Exception as e:
            print(f"Error cargando imagen {img_path}: {e}")
            # Retornar imagen en negro en caso de error
            image = Image.new('RGB', (224, 224), color='black')

        # Aplicar transformaciones
        if self.transform:
            image = self.transform(image)

        return image, label

    def get_class_distribution(self) -> dict:
        """Retorna la distribución de clases en el dataset."""
        distribution = {class_name: 0 for class_name in self.class_names}

        for _, label in self.samples:
            class_name = self.idx_to_class[label]
            distribution[class_name] += 1

        return distribution

    def __repr__(self) -> str:
        """Representación en string del dataset."""
        return (f"MedicinalPlantsDataset(\n"
                f"  Samples: {len(self.samples)}\n"
                f"  Classes: {len(self.class_names)}\n"
                f"  Class names: {', '.join(self.class_names[:5])}{'...' if len(self.class_names) > 5 else ''}\n"
                f")")


def create_dataloaders(train_dir: str,
                      val_dir: str,
                      test_dir: str,
                      batch_size: int = 32,
                      image_size: int = 224,
                      num_workers: int = 4,
                      augment: bool = True) -> Tuple[DataLoader, DataLoader, DataLoader, List[str]]:
    """
    Crea DataLoaders para entrenamiento, validación y test.

    Args:
        train_dir: Directorio de entrenamiento
        val_dir: Directorio de validación
        test_dir: Directorio de test
        batch_size: Tamaño del batch
        image_size: Tamaño de las imágenes
        num_workers: Número de workers para carga de datos
        augment: Si True, aplica data augmentation

    Returns:
        Tupla (train_loader, val_loader, test_loader, class_names)
    """
    from .preprocess import get_transforms

    # Obtener transformaciones
    transforms_dict = get_transforms(image_size=image_size, augment=augment)

    # Crear datasets
    train_dataset = MedicinalPlantsDataset(
        data_dir=train_dir,
        transform=transforms_dict['train']
    )

    val_dataset = MedicinalPlantsDataset(
        data_dir=val_dir,
        transform=transforms_dict['val'],
        class_names=train_dataset.class_names  # Usar las mismas clases
    )

    test_dataset = MedicinalPlantsDataset(
        data_dir=test_dir,
        transform=transforms_dict['test'],
        class_names=train_dataset.class_names
    )

    # Crear DataLoaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    print(f"\n{'='*70}")
    print(f"DataLoaders creados:")
    print(f"{'='*70}")
    print(f"Train: {len(train_dataset)} imágenes ({len(train_loader)} batches)")
    print(f"Val:   {len(val_dataset)} imágenes ({len(val_loader)} batches)")
    print(f"Test:  {len(test_dataset)} imágenes ({len(test_loader)} batches)")
    print(f"Batch size: {batch_size}")
    print(f"Clases: {len(train_dataset.class_names)}")
    print(f"{'='*70}\n")

    return train_loader, val_loader, test_loader, train_dataset.class_names


if __name__ == "__main__":
    # Ejemplo de uso
    print("Ejemplo de uso de MedicinalPlantsDataset:")
    print()
    print("from src.dataset.dataset import MedicinalPlantsDataset, create_dataloaders")
    print()
    print("# Crear dataset")
    print("dataset = MedicinalPlantsDataset(")
    print("    data_dir='data/processed/train',")
    print("    transform=transforms.ToTensor()")
    print(")")
    print()
    print("# O crear DataLoaders completos")
    print("train_loader, val_loader, test_loader, class_names = create_dataloaders(")
    print("    train_dir='data/processed/train',")
    print("    val_dir='data/processed/val',")
    print("    test_dir='data/processed/test',")
    print("    batch_size=32")
    print(")")
