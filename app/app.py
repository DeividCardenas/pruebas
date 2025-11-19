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
plant_mapping = {}
display_names = {}
device = 'cpu'


def allowed_file(filename):
    """Verifica si el archivo tiene una extensión permitida."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def load_model_and_info():
    """Carga el modelo entrenado y la información de plantas."""
    global model, class_names, plants_info, plant_mapping, display_names, device

    print("\n" + "="*70)
    print("Iniciando Asistente de Plantas Medicinales")
    print("="*70)

    # Configurar dispositivo
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Dispositivo: {device}")

    # Cargar mapeo de nombres de plantas
    mapping_path = ROOT_DIR / 'data' / 'plant_names_mapping.json'
    if mapping_path.exists():
        with open(mapping_path, 'r', encoding='utf-8') as f:
            mapping_data = json.load(f)
            plant_mapping = mapping_data.get('mapping', {})
            display_names = mapping_data.get('display_names', {})
        print(f"✓ Mapeo de nombres cargado: {len(plant_mapping)} plantas")
    else:
        print(f"⚠ Advertencia: No se encontró {mapping_path}")

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
                class_name = class_names[class_idx]

                # Usar nombre para mostrar (en español bonito)
                display_name = display_names.get(class_name, class_name)

                top_predictions.append({
                    'class': class_name,
                    'display_name': display_name,
                    'probability': prob
                })

        # Mapear nombre en inglés a español para buscar información
        spanish_key = plant_mapping.get(predicted_class, predicted_class.lower())

        # Obtener información de la planta usando la clave en español
        plant_info = plants_info.get('plantas_medicinales', {}).get(spanish_key, {})

        # Nombre para mostrar al usuario
        display_name = display_names.get(predicted_class, predicted_class)

        return {
            'success': True,
            'predicted_class': predicted_class,
            'display_name': display_name,
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
def home():
    """Página de inicio (landing)."""
    return render_template('home.html',
                         num_classes=len(class_names),
                         model_loaded=model is not None)


@app.route('/classifier')
def classifier():
    """Página del clasificador."""
    return render_template('classifier.html',
                         num_classes=len(class_names),
                         model_loaded=model is not None)


@app.route('/gallery')
def gallery():
    """Página de galería de plantas."""
    plantas = plants_info.get('plantas_medicinales', {})

    # Contar familias únicas
    familias = set()
    for plant_info in plantas.values():
        if 'familia' in plant_info:
            familias.add(plant_info['familia'])

    return render_template('gallery.html',
                         plants=plantas,
                         plants_json=json.dumps(plantas),
                         num_plants=len(plantas),
                         num_families=len(familias),
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


@app.route('/chatbot', methods=['POST'])
def chatbot():
    """
    Endpoint del chatbot - Procesa consultas sobre plantas medicinales.

    Sistema inteligente que:
    - Responde preguntas sobre plantas específicas
    - Recomienda plantas según síntomas/necesidades
    - Busca por propiedades medicinales
    - Proporciona información detallada
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip().lower()

        if not user_message:
            return jsonify({
                'success': False,
                'error': 'Mensaje vacío'
            })

        # Procesar la consulta y generar respuesta
        response_data = process_chatbot_query(user_message)

        return jsonify(response_data)

    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Error al procesar consulta: {str(e)}'
        })


def process_chatbot_query(query):
    """
    Procesa la consulta del usuario y genera una respuesta inteligente.

    Args:
        query: Consulta del usuario (en minúsculas)

    Returns:
        Diccionario con respuesta y sugerencias
    """
    plantas = plants_info.get('plantas_medicinales', {})

    # Palabras clave para diferentes tipos de consultas
    saludos = ['hola', 'buenos', 'buenas', 'hey', 'hi', 'hello']
    despedidas = ['adios', 'chao', 'hasta luego', 'bye']
    ayuda = ['ayuda', 'help', 'qué puedes hacer', 'que puedes']

    # 1. SALUDOS
    if any(word in query for word in saludos):
        return {
            'success': True,
            'response': '¡Hola! Soy tu Asistente Herbal. Puedo ayudarte con información sobre plantas medicinales, sus usos y propiedades. ¿Qué te gustaría saber?',
            'suggestions': [
                '¿Qué plantas conoces?',
                'Plantas antiinflamatorias',
                'Info sobre menta',
                '¿Cómo funciona?'
            ]
        }

    # 2. DESPEDIDAS
    if any(word in query for word in despedidas):
        return {
            'success': True,
            'response': '¡Hasta pronto! Recuerda siempre consultar con un profesional de salud antes de usar plantas medicinales. 🌿',
            'suggestions': []
        }

    # 3. AYUDA
    if any(word in query for word in ayuda):
        return {
            'success': True,
            'response': '''Puedo ayudarte con:

**Información de plantas**: "info sobre menta", "cuéntame sobre neem"
**Búsqueda por síntomas**: "plantas para dolor de cabeza", "qué planta ayuda con la digestión"
**Búsqueda por propiedades**: "plantas antiinflamatorias", "plantas antioxidantes"
**Listar plantas**: "qué plantas conoces", "lista de plantas"

¿Qué te gustaría saber?''',
            'suggestions': [
                '¿Qué plantas conoces?',
                'Plantas para dolor de cabeza',
                'Info sobre curcuma'
            ]
        }

    # 4. LISTAR PLANTAS
    if any(word in query for word in ['qué plantas', 'que plantas', 'lista', 'cuantas plantas', 'plantas disponibles']):
        plantas_nombres = []
        for key, info in list(plantas.items())[:10]:  # Primeras 10
            plantas_nombres.append(info.get('nombre_comun', key))

        response = f'''Conozco información de **{len(plantas)} plantas medicinales**. Aquí algunas:

{', '.join(plantas_nombres)}... y {len(plantas) - 10} más.

Pregúntame sobre cualquiera de ellas o busca por síntomas/propiedades.'''

        return {
            'success': True,
            'response': response,
            'suggestions': [
                'Info sobre menta',
                'Plantas antiinflamatorias',
                'Plantas para digestión'
            ]
        }

    # 5. BÚSQUEDA POR NOMBRE DE PLANTA
    plant_found = None
    plant_key = None
    for key, info in plantas.items():
        nombre_comun = info.get('nombre_comun', '').lower()
        nombre_cientifico = info.get('nombre_cientifico', '').lower()

        # Buscar coincidencias
        if key in query or nombre_comun.split(',')[0].lower() in query or nombre_cientifico.lower() in query:
            plant_found = info
            plant_key = key
            break

    if plant_found:
        usos = '\n'.join([f"• {uso}" for uso in plant_found.get('usos_tradicionales', [])[:4]])
        propiedades = ', '.join(plant_found.get('propiedades', [])[:3])

        response = f'''**{plant_found.get('nombre_comun', 'Planta')}** ({plant_found.get('nombre_cientifico', '')})

**Familia:** {plant_found.get('familia', 'N/A')}

**Usos tradicionales:**
{usos}

**Propiedades:** {propiedades}

**Modo de uso:** {plant_found.get('modo_uso', 'N/A')}

⚠️ **Precauciones:** {plant_found.get('precauciones', 'Consultar profesional de salud.')}'''

        return {
            'success': True,
            'response': response,
            'plant_info': plant_found,
            'suggestions': [
                '¿Otras plantas similares?',
                'Plantas para digestión',
                '¿Qué plantas conoces?'
            ]
        }

    # 6. BÚSQUEDA POR SÍNTOMAS/USOS
    sintomas_keywords = {
        'dolor de cabeza': ['dolor de cabeza', 'cefalea', 'migraña', 'headache'],
        'digestión': ['digestión', 'estómago', 'gastric', 'digestivo', 'nauseas', 'indigestión'],
        'fiebre': ['fiebre', 'temperatura', 'fever', 'antipirético'],
        'diabetes': ['diabetes', 'azúcar', 'glucosa'],
        'inflamación': ['inflamación', 'hinchazón', 'inflam'],
        'dolor': ['dolor', 'analgésico', 'pain'],
        'resfriado': ['resfriado', 'tos', 'gripe', 'cold', 'congestión'],
        'piel': ['piel', 'dermatitis', 'skin', 'heridas'],
        'ansiedad': ['ansiedad', 'estrés', 'nervios', 'anxiety', 'stress'],
        'artritis': ['artritis', 'articulaciones', 'arthritis'],
        'corazón': ['corazón', 'cardiovascular', 'circulación', 'heart'],
        'hígado': ['hígado', 'liver', 'hepat'],
        'inmune': ['inmune', 'defensas', 'immune', 'inmunológico']
    }

    matching_plants = []
    for sintoma, keywords in sintomas_keywords.items():
        if any(kw in query for kw in keywords):
            # Buscar plantas que traten este síntoma
            for key, info in plantas.items():
                usos_text = ' '.join(info.get('usos_tradicionales', [])).lower()
                propiedades_text = ' '.join(info.get('propiedades', [])).lower()

                if any(kw in usos_text or kw in propiedades_text for kw in keywords):
                    matching_plants.append({
                        'nombre': info.get('nombre_comun', key),
                        'cientifico': info.get('nombre_cientifico', ''),
                        'info': info
                    })

    if matching_plants:
        # Limitar a 5 plantas
        matching_plants = matching_plants[:5]

        response = f'Encontré **{len(matching_plants)} planta(s)** que podrían ayudarte:\n\n'

        for i, plant in enumerate(matching_plants, 1):
            propiedades = ', '.join(plant['info'].get('propiedades', [])[:2])
            response += f"**{i}. {plant['nombre']}**\n"
            response += f"   • Propiedades: {propiedades}\n"
            response += f"   • Uso: {plant['info'].get('modo_uso', 'N/A')}\n\n"

        response += '\n⚠️ Recuerda consultar con un profesional de salud antes de usar plantas medicinales.'

        return {
            'success': True,
            'response': response,
            'suggestions': [
                f"Info sobre {matching_plants[0]['nombre'].split(',')[0]}",
                '¿Qué plantas conoces?',
                'Ayuda'
            ]
        }

    # 7. BÚSQUEDA POR PROPIEDADES
    propiedades_keywords = {
        'antiinflamatorio': ['antiinflamatorio', 'inflamación'],
        'antioxidante': ['antioxidante', 'oxidante'],
        'digestivo': ['digestivo', 'digestión'],
        'analgésico': ['analgésico', 'dolor'],
        'antimicrobiano': ['antimicrobiano', 'antibacteriano', 'antifúngico'],
        'diurético': ['diurético'],
        'sedante': ['sedante', 'calmante', 'relajante']
    }

    matching_by_property = []
    for propiedad, keywords in propiedades_keywords.items():
        if any(kw in query for kw in keywords):
            for key, info in plantas.items():
                propiedades = [p.lower() for p in info.get('propiedades', [])]
                if any(kw in ' '.join(propiedades) for kw in keywords):
                    matching_by_property.append({
                        'nombre': info.get('nombre_comun', key),
                        'propiedades': info.get('propiedades', [])
                    })

    if matching_by_property:
        matching_by_property = matching_by_property[:6]

        plantas_lista = ', '.join([p['nombre'].split(',')[0] for p in matching_by_property])

        response = f'''Encontré **{len(matching_by_property)} plantas** con estas propiedades:

{plantas_lista}

Pregúntame sobre alguna en específico para más detalles.'''

        return {
            'success': True,
            'response': response,
            'suggestions': [
                f"Info sobre {matching_by_property[0]['nombre'].split(',')[0]}",
                '¿Qué otras propiedades hay?',
                'Plantas para digestión'
            ]
        }

    # 8. PREGUNTA SOBRE CÓMO FUNCIONA EL SISTEMA
    if any(word in query for word in ['cómo funciona', 'como funciona', 'cómo usar', 'how']):
        return {
            'success': True,
            'response': '''Este es un sistema de clasificación de plantas medicinales con IA.

**Funcionalidades:**
• **Clasificador**: Sube una foto de una planta y te diré qué es
• **Galería**: Explora todas las plantas disponibles
• **Chatbot**: Pregúntame sobre plantas, síntomas o propiedades

**Puedes preguntarme:**
"¿Qué planta es buena para el dolor de cabeza?"
"Cuéntame sobre la menta"
"Plantas antiinflamatorias"

¿Qué te gustaría saber?''',
            'suggestions': [
                '¿Qué plantas conoces?',
                'Plantas para digestión',
                'Info sobre curcuma'
            ]
        }

    # 9. RESPUESTA POR DEFECTO
    return {
        'success': True,
        'response': 'No estoy seguro de cómo ayudarte con eso. Puedo darte información sobre plantas medicinales específicas, recomendar plantas según síntomas, o buscar por propiedades. ¿Qué te gustaría saber?',
        'suggestions': [
            '¿Qué puedes hacer?',
            '¿Qué plantas conoces?',
            'Plantas para dolor de cabeza'
        ]
    }


if __name__ == '__main__':
    # Cargar modelo e información
    load_model_and_info()

    # Ejecutar aplicación
    print("\n🌿 Asistente de Plantas Medicinales iniciado")
    print("   Visita: http://localhost:5000")
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
