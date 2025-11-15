# 🌿 Guía Paso a Paso: Clasificador de Plantas Medicinales

## 📋 Contenido
1. [Instalación Inicial](#paso-1-instalación-inicial)
2. [Preparar Datos](#paso-2-preparar-datos)
3. [Entrenar el Modelo](#paso-3-entrenar-el-modelo)
4. [Usar la Aplicación Web](#paso-4-usar-la-aplicación-web)
5. [Solución de Problemas](#solución-de-problemas)

---

## Paso 1: Instalación Inicial

### 1.1 Requisitos Previos
Asegúrate de tener instalado:
- Python 3.8 o superior
- pip (gestor de paquetes)
- Git

Para verificar:
```bash
python --version
pip --version
```

### 1.2 Crear Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

Verás `(venv)` al inicio de tu línea de comando cuando esté activado.

### 1.3 Instalar Dependencias
```bash
pip install -r requirements.txt
```

Esto instalará:
- PyTorch (Deep Learning)
- Flask (servidor web)
- OpenCV (procesamiento de imágenes)
- Y otras librerías necesarias

⏱️ **Tiempo estimado**: 5-10 minutos (depende de tu conexión)

---

## Paso 2: Preparar Datos

### 2.1 Obtener el Dataset

**Opción A: Desde Kaggle (Recomendado)**
```bash
# Instalar Kaggle CLI (si no lo tienes)
pip install kaggle

# Descargar dataset
kaggle datasets download -d aryashah2k/indian-medicinal-leaves-dataset

# Descomprimir
unzip indian-medicinal-leaves-dataset.zip -d data/raw/
```

**Opción B: Usar tus propias imágenes**

Organiza tus imágenes así:
```
data/raw/
├── aloe_vera/
│   ├── imagen1.jpg
│   ├── imagen2.jpg
│   └── ...
├── manzanilla/
│   ├── imagen1.jpg
│   └── ...
└── otra_planta/
    └── ...
```

### 2.2 Explorar y Validar Datos

Abre el primer notebook:
```bash
jupyter notebook notebooks/01_exploracion_datos.ipynb
```

**En el notebook:**
1. **Ejecuta todas las celdas** (Cell → Run All)
2. Verás:
   - Cantidad de imágenes por clase
   - Distribución de datos
   - Ejemplos visuales de plantas
3. El notebook dividirá automáticamente en:
   - 70% entrenamiento
   - 15% validación
   - 15% prueba

⏱️ **Tiempo estimado**: 10-15 minutos

---

## Paso 3: Entrenar el Modelo

### 3.1 Ejecutar Entrenamiento

Abre el segundo notebook:
```bash
jupyter notebook notebooks/02_entrenamiento_modelo.ipynb
```

**En el notebook:**
1. **Ejecuta todas las celdas** (Cell → Run All)
2. El entrenamiento:
   - Carga MobileNetV2 pre-entrenado
   - Aplica Transfer Learning
   - Usa Data Augmentation
   - Guarda el mejor modelo

### 3.2 Durante el Entrenamiento

Verás algo como:
```
Epoch 1/50
Train Loss: 2.453 | Train Acc: 45.2%
Val Loss: 1.892 | Val Acc: 58.7%

Epoch 2/50
Train Loss: 1.234 | Train Acc: 67.8%
Val Loss: 1.123 | Val Acc: 72.3%
...
```

### 3.3 Resultado

Al finalizar:
- ✅ Modelo guardado en `models/best_model.pth`
- ✅ Gráficas de pérdida y precisión
- ✅ Listo para usar en la app web

⏱️ **Tiempo estimado**: 30-60 minutos (depende de tu hardware)

💡 **Tip**: Si tienes GPU, el entrenamiento será mucho más rápido

---

## Paso 4: Usar la Aplicación Web

### 4.1 Iniciar el Servidor

```bash
python app/app.py
```

Verás:
```
 * Running on http://127.0.0.1:5000
 * Modelo cargado correctamente: 30 clases
```

### 4.2 Abrir la Interfaz

1. Abre tu navegador web
2. Ve a: `http://localhost:5000`
3. Verás la interfaz del clasificador

### 4.3 Clasificar una Planta

**Paso a paso en la interfaz:**

1. **Subir imagen**:
   - Arrastra una imagen a la zona de "Drag & Drop"
   - O haz clic en "Seleccionar Imagen"
   - Formatos: JPG o PNG
   - Tamaño máximo: 16MB

2. **Preview**:
   - Verás la imagen que seleccionaste
   - Si quieres cambiarla: clic en "Cambiar Imagen"

3. **Analizar**:
   - Haz clic en "Analizar Planta 🔍"
   - Aparecerá un spinner mientras analiza

4. **Ver Resultados**:
   ```
   🌿 ALOE VERA (92.5% confianza)

   Top 3 Predicciones:
   1. Aloe Vera    ████████████░  92.5%
   2. Sábila       ████░░░░░░░░░  35.2%
   3. Cactus       ██░░░░░░░░░░░  18.7%

   Información:
   - Familia: Asphodelaceae
   - Usos tradicionales
   - Propiedades medicinales
   - Modo de uso
   - Precauciones
   ```

5. **Analizar otra**:
   - Haz clic en "Analizar Otra Planta"
   - Repite el proceso

### 4.4 Detener el Servidor

En la terminal donde ejecutaste la app:
- Presiona `Ctrl + C`

---

## Paso 5: Evaluar el Modelo (Opcional)

Para ver métricas detalladas:

```bash
jupyter notebook notebooks/03_evaluacion_modelo.ipynb
```

Verás:
- Matriz de confusión
- Precisión, Recall, F1-Score por clase
- Ejemplos de predicciones correctas/incorrectas
- Análisis de errores

⏱️ **Tiempo estimado**: 10 minutos

---

## 🎯 Resumen del Flujo Completo

```
1. Instalar dependencias
   ↓
2. Obtener/organizar dataset
   ↓
3. Explorar datos (notebook 01)
   ↓
4. Entrenar modelo (notebook 02)
   ↓
5. Ejecutar app web
   ↓
6. Clasificar plantas
```

---

## Solución de Problemas

### ❌ Error: "Modelo no disponible"

**Solución**: Necesitas entrenar el modelo primero
```bash
jupyter notebook notebooks/02_entrenamiento_modelo.ipynb
```

### ❌ Error: "No module named 'torch'"

**Solución**: Instalar dependencias
```bash
pip install -r requirements.txt
```

### ❌ Error: "CUDA out of memory"

**Solución**: El modelo intentará usar GPU automáticamente. Si tienes problemas:
- Reduce el batch_size en el notebook
- O fuerza CPU (más lento pero funciona):
  ```python
  device = torch.device('cpu')
  ```

### ❌ La interfaz no carga

**Verificar**:
1. ¿El servidor está corriendo?
   ```bash
   python app/app.py
   ```
2. ¿Estás usando la URL correcta?
   - Debe ser: `http://localhost:5000`

### ❌ Error: "File not allowed"

**Solución**: Solo se permiten imágenes JPG y PNG
- Convierte tu imagen a JPG/PNG
- O usa otra imagen

---

## 📊 Métricas Esperadas

Con el dataset de plantas medicinales indias:
- **Precisión**: ~92-95%
- **Top-3 Accuracy**: ~98%
- **Tiempo de inferencia**: < 1 segundo

---

## 💡 Consejos para Mejores Resultados

### Para mejores predicciones:
1. ✅ Usa imágenes claras y bien iluminadas
2. ✅ Enfoca la hoja completa de la planta
3. ✅ Evita fondos muy complejos
4. ✅ Usa imágenes similares a las del entrenamiento

### Para mejorar el modelo:
1. 📈 Agrega más imágenes por clase
2. 📸 Usa data augmentation más agresivo
3. ⚙️ Ajusta hiperparámetros (learning rate, epochs)
4. 🔄 Prueba otros modelos (ResNet, EfficientNet)

---

## 🚀 Comandos Rápidos

```bash
# Activar entorno
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Notebooks
jupyter notebook

# Ejecutar app web
python app/app.py

# Verificar proyecto
python verificar_proyecto.py
```

---

## 📚 Documentación Adicional

- **Reporte técnico**: `docs/REPORTE_PROYECTO.md`
- **Plan de trabajo**: `docs/PLAN_TRABAJO.md`
- **Interfaz web**: `INTERFAZ_WEB_COMPLETA.md`
- **Verificación**: `VERIFICACION_COMPLETA.md`

---

## ✅ Checklist de Inicio Rápido

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Dataset descargado en `data/raw/`
- [ ] Notebook 01 ejecutado (exploración)
- [ ] Notebook 02 ejecutado (entrenamiento)
- [ ] Modelo guardado en `models/best_model.pth`
- [ ] App web ejecutándose (`python app/app.py`)
- [ ] Interfaz accesible en `http://localhost:5000`

---

## 🎓 ¿Primera Vez con Machine Learning?

**No te preocupes**, esta guía está diseñada para principiantes:

1. **Sigue los pasos en orden**
2. **Lee los mensajes de error** (te dirán qué falta)
3. **Experimenta** con diferentes imágenes
4. **Explora** los notebooks para entender cómo funciona

---

## 📞 ¿Necesitas Ayuda?

Si algo no funciona:
1. Revisa la sección "Solución de Problemas"
2. Verifica que completaste todos los pasos previos
3. Lee los mensajes de error completos
4. Abre un issue en GitHub

---

**¡Listo! Ahora puedes clasificar plantas medicinales con IA 🌿🤖**

Desarrollado con ❤️ para el curso de Inteligencia Artificial
