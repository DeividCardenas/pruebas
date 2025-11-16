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
    // Solo abrir el selector de archivos si no se hizo click en el botón
    if (!selectBtn.contains(e.target)) {
        fileInput.click();
    }
});

// Funciones
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleFile(file);
    }
}

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

function displayResults(data) {
    // Mostrar sección de resultados
    resultsSection.style.display = 'block';

    // Nombre de la planta (usar display_name si está disponible)
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

function displayTopPredictions(predictions) {
    const container = document.getElementById('topPredictions');
    container.innerHTML = '';

    predictions.forEach((pred, index) => {
        const item = document.createElement('div');
        item.className = 'prediction-item';

        const name = document.createElement('span');
        name.className = 'prediction-name';
        // Usar display_name si está disponible, si no formatear
        const displayName = pred.display_name || formatPlantName(pred.class);
        name.textContent = `${index + 1}. ${displayName}`;

        const prob = document.createElement('span');
        prob.className = 'prediction-prob';
        prob.textContent = `${pred.probability.toFixed(1)}%`;

        const bar = document.createElement('div');
        bar.className = 'probability-bar';

        const fill = document.createElement('div');
        fill.className = 'probability-fill';
        setTimeout(() => {
            fill.style.width = `${pred.probability}%`;
        }, 100 + (index * 100));

        bar.appendChild(fill);

        const wrapper = document.createElement('div');
        wrapper.style.flex = '1';
        wrapper.appendChild(name);
        wrapper.appendChild(bar);

        item.appendChild(wrapper);
        item.appendChild(prob);

        container.appendChild(item);
    });
}

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

    const colors = [
        'rgba(102, 126, 234, 0.8)',
        'rgba(118, 75, 162, 0.8)',
        'rgba(72, 187, 120, 0.8)'
    ];

    const borderColors = [
        'rgba(102, 126, 234, 1)',
        'rgba(118, 75, 162, 1)',
        'rgba(72, 187, 120, 1)'
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
                        color: '#2d3748'
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(45, 55, 72, 0.95)',
                    titleFont: {
                        size: 14,
                        weight: 'bold'
                    },
                    bodyFont: {
                        size: 13
                    },
                    padding: 12,
                    cornerRadius: 8,
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

function formatPlantName(name) {
    // Convierte "aloe_vera" a "Aloe Vera"
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function showError(message) {
    errorSection.style.display = 'block';
    resultsSection.style.display = 'none';
    document.getElementById('errorMessage').textContent = message;

    // Scroll al error
    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
}

// Inicialización
console.log('🌿 Clasificador de Plantas Medicinales cargado');
console.log('📊 Chart.js integrado');
