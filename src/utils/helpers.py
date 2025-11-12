"""
Funciones auxiliares para el proyecto de clasificación de plantas medicinales.
"""

import os
import json
import yaml
import torch
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import confusion_matrix
from typing import Dict, List, Any, Optional


def load_config(config_path: str = "config/config.yaml") -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo YAML.

    Args:
        config_path: Ruta al archivo de configuración

    Returns:
        Diccionario con la configuración
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    return config


def load_plants_info(json_path: str = "data/plantas_info.json") -> Dict[str, Any]:
    """
    Carga la información de plantas medicinales desde JSON.

    Args:
        json_path: Ruta al archivo JSON con información de plantas

    Returns:
        Diccionario con información de las plantas
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        plants_info = json.load(f)
    return plants_info


def get_class_names(data_dir: str) -> List[str]:
    """
    Obtiene los nombres de las clases desde el directorio de datos.

    Args:
        data_dir: Directorio que contiene las carpetas de clases

    Returns:
        Lista ordenada de nombres de clases
    """
    class_names = sorted([d for d in os.listdir(data_dir)
                         if os.path.isdir(os.path.join(data_dir, d))])
    return class_names


def create_confusion_matrix(y_true: np.ndarray,
                           y_pred: np.ndarray,
                           class_names: List[str],
                           save_path: Optional[str] = None,
                           figsize: tuple = (12, 10)) -> None:
    """
    Crea y visualiza una matriz de confusión.

    Args:
        y_true: Etiquetas verdaderas
        y_pred: Predicciones del modelo
        class_names: Nombres de las clases
        save_path: Ruta para guardar la figura (opcional)
        figsize: Tamaño de la figura
    """
    cm = confusion_matrix(y_true, y_pred)

    plt.figure(figsize=figsize)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Matriz de Confusión - Clasificación de Plantas Medicinales')
    plt.ylabel('Etiqueta Verdadera')
    plt.xlabel('Predicción')
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Matriz de confusión guardada en: {save_path}")

    plt.show()


def plot_training_history(history: Dict[str, List[float]],
                          save_path: Optional[str] = None) -> None:
    """
    Visualiza el historial de entrenamiento (pérdida y precisión).

    Args:
        history: Diccionario con listas de métricas por época
        save_path: Ruta para guardar la figura (opcional)
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Pérdida
    ax1.plot(history['train_loss'], label='Train Loss', marker='o')
    ax1.plot(history['val_loss'], label='Validation Loss', marker='s')
    ax1.set_xlabel('Época')
    ax1.set_ylabel('Pérdida')
    ax1.set_title('Pérdida durante el Entrenamiento')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Precisión
    ax2.plot(history['train_acc'], label='Train Accuracy', marker='o')
    ax2.plot(history['val_acc'], label='Validation Accuracy', marker='s')
    ax2.set_xlabel('Época')
    ax2.set_ylabel('Precisión (%)')
    ax2.set_title('Precisión durante el Entrenamiento')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Gráfica de entrenamiento guardada en: {save_path}")

    plt.show()


def save_model_checkpoint(model: torch.nn.Module,
                         optimizer: torch.optim.Optimizer,
                         epoch: int,
                         loss: float,
                         accuracy: float,
                         class_names: List[str],
                         save_path: str) -> None:
    """
    Guarda un checkpoint del modelo.

    Args:
        model: Modelo PyTorch
        optimizer: Optimizador
        epoch: Número de época
        loss: Pérdida actual
        accuracy: Precisión actual
        class_names: Nombres de las clases
        save_path: Ruta donde guardar el checkpoint
    """
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss,
        'accuracy': accuracy,
        'class_names': class_names
    }

    # Crear directorio si no existe
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    torch.save(checkpoint, save_path)
    print(f"Checkpoint guardado en: {save_path}")


def load_model_checkpoint(model: torch.nn.Module,
                         checkpoint_path: str,
                         optimizer: Optional[torch.optim.Optimizer] = None,
                         device: str = 'cpu') -> Dict[str, Any]:
    """
    Carga un checkpoint del modelo.

    Args:
        model: Modelo PyTorch (arquitectura debe coincidir)
        checkpoint_path: Ruta al checkpoint
        optimizer: Optimizador (opcional)
        device: Dispositivo ('cpu' o 'cuda')

    Returns:
        Diccionario con información del checkpoint
    """
    checkpoint = torch.load(checkpoint_path, map_location=device)

    model.load_state_dict(checkpoint['model_state_dict'])

    if optimizer and 'optimizer_state_dict' in checkpoint:
        optimizer.load_state_dict(checkpoint['optimizer_state_dict'])

    print(f"Checkpoint cargado desde: {checkpoint_path}")
    print(f"  - Época: {checkpoint.get('epoch', 'N/A')}")
    print(f"  - Precisión: {checkpoint.get('accuracy', 'N/A'):.2f}%")

    return checkpoint


def calculate_class_weights(data_dir: str, class_names: List[str]) -> torch.Tensor:
    """
    Calcula pesos para clases desbalanceadas.

    Args:
        data_dir: Directorio con los datos
        class_names: Lista de nombres de clases

    Returns:
        Tensor con pesos para cada clase
    """
    class_counts = []

    for class_name in class_names:
        class_path = os.path.join(data_dir, class_name)
        if os.path.exists(class_path):
            count = len([f for f in os.listdir(class_path)
                        if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
            class_counts.append(count)
        else:
            class_counts.append(0)

    total = sum(class_counts)
    weights = [total / (len(class_names) * count) if count > 0 else 0
               for count in class_counts]

    return torch.FloatTensor(weights)


def format_time(seconds: float) -> str:
    """
    Formatea segundos a una cadena legible.

    Args:
        seconds: Tiempo en segundos

    Returns:
        Cadena formateada (ej: "2h 30m 15s")
    """
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)

    if h > 0:
        return f"{h}h {m}m {s}s"
    elif m > 0:
        return f"{m}m {s}s"
    else:
        return f"{s}s"
