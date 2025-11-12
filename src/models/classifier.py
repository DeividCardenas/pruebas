"""
Definición de modelos de clasificación usando Transfer Learning.

Soporta:
- MobileNetV2 (recomendado para CPU)
- ResNet50
- EfficientNet-B0
"""

import torch
import torch.nn as nn
import torchvision.models as models
from typing import Optional


class MedicinalPlantClassifier(nn.Module):
    """
    Clasificador de plantas medicinales usando Transfer Learning.

    Args:
        num_classes: Número de clases de plantas
        architecture: Arquitectura base ('mobilenet_v2', 'resnet50', 'efficientnet_b0')
        pretrained: Si True, usa pesos pre-entrenados en ImageNet
        dropout: Tasa de dropout
        freeze_ratio: Proporción de capas a congelar (0.0 a 1.0)
    """

    def __init__(self,
                 num_classes: int,
                 architecture: str = 'mobilenet_v2',
                 pretrained: bool = True,
                 dropout: float = 0.5,
                 freeze_ratio: float = 0.7):
        super(MedicinalPlantClassifier, self).__init__()

        self.num_classes = num_classes
        self.architecture = architecture

        # Seleccionar arquitectura base
        if architecture == 'mobilenet_v2':
            self.model = models.mobilenet_v2(pretrained=pretrained)
            num_features = self.model.classifier[1].in_features

            # Reemplazar clasificador
            self.model.classifier = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(num_features, num_classes)
            )

        elif architecture == 'resnet50':
            self.model = models.resnet50(pretrained=pretrained)
            num_features = self.model.fc.in_features

            # Reemplazar capa fully connected
            self.model.fc = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(num_features, num_classes)
            )

        elif architecture == 'efficientnet_b0':
            self.model = models.efficientnet_b0(pretrained=pretrained)
            num_features = self.model.classifier[1].in_features

            # Reemplazar clasificador
            self.model.classifier = nn.Sequential(
                nn.Dropout(p=dropout),
                nn.Linear(num_features, num_classes)
            )

        else:
            raise ValueError(f"Arquitectura '{architecture}' no soportada. "
                           f"Use: 'mobilenet_v2', 'resnet50', o 'efficientnet_b0'")

        # Congelar capas si se especifica
        if freeze_ratio > 0:
            self._freeze_layers(freeze_ratio)

    def _freeze_layers(self, freeze_ratio: float):
        """
        Congela una proporción de las capas del modelo.

        Args:
            freeze_ratio: Proporción de capas a congelar (0.0 a 1.0)
        """
        # Obtener todos los parámetros
        all_params = list(self.model.parameters())
        num_to_freeze = int(len(all_params) * freeze_ratio)

        # Congelar los primeros parámetros
        for param in all_params[:num_to_freeze]:
            param.requires_grad = False

        print(f"✓ Congeladas {num_to_freeze}/{len(all_params)} capas ({freeze_ratio*100:.1f}%)")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass del modelo.

        Args:
            x: Tensor de entrada [batch_size, 3, H, W]

        Returns:
            Tensor de salida [batch_size, num_classes]
        """
        return self.model(x)

    def unfreeze_all(self):
        """Descongela todas las capas del modelo."""
        for param in self.model.parameters():
            param.requires_grad = True
        print("✓ Todas las capas descongeladas")

    def get_trainable_params(self) -> int:
        """Retorna el número de parámetros entrenables."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def get_total_params(self) -> int:
        """Retorna el número total de parámetros."""
        return sum(p.numel() for p in self.parameters())

    def summary(self):
        """Imprime un resumen del modelo."""
        print(f"\n{'='*70}")
        print(f"Resumen del Modelo: {self.architecture}")
        print(f"{'='*70}")
        print(f"Arquitectura base: {self.architecture}")
        print(f"Número de clases: {self.num_classes}")
        print(f"Parámetros totales: {self.get_total_params():,}")
        print(f"Parámetros entrenables: {self.get_trainable_params():,}")
        print(f"Parámetros congelados: {self.get_total_params() - self.get_trainable_params():,}")
        print(f"{'='*70}\n")


def create_model(num_classes: int,
                architecture: str = 'mobilenet_v2',
                pretrained: bool = True,
                dropout: float = 0.5,
                freeze_ratio: float = 0.7,
                device: str = 'cpu') -> MedicinalPlantClassifier:
    """
    Crea y configura un modelo de clasificación.

    Args:
        num_classes: Número de clases
        architecture: Arquitectura ('mobilenet_v2', 'resnet50', 'efficientnet_b0')
        pretrained: Usar pesos pre-entrenados
        dropout: Tasa de dropout
        freeze_ratio: Proporción de capas a congelar
        device: Dispositivo ('cpu' o 'cuda')

    Returns:
        Modelo configurado
    """
    print(f"\nCreando modelo {architecture}...")

    # Crear modelo
    model = MedicinalPlantClassifier(
        num_classes=num_classes,
        architecture=architecture,
        pretrained=pretrained,
        dropout=dropout,
        freeze_ratio=freeze_ratio
    )

    # Mover a dispositivo
    model = model.to(device)

    # Mostrar resumen
    model.summary()

    return model


def load_pretrained_model(checkpoint_path: str,
                         num_classes: int,
                         architecture: str = 'mobilenet_v2',
                         device: str = 'cpu') -> MedicinalPlantClassifier:
    """
    Carga un modelo desde un checkpoint.

    Args:
        checkpoint_path: Ruta al checkpoint
        num_classes: Número de clases
        architecture: Arquitectura del modelo
        device: Dispositivo

    Returns:
        Modelo cargado
    """
    # Crear modelo
    model = MedicinalPlantClassifier(
        num_classes=num_classes,
        architecture=architecture,
        pretrained=False
    )

    # Cargar pesos
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])

    # Mover a dispositivo
    model = model.to(device)

    print(f"✓ Modelo cargado desde: {checkpoint_path}")

    return model


if __name__ == "__main__":
    # Ejemplo de uso
    print("Ejemplo de uso:")
    print()

    # Crear modelo
    model = create_model(
        num_classes=10,
        architecture='mobilenet_v2',
        pretrained=True,
        dropout=0.5,
        freeze_ratio=0.7,
        device='cpu'
    )

    # Probar forward pass
    dummy_input = torch.randn(1, 3, 224, 224)
    output = model(dummy_input)
    print(f"Input shape: {dummy_input.shape}")
    print(f"Output shape: {output.shape}")
