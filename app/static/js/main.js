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
retryBtn.addEventListener('click', resetUpload');

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

uploadBox.addEventListener('click', (e) => {
    if (e.target !== selectBtn && !selectBtn.contains(e.target)) {
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

    // Mostrar preview con animación
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        uploadBox.style.display = 'none';
        previewSection.style.display = 'block';

        // Agregar efecto de fade in
        previewSection.style.opacity = '0';
        setTimeout(() => {
            previewSection.style.transition = 'opacity 0.5s ease';
            previewSection.style.opacity = '1';
        }, 10);
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

    // Mostrar loading con animación
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
    // Mostrar sección de resultados con animación
    resultsSection.style.display = 'block';
    resultsSection.style.opacity = '0';
    setTimeout(() => {
        resultsSection.style.transition = 'opacity 0.6s ease';
        resultsSection.style.opacity = '1';
    }, 10);

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

    // Scroll suave a resultados
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

        // Animación escalonada
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';

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

        // Animar entrada
        setTimeout(() => {
            item.style.transition = 'all 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, 100 + (index * 100));
    });
}

function createPredictionsChart(predictions) {
    // Destruir gráfico anterior si existe
    if (predictionsChart) {
        predictionsChart.destroy();
    }

    const ctx = document.getElementById('predictionsChart').getContext('2d');

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
                duration: 1500,
                easing: 'easeInOutQuart'
            }
        }
    });
}

function displayPlantInfo(info) {
    const infoCard = document.getElementById('plantInfoCard');
    infoCard.style.display = 'block';

    // Animación de entrada
    infoCard.style.opacity = '0';
    infoCard.style.transform = 'translateY(20px)';
    setTimeout(() => {
        infoCard.style.transition = 'all 0.6s ease';
        infoCard.style.opacity = '1';
        infoCard.style.transform = 'translateY(0)';
    }, 300);

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
        info.usos_tradicionales.forEach((use, index) => {
            const li = document.createElement('li');
            li.textContent = use;
            li.style.opacity = '0';
            li.style.transform = 'translateX(-10px)';
            usesList.appendChild(li);

            // Animación escalonada
            setTimeout(() => {
                li.style.transition = 'all 0.4s ease';
                li.style.opacity = '1';
                li.style.transform = 'translateX(0)';
            }, 400 + (index * 80));
        });
    }

    // Propiedades
    if (info.propiedades && info.propiedades.length > 0) {
        const propsContainer = document.getElementById('properties');
        propsContainer.innerHTML = '';
        info.propiedades.forEach((prop, index) => {
            const tag = document.createElement('span');
            tag.className = 'property-tag';
            tag.textContent = prop;
            tag.style.opacity = '0';
            tag.style.transform = 'scale(0.8)';
            propsContainer.appendChild(tag);

            // Animación escalonada
            setTimeout(() => {
                tag.style.transition = 'all 0.4s ease';
                tag.style.opacity = '1';
                tag.style.transform = 'scale(1)';
            }, 400 + (index * 100));
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

    // Animación de entrada
    errorSection.style.opacity = '0';
    setTimeout(() => {
        errorSection.style.transition = 'opacity 0.5s ease';
        errorSection.style.opacity = '1';
    }, 10);

    // Scroll al error
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// Añadir efecto de partículas de fondo (opcional)
function createFloatingLeaves() {
    const body = document.body;
    const leafIcons = ['🍃', '🌿', '🍀', '🌱'];

    for (let i = 0; i < 15; i++) {
        const leaf = document.createElement('div');
        leaf.textContent = leafIcons[Math.floor(Math.random() * leafIcons.length)];
        leaf.style.position = 'fixed';
        leaf.style.fontSize = `${Math.random() * 20 + 15}px`;
        leaf.style.left = `${Math.random() * 100}%`;
        leaf.style.top = `-50px`;
        leaf.style.opacity = '0.15';
        leaf.style.pointerEvents = 'none';
        leaf.style.zIndex = '0';
        leaf.style.animation = `fall ${Math.random() * 10 + 10}s linear infinite`;
        leaf.style.animationDelay = `${Math.random() * 5}s`;

        body.appendChild(leaf);
    }
}

// Añadir animación de caída
const style = document.createElement('style');
style.textContent = `
    @keyframes fall {
        0% {
            transform: translateY(-50px) rotate(0deg);
            opacity: 0.15;
        }
        50% {
            opacity: 0.2;
        }
        100% {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Inicialización
console.log('🌿 Clasificador de Plantas Medicinales cargado');
console.log('📊 Chart.js integrado');

// Crear hojas flotantes (opcional, descomentar si se desea)
// createFloatingLeaves();

// Efecto de escritura en el header (opcional)
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

// Añadir efectos de hover a los botones
document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
    button.addEventListener('mouseenter', function(e) {
        const rect = this.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;

        const ripple = document.createElement('span');
        ripple.style.cssText = `
            position: absolute;
            width: 20px;
            height: 20px;
            background: rgba(255, 255, 255, 0.4);
            border-radius: 50%;
            pointer-events: none;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            left: ${x}px;
            top: ${y}px;
        `;

        this.appendChild(ripple);

        setTimeout(() => ripple.remove(), 600);
    });
});

// Añadir animación de ripple
const rippleStyle = document.createElement('style');
rippleStyle.textContent = `
    @keyframes ripple {
        to {
            transform: scale(20);
            opacity: 0;
        }
    }
`;
document.head.appendChild(rippleStyle);

// Contador de animación para las estadísticas
function animateCounter(element, target, duration = 1000) {
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            current = target;
            clearInterval(timer);
        }
        element.textContent = Math.floor(current);
    }, 16);
}

// Observador de intersección para animaciones al hacer scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observar elementos con clase 'fade-in-on-scroll'
document.querySelectorAll('.result-card, .predictions-card, .info-card').forEach(el => {
    observer.observe(el);
});
