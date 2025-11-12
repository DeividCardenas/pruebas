"""
Script de entrenamiento del modelo de clasificación de plantas medicinales.

Incluye:
- Entrenamiento con Transfer Learning
- Early stopping
- Guardado de checkpoints
- Logging de métricas
- Visualización de progreso
"""

import os
import time
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from typing import Dict, List, Tuple, Optional
from tqdm import tqdm
import numpy as np


class EarlyStopping:
    """
    Early stopping para detener el entrenamiento cuando la validación no mejora.

    Args:
        patience: Número de épocas a esperar antes de detener
        min_delta: Mínima mejora requerida
        mode: 'min' para pérdida, 'max' para accuracy
    """

    def __init__(self, patience: int = 10, min_delta: float = 0, mode: str = 'min'):
        self.patience = patience
        self.min_delta = min_delta
        self.mode = mode
        self.counter = 0
        self.best_score = None
        self.early_stop = False

    def __call__(self, score: float) -> bool:
        """
        Verifica si se debe detener el entrenamiento.

        Args:
            score: Métrica actual (pérdida o accuracy)

        Returns:
            True si se debe detener, False en caso contrario
        """
        if self.best_score is None:
            self.best_score = score
            return False

        if self.mode == 'min':
            improved = score < (self.best_score - self.min_delta)
        else:  # mode == 'max'
            improved = score > (self.best_score + self.min_delta)

        if improved:
            self.best_score = score
            self.counter = 0
        else:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True

        return self.early_stop


def train_epoch(model: nn.Module,
                dataloader: DataLoader,
                criterion: nn.Module,
                optimizer: optim.Optimizer,
                device: str) -> Tuple[float, float]:
    """
    Entrena el modelo por una época.

    Args:
        model: Modelo a entrenar
        dataloader: DataLoader de entrenamiento
        criterion: Función de pérdida
        optimizer: Optimizador
        device: Dispositivo ('cpu' o 'cuda')

    Returns:
        Tupla (pérdida promedio, accuracy)
    """
    model.train()

    running_loss = 0.0
    correct = 0
    total = 0

    pbar = tqdm(dataloader, desc='Training', leave=False)

    for inputs, labels in pbar:
        inputs = inputs.to(device)
        labels = labels.to(device)

        # Zero gradients
        optimizer.zero_grad()

        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)

        # Backward pass
        loss.backward()
        optimizer.step()

        # Estadísticas
        running_loss += loss.item() * inputs.size(0)
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()

        # Actualizar progress bar
        pbar.set_postfix({
            'loss': f'{loss.item():.4f}',
            'acc': f'{100.*correct/total:.2f}%'
        })

    epoch_loss = running_loss / total
    epoch_acc = 100. * correct / total

    return epoch_loss, epoch_acc


def validate_epoch(model: nn.Module,
                   dataloader: DataLoader,
                   criterion: nn.Module,
                   device: str) -> Tuple[float, float]:
    """
    Valida el modelo en el conjunto de validación.

    Args:
        model: Modelo a validar
        dataloader: DataLoader de validación
        criterion: Función de pérdida
        device: Dispositivo

    Returns:
        Tupla (pérdida promedio, accuracy)
    """
    model.eval()

    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        pbar = tqdm(dataloader, desc='Validation', leave=False)

        for inputs, labels in pbar:
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)

            # Estadísticas
            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

            # Actualizar progress bar
            pbar.set_postfix({
                'loss': f'{loss.item():.4f}',
                'acc': f'{100.*correct/total:.2f}%'
            })

    epoch_loss = running_loss / total
    epoch_acc = 100. * correct / total

    return epoch_loss, epoch_acc


def train_model(model: nn.Module,
                train_loader: DataLoader,
                val_loader: DataLoader,
                criterion: nn.Module,
                optimizer: optim.Optimizer,
                num_epochs: int,
                device: str,
                scheduler: Optional[optim.lr_scheduler._LRScheduler] = None,
                early_stopping: Optional[EarlyStopping] = None,
                checkpoint_dir: str = 'models/checkpoints',
                class_names: Optional[List[str]] = None) -> Dict[str, List[float]]:
    """
    Entrena el modelo completo.

    Args:
        model: Modelo a entrenar
        train_loader: DataLoader de entrenamiento
        val_loader: DataLoader de validación
        criterion: Función de pérdida
        optimizer: Optimizador
        num_epochs: Número de épocas
        device: Dispositivo
        scheduler: Learning rate scheduler (opcional)
        early_stopping: EarlyStopping (opcional)
        checkpoint_dir: Directorio para guardar checkpoints
        class_names: Nombres de las clases

    Returns:
        Diccionario con historial de entrenamiento
    """
    print(f"\n{'='*70}")
    print(f"Iniciando entrenamiento")
    print(f"{'='*70}")
    print(f"Épocas: {num_epochs}")
    print(f"Dispositivo: {device}")
    print(f"Learning rate: {optimizer.param_groups[0]['lr']}")
    print(f"Batch size: {train_loader.batch_size}")
    print(f"{'='*70}\n")

    # Crear directorio de checkpoints
    os.makedirs(checkpoint_dir, exist_ok=True)

    # Historial de entrenamiento
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': [],
        'learning_rates': []
    }

    best_val_acc = 0.0
    best_epoch = 0
    start_time = time.time()

    for epoch in range(num_epochs):
        epoch_start = time.time()

        print(f"\nÉpoca [{epoch+1}/{num_epochs}]")
        print("-" * 70)

        # Entrenamiento
        train_loss, train_acc = train_epoch(
            model, train_loader, criterion, optimizer, device
        )

        # Validación
        val_loss, val_acc = validate_epoch(
            model, val_loader, criterion, device
        )

        # Actualizar scheduler
        if scheduler is not None:
            if isinstance(scheduler, optim.lr_scheduler.ReduceLROnPlateau):
                scheduler.step(val_loss)
            else:
                scheduler.step()

        # Guardar historial
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        history['learning_rates'].append(optimizer.param_groups[0]['lr'])

        # Calcular tiempo
        epoch_time = time.time() - epoch_start

        # Imprimir resultados
        print(f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}%")
        print(f"Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.2f}%")
        print(f"LR: {optimizer.param_groups[0]['lr']:.6f} | Tiempo: {epoch_time:.1f}s")

        # Guardar mejor modelo
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_epoch = epoch + 1

            checkpoint_path = os.path.join(checkpoint_dir, 'best_model.pth')
            torch.save({
                'epoch': epoch + 1,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'val_loss': val_loss,
                'class_names': class_names
            }, checkpoint_path)

            print(f"✓ Mejor modelo guardado (Val Acc: {val_acc:.2f}%)")

        # Early stopping
        if early_stopping is not None:
            if early_stopping(val_loss):
                print(f"\n⚠ Early stopping activado en época {epoch+1}")
                break

    # Tiempo total
    total_time = time.time() - start_time
    hours = int(total_time // 3600)
    minutes = int((total_time % 3600) // 60)
    seconds = int(total_time % 60)

    print(f"\n{'='*70}")
    print(f"Entrenamiento completado")
    print(f"{'='*70}")
    print(f"Tiempo total: {hours}h {minutes}m {seconds}s")
    print(f"Mejor Val Acc: {best_val_acc:.2f}% (Época {best_epoch})")
    print(f"{'='*70}\n")

    return history


def evaluate_model(model: nn.Module,
                   test_loader: DataLoader,
                   device: str,
                   class_names: Optional[List[str]] = None) -> Dict:
    """
    Evalúa el modelo en el conjunto de test.

    Args:
        model: Modelo a evaluar
        test_loader: DataLoader de test
        device: Dispositivo
        class_names: Nombres de las clases

    Returns:
        Diccionario con métricas de evaluación
    """
    model.eval()

    all_predictions = []
    all_labels = []
    correct = 0
    total = 0

    print(f"\n{'='*70}")
    print(f"Evaluando modelo en conjunto de Test")
    print(f"{'='*70}\n")

    with torch.no_grad():
        for inputs, labels in tqdm(test_loader, desc='Testing'):
            inputs = inputs.to(device)
            labels = labels.to(device)

            outputs = model(inputs)
            _, predicted = outputs.max(1)

            all_predictions.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

    # Calcular accuracy
    accuracy = 100. * correct / total

    # Calcular métricas por clase
    from sklearn.metrics import classification_report, confusion_matrix

    all_predictions = np.array(all_predictions)
    all_labels = np.array(all_labels)

    # Reporte de clasificación
    if class_names is not None:
        report = classification_report(
            all_labels,
            all_predictions,
            target_names=class_names,
            digits=4
        )
    else:
        report = classification_report(all_labels, all_predictions, digits=4)

    print(f"\n{'='*70}")
    print(f"Resultados de Evaluación")
    print(f"{'='*70}")
    print(f"Test Accuracy: {accuracy:.2f}%")
    print(f"\nReporte de Clasificación:")
    print(report)

    results = {
        'accuracy': accuracy,
        'predictions': all_predictions,
        'labels': all_labels,
        'classification_report': report
    }

    return results


if __name__ == "__main__":
    print("Módulo de entrenamiento")
    print("=" * 70)
    print("Este módulo contiene funciones para entrenar y evaluar modelos.")
    print()
    print("Uso típico:")
    print()
    print("from src.models.train import train_model, evaluate_model")
    print()
    print("history = train_model(")
    print("    model=model,")
    print("    train_loader=train_loader,")
    print("    val_loader=val_loader,")
    print("    criterion=criterion,")
    print("    optimizer=optimizer,")
    print("    num_epochs=50,")
    print("    device='cpu'")
    print(")")
