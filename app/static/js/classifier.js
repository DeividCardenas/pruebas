/**
 * Classifier - Sistema de clasificación de plantas medicinales
 */

// Variables globales
let selectedFile = null;
let predictionsChart = null;

// Elementos del DOM
const uploadBox = document.getElementById('uploadBox');
const fileInput = document.getElementById('fileInput');
const selectBtn = document.getElementById('selectBtn');
const previewSection = document.getElementById('previewSection');
const previewImage = document.getElementById('previewImage');
const changeImageBtn = document.getElementById('changeImageBtn');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');
const tryAgainBtn = document.getElementById('tryAgainBtn');
const retryBtn = document.getElementById('retryBtn');

// Event Listeners
selectBtn.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', handleFileSelect);
changeImageBtn.addEventListener('click', resetUpload);
analyzeBtn.addEventListener('click', analyzeImage);
tryAgainBtn.addEventListener('click', resetUpload);
retryBtn.addEventListener('click', resetUpload);

// Drag and drop
uploadBox.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadBox.classList.add('dragover');
});

uploadBox.addEventListener('dragleave', () => {
    uploadBox.classList.remove('dragover');
});

uploadBox.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadBox.classList.remove('dragover');

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

// Click en el uploadBox (excepto en el botón)
uploadBox.addEventListener('click', (e) => {
    if (!selectBtn.contains(e.target)) {
        fileInput.click();
    }
});

/**
 * Maneja la selección de archivo desde el input
 */
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

/**
 * Procesa y valida el archivo seleccionado
 */
function handleFile(file) {
    // Validar tipo de archivo
    const validTypes = ['image/jpeg', 'image/jpg', 'image/png'];
    if (!validTypes.includes(file.type)) {
        showError('Por favor, selecciona una imagen válida (JPG o PNG)');
        return;
    }

    // Validar tamaño (16MB)
    if (file.size > 16 * 1024 * 1024) {
        showError('La imagen es demasiado grande. Máximo 16MB.');
        return;
    }

    selectedFile = file;

    // Mostrar preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadBox.style.display = 'none';
        previewSection.style.display = 'block';
    };
    reader.readAsDataURL(file);
}

/**
 * Reinicia el estado de la interfaz
 */
function resetUpload() {
    selectedFile = null;
    fileInput.value = '';
    uploadBox.style.display = 'block';
    previewSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';
    loading.style.display = 'none';

    // Destruir gráfico si existe
    if (predictionsChart) {
        predictionsChart.destroy();
        predictionsChart = null;
    }
}

/**
 * Analiza la imagen seleccionada
 */
async function analyzeImage() {
    if (!selectedFile) {
        showError('Por favor, selecciona una imagen primero');
        return;
    }

    // Mostrar loading
    previewSection.style.display = 'none';
    loading.style.display = 'block';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    // Crear FormData
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        // Enviar solicitud
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Ocultar loading
        loading.style.display = 'none';

        if (data.success) {
            displayResults(data);
        } else {
            showError(data.error || 'Error al analizar la imagen');
        }
    } catch (error) {
        loading.style.display = 'none';
        showError('Error de conexión. Por favor, intenta de nuevo.');
        console.error('Error:', error);
    }
}

/**
 * Muestra los resultados del análisis
 */
function displayResults(data) {
    // Mostrar sección de resultados
    resultsSection.style.display = 'block';

    // Nombre de la planta
    const plantName = data.display_name || formatPlantName(data.predicted_class);
    document.getElementById('plantName').textContent = plantName;

    // Confianza
    const confidence = data.confidence.toFixed(1);
    const confidenceBadge = document.getElementById('confidenceBadge');
    confidenceBadge.querySelector('span').textContent = `${confidence}%`;

    // Actualizar medidor de confianza
    const confidenceFill = document.getElementById('confidenceFill');
    setTimeout(() => {
        confidenceFill.style.width = `${confidence}%`;
    }, 100);

    // Top 3 predicciones
    displayTopPredictions(data.top_predictions);

    // Crear gráfico de predicciones
    createPredictionsChart(data.top_predictions);

    // Información de la planta
    if (data.plant_info && Object.keys(data.plant_info).length > 0) {
        displayPlantInfo(data.plant_info);
    } else {
        document.getElementById('plantInfoCard').style.display = 'none';
    }

    // Scroll a resultados
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 200);
}

/**
 * Muestra las top predicciones
 */
function displayTopPredictions(predictions) {
    const container = document.getElementById('topPredictions');
    container.innerHTML = '';

    predictions.forEach((pred, index) => {
        const item = document.createElement('div');
        item.className = 'prediction-item';

        const displayName = pred.display_name || formatPlantName(pred.class);

        const header = document.createElement('div');
        header.className = 'prediction-header';

        const title = document.createElement('h4');
        title.textContent = `${index + 1}. ${displayName}`;

        const percentage = document.createElement('span');
        percentage.className = 'prediction-percentage';
        percentage.textContent = `${pred.probability.toFixed(1)}%`;

        header.appendChild(title);
        header.appendChild(percentage);

        const bar = document.createElement('div');
        bar.className = 'prediction-bar';

        const fill = document.createElement('div');
        fill.className = 'prediction-bar-fill';
        setTimeout(() => {
            fill.style.width = `${pred.probability}%`;
        }, 100 + (index * 100));

        bar.appendChild(fill);
        item.appendChild(header);
        item.appendChild(bar);
        container.appendChild(item);
    });
}

/**
 * Crea el gráfico de predicciones con Chart.js
 */
function createPredictionsChart(predictions) {
    // Destruir gráfico anterior si existe
    if (predictionsChart) {
        predictionsChart.destroy();
    }

    const ctx = document.getElementById('predictionsChart');
    if (!ctx) return;

    // Preparar datos
    const labels = predictions.map((pred, index) => {
        const displayName = pred.display_name || formatPlantName(pred.class);
        return displayName.length > 20 ? displayName.substring(0, 20) + '...' : displayName;
    });

    const data = predictions.map(pred => pred.probability.toFixed(1));

    // Colores para tema oscuro
    const colors = [
        'rgba(102, 126, 234, 0.8)',    // Púrpura
        'rgba(33, 147, 176, 0.8)',      // Azul
        'rgba(17, 153, 142, 0.8)'       // Verde
    ];

    const borderColors = [
        'rgba(102, 126, 234, 1)',
        'rgba(33, 147, 176, 1)',
        'rgba(17, 153, 142, 1)'
    ];

    predictionsChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                label: 'Probabilidad (%)',
                data: data,
                backgroundColor: colors,
                borderColor: borderColors,
                borderWidth: 2,
                hoverOffset: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 15,
                        font: {
                            size: 12,
                            weight: '600'
                        },
                        color: '#b4b9c9' // Color para tema oscuro
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(26, 31, 53, 0.95)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    titleColor: '#ffffff',
                    bodyColor: '#b4b9c9',
                    padding: 12,
                    cornerRadius: 8,
                    borderColor: 'rgba(102, 126, 234, 0.3)',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            return ' ' + context.parsed + '%';
                        }
                    }
                }
            },
            animation: {
                animateScale: true,
                animateRotate: true,
                duration: 1000,
                easing: 'easeInOutQuart'
            }
        }
    });
}

/**
 * Muestra la información detallada de la planta
 */
function displayPlantInfo(info) {
    const infoCard = document.getElementById('plantInfoCard');
    infoCard.style.display = 'block';

    // Nombre científico
    if (info.nombre_cientifico) {
        document.getElementById('scientificName').textContent = info.nombre_cientifico;
    }

    // Familia
    if (info.familia) {
        document.getElementById('plantFamily').textContent = info.familia;
    }

    // Usos tradicionales
    if (info.usos_tradicionales && info.usos_tradicionales.length > 0) {
        const usesList = document.getElementById('traditionalUses');
        usesList.innerHTML = '';
        info.usos_tradicionales.forEach((use) => {
            const li = document.createElement('li');
            li.textContent = use;
            usesList.appendChild(li);
        });
    }

    // Propiedades
    if (info.propiedades && info.propiedades.length > 0) {
        const propsContainer = document.getElementById('properties');
        propsContainer.innerHTML = '';
        info.propiedades.forEach((prop) => {
            const tag = document.createElement('span');
            tag.className = 'property-tag';
            tag.textContent = prop;
            propsContainer.appendChild(tag);
        });
    }

    // Modo de uso
    if (info.modo_uso) {
        document.getElementById('usageMode').textContent = info.modo_uso;
    }

    // Precauciones
    if (info.precauciones) {
        document.getElementById('precautions').textContent = info.precauciones;
    }
}

/**
 * Formatea el nombre de la planta
 */
function formatPlantName(name) {
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

/**
 * Muestra un mensaje de error
 */
function showError(message) {
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    previewSection.style.display = 'none';
    uploadBox.style.display = 'none';
    document.getElementById('errorMessage').textContent = message;

    // Scroll al error
    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

// Inicialización
console.log('🌿 Clasificador de Plantas Medicinales cargado');
console.log('🎨 Tema oscuro activado');
console.log('📊 Chart.js integrado');
