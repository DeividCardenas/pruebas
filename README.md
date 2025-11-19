# 🌿 Clasificador de Plantas Medicinales

Sistema de clasificación de plantas medicinales usando Transfer Learning con PyTorch y MobileNetV2.

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1.0-red.svg)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Tabla de Contenidos

- [Descripción](#descripción)
- [Características](#características)
- [Arquitectura del Proyecto](#arquitectura-del-proyecto)
- [Instalación](#instalación)
- [Uso Rápido](#uso-rápido)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Metodología](#metodología)
- [Resultados](#resultados)
- [Equipo](#equipo)
- [Documentación](#documentación)

## 🎯 Descripción

Sistema de clasificación automática de plantas medicinales basado en Visión Computacional y Deep Learning. El clasificador procesa imágenes de hojas y proporciona:

- Identificación de especie con 99 clases disponibles
- Top-3 predicciones con niveles de confianza
- Información sobre usos tradicionales y precauciones

Desarrollado como proyecto final para el curso de Inteligencia Artificial, este sistema aplica Transfer Learning con MobileNetV2 alcanzando 98.51% de accuracy en validación.

## ✨ Características

### Técnicas Implementadas

- Transfer Learning con MobileNetV2 (pesos pre-entrenados ImageNet)
- Data Augmentation con transformaciones geométricas y de color
- Early Stopping con patience de 10 épocas
- Learning Rate Scheduler (StepLR)
- Evaluación con matriz de confusión y métricas por clase

### Funcionalidades del Sistema

- Clasificación de 99 especies de plantas medicinales
- Predicciones con niveles de confianza (top-3)
- Base de datos con información medicinal tradicional
- Interfaz web construida con Flask
- Notebooks Jupyter para análisis y entrenamiento

## 🏗️ Arquitectura del Proyecto

```
medicinal-plants-classifier/
├── src/                    # Código fuente
│   ├── dataset/           # Manejo de datos
│   ├── models/            # Modelos y entrenamiento
│   └── utils/             # Utilidades
├── app/                   # Aplicación Flask
│   ├── templates/         # Plantillas HTML
│   └── static/           # CSS, JS, uploads
├── notebooks/             # Jupyter Notebooks
├── data/                  # Datos (raw y procesados)
├── models/                # Modelos entrenados
├── config/                # Configuración
└── docs/                  # Documentación
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git

### Pasos de Instalación

1. **Clonar el repositorio**

```bash
git clone https://github.com/tu-usuario/medicinal-plants-classifier.git
cd medicinal-plants-classifier
```

2. **Crear entorno virtual**

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

4. **Descargar dataset**

Opción A: Kaggle (Recomendado)
```bash
kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset
unzip indian-medicinal-leaves-dataset.zip -d data/raw/
```

Opción B: Organizar tu propio dataset en `data/raw/` siguiendo la estructura:
```
data/raw/
├── aloe_vera/
│   └── *.jpg
├── manzanilla/
│   └── *.jpg
└── ...
```

## 📖 Uso Rápido

### 1. Preparar Datos

```bash
jupyter notebook notebooks/01_exploracion_datos.ipynb
```

Este notebook te guiará para:
- Validar el dataset
- Analizar la distribución de clases
- Dividir en train/val/test

### 2. Entrenar Modelo

```bash
jupyter notebook notebooks/02_entrenamiento_modelo.ipynb
```

Entrena el modelo con:
- Transfer Learning (MobileNetV2)
- Data augmentation
- Early stopping

### 3. Evaluar Modelo

```bash
jupyter notebook notebooks/03_evaluacion_modelo.ipynb
```

Evalúa el modelo con:
- Métricas detalladas
- Matriz de confusión
- Análisis de errores

### 4. Ejecutar Aplicación Web

```bash
python app/app.py
```

Abre tu navegador en `http://localhost:5000` y prueba el clasificador.

## 🔬 Metodología

### 1. Recolección de Datos

- **Fuente**: Kaggle - Indian Medicinal Leaves Dataset
- **Clases**: 99 especies de plantas medicinales
- **Total de imágenes**: 19,546 imágenes
- **División**:
  - Train: 13,339 imágenes (68.2%)
  - Validation: 3,025 imágenes (15.5%)
  - Test: 3,182 imágenes (16.3%)

### 2. Preprocesamiento

- Resize a 224x224 (tamaño de entrada de MobileNetV2)
- Normalización con media y std de ImageNet
- Data Augmentation:
  - Random horizontal flip
  - Random rotation (±15°)
  - Color jitter (brightness, contrast, saturation)
  - Random affine transforms

### 3. Modelo

**Arquitectura**: MobileNetV2 (Transfer Learning)

- **Base**: MobileNetV2 pre-entrenado en ImageNet
- **Estrategia**: Fine-tuning con capas congeladas
- **Modificaciones**:
  - Congelar 70% de las capas base
  - Reemplazar clasificador final
  - Dropout (0.5) para regularización

**Justificación**:
- MobileNetV2 es ligero y eficiente (ideal para CPU)
- Pre-entrenado en ImageNet (buenas features para plantas)
- Excelente balance precisión/velocidad

### 4. Entrenamiento

- **Optimizador**: Adam (lr=0.001)
- **Loss**: CrossEntropyLoss
- **Batch Size**: 32
- **Épocas**: 50 (con early stopping)
- **Scheduler**: StepLR (reducción cada 10 épocas)
- **Early Stopping**: Patience de 10 épocas

### 5. Evaluación

- **Métricas**: Accuracy, Precision, Recall, F1-Score
- **Visualización**: Matriz de confusión, curvas de aprendizaje
- **Análisis**: Errores por clase, distribución de confianza

## 🧠 Arquitectura de la Red Neuronal

### Configuración del Modelo

El sistema utiliza **MobileNetV2** con Transfer Learning, aprovechando pesos pre-entrenados en ImageNet. Esta arquitectura fue seleccionada por su balance entre precisión y eficiencia computacional.

**Especificaciones técnicas:**

```python
# Arquitectura base
Base: MobileNetV2 (pre-trained on ImageNet)
Input shape: (batch_size, 3, 224, 224)

# Capas congeladas
Freeze ratio: 70% (primeras 110 de 158 capas)
Trainable layers: Últimas 48 capas + clasificador personalizado

# Clasificador personalizado
nn.Sequential(
    nn.Dropout(p=0.5),
    nn.Linear(in_features=1280, out_features=99)
)
```

**Distribución de parámetros:**

| Componente | Parámetros | Porcentaje |
|------------|------------|------------|
| Parámetros totales | 2,350,691 | 100% |
| Parámetros entrenables | 1,870,563 | 79.6% |
| Parámetros congelados | 480,128 | 20.4% |

### Hiperparámetros de Entrenamiento

```yaml
# Configuración principal
batch_size: 32
epochs: 50 (early stopping en 47)
learning_rate: 0.001
optimizer: Adam
loss_function: CrossEntropyLoss

# Learning Rate Scheduler
type: StepLR
step_size: 10  # Reduce LR cada 10 épocas
gamma: 0.1     # Factor de reducción

# Regularización
dropout: 0.5
weight_decay: 0
early_stopping_patience: 10
```

### Flujo de Datos

```
Imagen (RGB) → Resize(224x224) → Normalización → MobileNetV2 Features
→ Global Average Pooling → Dropout(0.5) → Linear(1280→99) → Softmax → Predicción
```

## 📊 Resultados

### Métricas de Rendimiento

| Métrica | Training | Validation | Gap |
|---------|----------|------------|-----|
| **Accuracy** | 99.54% | **98.51%** | 1.03% |
| **Loss** | 0.0178 | 0.0530 | - |

### Detalles del Entrenamiento

- Épocas entrenadas: 47 (early stopping activado)
- Arquitectura: MobileNetV2
- Parámetros totales: 2,350,691
- Parámetros entrenables: 1,870,563 (79.6%)
- Tiempo total: ~3 horas (CPU Intel/AMD)

### Rendimiento del Sistema

- Precisión en validación: 98.51%
- Gap train-validation: 1.03%
- Tiempo de inferencia: ~45ms por imagen (CPU)
- Clases soportadas: 99 especies

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+**
- **PyTorch 2.1.0**: Framework de Deep Learning
- **torchvision**: Modelos pre-entrenados y transformaciones
- **OpenCV**: Procesamiento de imágenes
- **Flask**: Framework web
- **Jupyter**: Notebooks interactivos
- **NumPy, Pandas**: Manipulación de datos
- **Matplotlib, Seaborn**: Visualización
- **scikit-learn**: Métricas de evaluación

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- Dataset: [Indian Medicinal Leaves Dataset](https://www.kaggle.com/datasets/aryashah2k/indian-medicinal-leaves-dataset)
- Arquitectura base: MobileNetV2 (Google)
- Framework: PyTorch (Meta AI)

## 📞 Contacto

Para preguntas o sugerencias, por favor abre un issue en este repositorio.

---

**Desarrollado con ❤️ para el curso de Inteligencia Artificial**
