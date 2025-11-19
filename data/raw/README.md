# Dataset de Plantas Medicinales

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
