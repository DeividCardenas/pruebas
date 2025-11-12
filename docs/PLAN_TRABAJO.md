# 📅 Plan de Trabajo - 2 Semanas

## Proyecto: Clasificación de Plantas Medicinales
**Equipo**: 3 integrantes
**Duración**: 14 días
**Objetivo**: Desarrollar un clasificador de plantas medicinales con asistente web

---

## 📊 Distribución de Tareas por Miembro

### 👤 Miembro 1: Especialista en Datos
**Responsabilidades principales**:
- Descarga y organización del dataset
- Preprocesamiento de imágenes
- Data augmentation
- División train/val/test

### 👤 Miembro 2: Especialista en Modelado
**Responsabilidades principales**:
- Implementación del modelo
- Entrenamiento con Transfer Learning
- Experimentación con hiperparámetros
- Evaluación y métricas

### 👤 Miembro 3: Especialista en Desarrollo
**Responsabilidades principales**:
- Desarrollo de la aplicación Flask
- Integración del modelo
- Base de conocimientos de plantas
- Documentación

---

## 📆 Planificación por Días

### **Semana 1: Investigación, Datos y Modelo Base**

#### Día 1-2: Investigación y Setup (Todos)
**Objetivos**:
- Configurar entorno de desarrollo
- Investigar datasets disponibles
- Definir arquitectura del proyecto
- Configurar repositorio Git

**Tareas**:
- [ ] **Todos**: Reunión de inicio, definir roles
- [ ] **Todos**: Crear repositorio Git y estructura de carpetas
- [ ] **Todos**: Instalar dependencias (Python, PyTorch, etc.)
- [ ] **Miembro 1**: Investigar datasets de plantas medicinales
- [ ] **Miembro 2**: Estudiar MobileNetV2 y Transfer Learning
- [ ] **Miembro 3**: Investigar Flask y diseño de UI

**Entregable**: Entorno configurado, dataset identificado

---

#### Día 3-4: Preparación de Datos (Miembro 1 lidera)
**Objetivos**:
- Descargar dataset
- Exploración de datos
- Preprocesamiento

**Tareas**:
- [ ] **Miembro 1**: Descargar dataset de Kaggle
- [ ] **Miembro 1**: Notebook de exploración (01_exploracion_datos.ipynb)
- [ ] **Miembro 1**: Implementar data augmentation
- [ ] **Miembro 1**: Crear splits train/val/test
- [ ] **Miembro 2**: Ayudar con validación de imágenes
- [ ] **Miembro 3**: Documentar proceso de descarga en README

**Entregable**: Dataset organizado en train/val/test, notebook de exploración

---

#### Día 5-6: Modelo Base (Miembro 2 lidera)
**Objetivos**:
- Implementar arquitectura del modelo
- Primer entrenamiento

**Tareas**:
- [ ] **Miembro 2**: Implementar MedicinalPlantClassifier
- [ ] **Miembro 2**: Configurar DataLoaders
- [ ] **Miembro 2**: Implementar loop de entrenamiento
- [ ] **Miembro 2**: Entrenar modelo base (10 épocas de prueba)
- [ ] **Miembro 1**: Preparar más datos si es necesario
- [ ] **Miembro 3**: Empezar diseño de interfaz web

**Entregable**: Modelo entrenado (versión base), métricas iniciales

---

#### Día 7: Revisión Semana 1 (Todos)
**Objetivos**:
- Revisar progreso
- Ajustar plan si es necesario
- Demo interna

**Tareas**:
- [ ] **Todos**: Reunión de revisión
- [ ] **Todos**: Demo del modelo base
- [ ] **Todos**: Identificar problemas y ajustes
- [ ] **Todos**: Actualizar documentación

**Entregable**: Presentación de avances, plan ajustado

---

### **Semana 2: Optimización, Aplicación y Documentación**

#### Día 8-9: Optimización del Modelo (Miembro 2 lidera)
**Objetivos**:
- Optimizar hiperparámetros
- Entrenamiento completo
- Evaluación exhaustiva

**Tareas**:
- [ ] **Miembro 2**: Experimentar con hiperparámetros
- [ ] **Miembro 2**: Entrenamiento completo (50 épocas)
- [ ] **Miembro 2**: Notebook de evaluación (03_evaluacion_modelo.ipynb)
- [ ] **Miembro 2**: Generar matriz de confusión
- [ ] **Miembro 1**: Análisis de errores, mejorar data augmentation
- [ ] **Miembro 3**: Preparar estructura de Flask

**Entregable**: Modelo final entrenado, métricas completas

---

#### Día 10-11: Aplicación Web (Miembro 3 lidera)
**Objetivos**:
- Desarrollar interfaz web
- Integrar modelo
- Base de conocimientos

**Tareas**:
- [ ] **Miembro 3**: Implementar backend Flask (app.py)
- [ ] **Miembro 3**: Diseñar HTML/CSS (index.html, style.css)
- [ ] **Miembro 3**: Implementar JavaScript (main.js)
- [ ] **Miembro 3**: Integrar modelo entrenado
- [ ] **Miembro 3**: Crear base de conocimientos (plantas_info.json)
- [ ] **Miembro 2**: Ayudar con integración del modelo
- [ ] **Miembro 1**: Probar aplicación, reportar bugs

**Entregable**: Aplicación web funcional

---

#### Día 12: Documentación (Todos)
**Objetivos**:
- Completar documentación
- Preparar reporte
- Preparar presentación

**Tareas**:
- [ ] **Miembro 1**: Sección de datos en reporte
- [ ] **Miembro 2**: Sección de modelo y resultados en reporte
- [ ] **Miembro 3**: README.md completo
- [ ] **Todos**: Revisar y editar reporte
- [ ] **Todos**: Crear presentación (slides)
- [ ] **Todos**: Grabar video demo (opcional)

**Entregable**: Reporte completo, presentación preparada

---

#### Día 13: Testing y Pulido (Todos)
**Objetivos**:
- Pruebas exhaustivas
- Corregir bugs
- Mejorar UX

**Tareas**:
- [ ] **Todos**: Testing de la aplicación
- [ ] **Todos**: Corregir bugs encontrados
- [ ] **Miembro 3**: Mejorar diseño de interfaz
- [ ] **Miembro 2**: Verificar que todas las métricas sean correctas
- [ ] **Miembro 1**: Verificar calidad de datos
- [ ] **Todos**: Ensayar presentación

**Entregable**: Sistema completo y testeado

---

#### Día 14: Entrega Final (Todos)
**Objetivos**:
- Preparar entrega
- Última revisión
- Backup

**Tareas**:
- [ ] **Todos**: Revisión final de código
- [ ] **Todos**: Verificar todos los entregables
- [ ] **Todos**: Crear backup del proyecto
- [ ] **Todos**: Subir a repositorio
- [ ] **Todos**: Preparar demo en vivo
- [ ] **Todos**: Ensayo final de presentación

**Entregable**: Proyecto completo listo para presentación

---

## 📋 Checklist de Entregables

### Código Fuente ✅
- [ ] Código documentado y comentado
- [ ] Estructura modular
- [ ] Requirements.txt
- [ ] .gitignore configurado
- [ ] README.md completo

### Notebooks ✅
- [ ] 01_exploracion_datos.ipynb
- [ ] 02_entrenamiento_modelo.ipynb
- [ ] 03_evaluacion_modelo.ipynb

### Modelo ✅
- [ ] Modelo entrenado (best_model.pth)
- [ ] Checkpoints guardados
- [ ] Logs de entrenamiento

### Aplicación ✅
- [ ] Backend Flask funcional
- [ ] Frontend atractivo
- [ ] Base de conocimientos
- [ ] Manejo de errores

### Documentación ✅
- [ ] Reporte del proyecto (10-15 páginas)
- [ ] README.md
- [ ] Comentarios en código
- [ ] Diagramas (arquitectura, flujo)

### Presentación ✅
- [ ] Slides (10-15 minutos)
- [ ] Demo en vivo
- [ ] Video (opcional)
- [ ] Q&A preparada

---

## 🎯 Hitos Clave

| Día | Hito | Responsable |
|-----|------|-------------|
| 2 | Dataset descargado | Miembro 1 |
| 4 | Datos preprocesados | Miembro 1 |
| 6 | Modelo base entrenado | Miembro 2 |
| 9 | Modelo final optimizado | Miembro 2 |
| 11 | Aplicación web completa | Miembro 3 |
| 12 | Documentación finalizada | Todos |
| 14 | Proyecto listo para entrega | Todos |

---

## 🚨 Gestión de Riesgos

### Riesgo 1: Dataset insuficiente
**Probabilidad**: Media
**Impacto**: Alto
**Mitigación**:
- Tener datasets alternativos identificados
- Usar data augmentation agresivo
- Reducir número de clases si es necesario

### Riesgo 2: Modelo no converge
**Probabilidad**: Baja
**Impacto**: Alto
**Mitigación**:
- Usar Transfer Learning (más robusto)
- Tener arquitecturas alternativas listas (ResNet50)
- Consultar con profesor/TAs

### Riesgo 3: Problemas técnicos (hardware, software)
**Probabilidad**: Media
**Impacto**: Medio
**Mitigación**:
- Usar Google Colab como backup
- Tener backups frecuentes
- Iniciar entrenamiento con anticipación

### Riesgo 4: Integración modelo-aplicación
**Probabilidad**: Baja
**Impacto**: Medio
**Mitigación**:
- Probar integración temprano (Día 10)
- Documentar formato de entrada/salida
- Tener plan B (CLI en lugar de web)

### Riesgo 5: Falta de tiempo
**Probabilidad**: Media
**Impacto**: Alto
**Mitigación**:
- Buffer de 1 día al final
- Identificar entregables críticos vs opcionales
- Reuniones diarias de 15 min (stand-up)

---

## 🤝 Comunicación del Equipo

### Reuniones
- **Daily Standup**: 15 min diarios (virtual)
  - ¿Qué hiciste ayer?
  - ¿Qué harás hoy?
  - ¿Hay bloqueadores?

- **Revisión Semanal**: 1 hora al final de cada semana
  - Demo de avances
  - Retrospectiva
  - Planificación ajustada

### Herramientas
- **Git**: Control de versiones
- **Slack/WhatsApp**: Comunicación rápida
- **Google Drive**: Documentos compartidos
- **Trello/Notion**: Gestión de tareas

### Buenas Prácticas
- Commits frecuentes con mensajes descriptivos
- Pull requests para cambios importantes
- Documentar decisiones importantes
- Pedir ayuda temprano si hay problemas

---

## 💡 Consejos para el Éxito

1. **Empezar simple**: Primero un modelo básico que funcione, luego optimizar
2. **Iterar rápido**: Ciclos cortos de desarrollo-prueba-mejora
3. **Comunicación constante**: No trabajar en silos
4. **Documentar todo**: Facilita el reporte final
5. **Probar frecuentemente**: Catch bugs early
6. **Gestión del tiempo**: No dejar todo para el final
7. **Celebrar logros**: Mantener la motivación alta

---

## 📈 Criterios de Éxito

### Mínimo Viable (Aprobar)
- [x] Modelo entrenado con >80% accuracy
- [x] Aplicación funcional básica
- [x] Reporte completo
- [x] Presentación de 10-15 min

### Objetivo Esperado (Buena Nota)
- [x] Modelo >90% accuracy
- [x] Aplicación web profesional
- [x] Documentación excelente
- [x] Demo impresionante

### Stretch Goals (Excelencia)
- [ ] >95% accuracy
- [ ] App mobile
- [ ] Dataset propio recopilado
- [ ] Paper/publicación

---

**¡Buena suerte equipo! 🚀🌿**
