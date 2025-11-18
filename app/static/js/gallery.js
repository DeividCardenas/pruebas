/**
 * Gallery - Sistema de galería de plantas medicinales
 */

// Elementos del DOM
const searchInput = document.getElementById('searchInput');
const plantsGrid = document.getElementById('plantsGrid');
const noResults = document.getElementById('noResults');
const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.getElementById('modalContent');

/**
 * Búsqueda de plantas
 */
if (searchInput) {
    searchInput.addEventListener('input', function() {
        const searchTerm = this.value.toLowerCase().trim();
        const plantCards = plantsGrid.querySelectorAll('.plant-card');
        let visibleCount = 0;

        plantCards.forEach(card => {
            const plantName = card.dataset.plantName;
            const isVisible = plantName.includes(searchTerm);

            if (isVisible) {
                card.style.display = 'block';
                visibleCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Mostrar mensaje si no hay resultados
        if (visibleCount === 0) {
            noResults.style.display = 'block';
            plantsGrid.style.display = 'none';
        } else {
            noResults.style.display = 'none';
            plantsGrid.style.display = 'grid';
        }
    });
}

/**
 * Muestra el modal con los detalles de la planta
 */
function showPlantDetails(plantKey) {
    const plant = plantsData[plantKey];

    if (!plant) {
        console.error('Planta no encontrada:', plantKey);
        return;
    }

    // Generar contenido del modal
    let content = `
        <div class="modal-header">
            <h2 class="modal-title">${plant.nombre_comun.split(',')[0]}</h2>
            <p class="modal-scientific">${plant.nombre_cientifico}</p>
            <div class="modal-family">
                <i class="fas fa-dna"></i>
                <span>${plant.familia}</span>
            </div>
        </div>
    `;

    // Usos tradicionales
    if (plant.usos_tradicionales && plant.usos_tradicionales.length > 0) {
        content += `
            <div class="modal-section">
                <h3 class="modal-section-title">
                    <i class="fas fa-pills"></i>
                    Usos Tradicionales
                </h3>
                <div class="modal-section-content">
                    <ul>
                        ${plant.usos_tradicionales.map(uso => `<li>${uso}</li>`).join('')}
                    </ul>
                </div>
            </div>
        `;
    }

    // Propiedades
    if (plant.propiedades && plant.propiedades.length > 0) {
        content += `
            <div class="modal-section">
                <h3 class="modal-section-title">
                    <i class="fas fa-star"></i>
                    Propiedades
                </h3>
                <div class="modal-section-content">
                    <div class="modal-properties">
                        ${plant.propiedades.map(prop => `
                            <span class="modal-property-tag">${prop}</span>
                        `).join('')}
                    </div>
                </div>
            </div>
        `;
    }

    // Modo de uso
    if (plant.modo_uso) {
        content += `
            <div class="modal-section">
                <h3 class="modal-section-title">
                    <i class="fas fa-book-medical"></i>
                    Modo de Uso
                </h3>
                <div class="modal-section-content">
                    <p>${plant.modo_uso}</p>
                </div>
            </div>
        `;
    }

    // Precauciones
    if (plant.precauciones) {
        content += `
            <div class="modal-warning">
                <h4>
                    <i class="fas fa-exclamation-triangle"></i>
                    Precauciones
                </h4>
                <p>${plant.precauciones}</p>
            </div>
        `;
    }

    modalContent.innerHTML = content;
    modalOverlay.style.display = 'flex';
    document.body.style.overflow = 'hidden';
}

/**
 * Cierra el modal
 */
function closeModal() {
    modalOverlay.style.display = 'none';
    document.body.style.overflow = '';
}

// Cerrar modal al hacer click fuera
modalOverlay.addEventListener('click', function(e) {
    if (e.target === modalOverlay) {
        closeModal();
    }
});

// Cerrar modal con la tecla ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modalOverlay.style.display === 'flex') {
        closeModal();
    }
});

console.log('🌿 Galería de plantas cargada');
console.log(`📊 ${Object.keys(plantsData).length} plantas disponibles`);
