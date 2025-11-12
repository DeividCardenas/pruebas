"""
Aplicación Flask - Asistente de Clasificación de Plantas Medicinales

Esta aplicación web permite:
- Subir imágenes de plantas
- Clasificar la planta usando el modelo entrenado
- Mostrar información sobre usos tradicionales
"""

import os
import sys
import json
import yaml
from pathlib import Path
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import torchvision.transforms as transforms
from flask import Flask, render_template, request, jsonify, url_for

# Agregar el directorio raíz al path
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.models.classifier import MedicinalPlantClassifier

app = Flask(__name__)

# Configuración
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Variables globales
model = None
class_names = []
plants_info = {}
device = 'cpu'


def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_model_and_info():
    """Carga el modelo entrenado y la información de plantas."""
    global model, class_names, plants_info, device

    print("\n" + "="*70)
    print("Iniciando Asistente de Plantas Medicinales")
    print("="*70)

    # Configurar dispositivo
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Dispositivo: {device}")

    # Cargar información de plantas
    plants_info_path = ROOT_DIR / 'data' / 'plantas_info.json'
    if plants_info_path.exists():
        with open(plants_info_path, 'r', encoding='utf-8') as f:
            plants_info = json.load(f)
        print(f"✓ Información de plantas cargada: {len(plants_info.get('plantas_medicinales', {}))} plantas")
    else:
        print(f"⚠ Advertencia: No se encontró {plants_info_path}")

    # Cargar modelo
    model_path = ROOT_DIR / 'models' / 'best_model.pth'

    if model_path.exists():
        print(f"Cargando modelo desde: {model_path}")

        # Cargar checkpoint
        checkpoint = torch.load(model_path, map_location=device)
        class_names = checkpoint.get('class_names', [])

        if not class_names:
            print("⚠ Advertencia: No se encontraron nombres de clases en el checkpoint")
            return

        # Crear modelo
        model = MedicinalPlantClassifier(
            num_classes=len(class_names),
            architecture='mobilenet_v2',
            pretrained=False
        )

        # Cargar pesos
        model.load_state_dict(checkpoint['model_state_dict'])
        model.to(device)
        model.eval()

        print(f"✓ Modelo cargado exitosamente")
        print(f"  - Clases: {len(class_names)}")
        print(f"  - Accuracy de validación: {checkpoint.get('val_acc', 'N/A'):.2f}%")

    else:
        print(f"⚠ Advertencia: No se encontró el modelo en {model_path}")
        print(f"  Entrena un modelo primero usando el notebook de entrenamiento")

    print("="*70 + "\n")


def get_image_transforms():
    """Retorna las transformaciones para imágenes de predicción."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])


def predict_image(image_path):
    """
    Realiza la predicción sobre una imagen.

    Args:
        image_path: Ruta a la imagen

    Returns:
        Diccionario con predicción y probabilidades
    """
    if model is None:
        return {
            'error': 'Modelo no cargado. Entrena el modelo primero.',
            'success': False
        }

    try:
        # Cargar y transformar imagen
        image = Image.open(image_path).convert('RGB')
        transform = get_image_transforms()
        image_tensor = transform(image).unsqueeze(0).to(device)

        # Predicción
        with torch.no_grad():
            outputs = model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted_idx = probabilities.max(1)

        # Obtener top 3 predicciones
        top3_prob, top3_idx = probabilities.topk(3, dim=1)

        predicted_class = class_names[predicted_idx.item()]
        confidence_score = confidence.item() * 100

        # Top 3 predicciones
        top_predictions = []
        for i in range(3):
            if i < len(top3_idx[0]):
                class_idx = top3_idx[0][i].item()
                prob = top3_prob[0][i].item() * 100
                top_predictions.append({
                    'class': class_names[class_idx],
                    'probability': prob
                })

        # Obtener información de la planta
        plant_info = plants_info.get('plantas_medicinales', {}).get(predicted_class, {})

        return {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': confidence_score,
            'top_predictions': top_predictions,
            'plant_info': plant_info
        }

    except Exception as e:
        return {
            'error': f'Error al procesar imagen: {str(e)}',
            'success': False
        }


@app.route('/')
def index():
    """Página principal."""
    return render_template('index.html',
                         num_classes=len(class_names),
                         model_loaded=model is not None)


@app.route('/predict', methods=['POST'])
def predict():
    """Endpoint para realizar predicciones."""
    if 'file' not in request.files:
        return jsonify({'error': 'No se envió ningún archivo', 'success': False})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo', 'success': False})

    if file and allowed_file(file.filename):
        # Guardar archivo
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Crear directorio si no existe
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        file.save(filepath)

        # Realizar predicción
        result = predict_image(filepath)

        # Agregar URL de la imagen
        if result.get('success'):
            result['image_url'] = url_for('static', filename=f'uploads/{filename}')

        return jsonify(result)

    return jsonify({'error': 'Tipo de archivo no permitido', 'success': False})


@app.route('/classes')
def get_classes():
    """Retorna la lista de clases disponibles."""
    return jsonify({
        'classes': class_names,
        'num_classes': len(class_names)
    })


@app.route('/plant-info/<class_name>')
def get_plant_info(class_name):
    """Retorna información sobre una planta específica."""
    plant_info = plants_info.get('plantas_medicinales', {}).get(class_name, {})

    if plant_info:
        return jsonify({
            'success': True,
            'class_name': class_name,
            'info': plant_info
        })
    else:
        return jsonify({
            'success': False,
            'error': f'No se encontró información para {class_name}'
        })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'num_classes': len(class_names),
        'device': device
    })


if __name__ == '__main__':
    # Cargar modelo e información
    load_model_and_info()

    # Ejecutar aplicación
    print("\n🌿 Asistente de Plantas Medicinales iniciado")
    print("   Visita: http://localhost:5000")
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
