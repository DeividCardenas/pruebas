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

Este proyecto implementa un sistema completo de clasificación de plantas medicinales utilizando técnicas avanzadas de Visión Computacional y Deep Learning. El sistema permite:

- **Clasificar** diferentes especies de plantas medicinales a partir de imágenes
- **Identificar** la planta y sugerir usos tradicionales
- **Proporcionar** información detallada sobre propiedades y precauciones

El proyecto fue desarrollado como trabajo final del curso de Visión Computacional, aplicando Transfer Learning con MobileNetV2 para obtener alta precisión incluso con datasets limitados.

## ✨ Características

### Técnicas

- ✅ **Transfer Learning** con MobileNetV2 pre-entrenado en ImageNet
- ✅ **Data Augmentation** para mejorar la generalización
- ✅ **Early Stopping** para evitar overfitting
- ✅ **Learning Rate Scheduling** para optimizar el entrenamiento
- ✅ **Matriz de Confusión** y métricas detalladas

### Funcionalidades

- 🌱 Clasificación de hasta 30+ especies de plantas medicinales
- 📊 Visualización de probabilidades y top-3 predicciones
- 💊 Base de conocimientos con usos tradicionales y precauciones
- 🌐 Interfaz web profesional con Flask
- 📓 Notebooks interactivos para experimentación

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

## 📁 Estructura del Proyecto

```
.
├── README.md                          # Este archivo
├── requirements.txt                   # Dependencias
├── .gitignore                        # Archivos ignorados por git
│
├── config/
│   └── config.yaml                   # Configuración del proyecto
│
├── src/                              # Código fuente
│   ├── __init__.py
│   ├── dataset/
│   │   ├── __init__.py
│   │   ├── download.py              # Descarga de datasets
│   │   ├── preprocess.py            # Preprocesamiento
│   │   └── dataset.py               # Dataset PyTorch
│   ├── models/
│   │   ├── __init__.py
│   │   ├── classifier.py            # Arquitectura del modelo
│   │   └── train.py                 # Entrenamiento
│   └── utils/
│       ├── __init__.py
│       └── helpers.py               # Funciones auxiliares
│
├── app/                              # Aplicación Flask
│   ├── __init__.py
│   ├── app.py                       # Backend Flask
│   ├── templates/
│   │   └── index.html               # Interfaz web
│   └── static/
│       ├── css/style.css            # Estilos
│       ├── js/main.js               # JavaScript
│       └── uploads/                 # Imágenes subidas
│
├── notebooks/                        # Jupyter Notebooks
│   ├── 01_exploracion_datos.ipynb
│   ├── 02_entrenamiento_modelo.ipynb
│   └── 03_evaluacion_modelo.ipynb
│
├── data/                             # Datos
│   ├── raw/                         # Datos originales
│   ├── processed/                   # Datos procesados
│   │   ├── train/
│   │   ├── val/
│   │   └── test/
│   └── plantas_info.json            # Info de plantas
│
├── models/                           # Modelos entrenados
│   ├── best_model.pth               # Mejor modelo
│   └── checkpoints/                 # Checkpoints
│
├── docs/                             # Documentación
│   ├── REPORTE_PROYECTO.md          # Reporte detallado
│   ├── PLAN_TRABAJO.md              # Plan de trabajo
│   └── PRESENTACION.md              # Outline de presentación
│
└── tests/                            # Tests unitarios
    └── __init__.py
```

## 🔬 Metodología

### 1. Recolección de Datos

- **Fuente**: Kaggle - Indian Medicinal Leaves Dataset
- **Clases**: 30+ especies de plantas medicinales
- **División**: 70% Train, 15% Validation, 15% Test

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

## 📊 Resultados

Los resultados varían según el dataset utilizado. Ejemplo con Indian Medicinal Leaves Dataset:

- **Test Accuracy**: ~92-95%
- **Precision promedio**: ~0.93
- **Recall promedio**: ~0.92
- **F1-Score promedio**: ~0.92

Ver `docs/REPORTE_PROYECTO.md` para resultados detallados.

## 👥 Equipo

- **Miembro 1**: Preprocesamiento de datos y dataset
- **Miembro 2**: Modelado y entrenamiento
- **Miembro 3**: Aplicación web y documentación

## 📚 Documentación

- [**Reporte del Proyecto**](docs/REPORTE_PROYECTO.md): Documento técnico completo
- [**Plan de Trabajo**](docs/PLAN_TRABAJO.md): Planificación de 2 semanas
- [**Presentación**](docs/PRESENTACION.md): Outline para la presentación final

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
