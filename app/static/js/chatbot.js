/**
 * CHATBOT - Asistente Virtual de Plantas Medicinales
 * Sistema inteligente de consultas sobre plantas medicinales
 */

class MedicinalPlantsChatbot {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.conversationHistory = [];
        this.init();
    }

    init() {
        this.createChatbotUI();
        this.attachEventListeners();
        this.showWelcomeMessage();
    }

    createChatbotUI() {
        const chatbotHTML = `
            <div class="chatbot-container">
                <!-- Botón Flotante -->
                <button class="chatbot-fab" id="chatbot-fab" aria-label="Abrir asistente virtual">
                    <i class="fas fa-comment-medical"></i>
                </button>

                <!-- Ventana de Chat -->
                <div class="chatbot-window" id="chatbot-window">
                    <!-- Header -->
                    <div class="chatbot-header">
                        <div class="chatbot-header-content">
                            <div class="chatbot-avatar">
                                <i class="fas fa-leaf"></i>
                            </div>
                            <div class="chatbot-info">
                                <h3>Asistente Herbal</h3>
                                <div class="chatbot-status">
                                    <span class="status-dot"></span>
                                    <span>En línea</span>
                                </div>
                            </div>
                        </div>
                        <button class="chatbot-close" id="chatbot-close" aria-label="Cerrar chat">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>

                    <!-- Área de Mensajes -->
                    <div class="chatbot-messages" id="chatbot-messages">
                        <!-- Los mensajes se insertarán aquí -->
                    </div>

                    <!-- Área de Input -->
                    <div class="chatbot-input-area">
                        <div class="chatbot-input-wrapper">
                            <textarea
                                class="chatbot-input"
                                id="chatbot-input"
                                placeholder="Escribe tu pregunta sobre plantas medicinales..."
                                rows="1"
                            ></textarea>
                            <button class="chatbot-send-btn" id="chatbot-send-btn" aria-label="Enviar mensaje">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        const fab = document.getElementById('chatbot-fab');
        const closeBtn = document.getElementById('chatbot-close');
        const sendBtn = document.getElementById('chatbot-send-btn');
        const input = document.getElementById('chatbot-input');

        fab.addEventListener('click', () => this.toggleChat());
        closeBtn.addEventListener('click', () => this.closeChat());
        sendBtn.addEventListener('click', () => this.sendMessage());

        input.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Auto-resize textarea
        input.addEventListener('input', (e) => {
            e.target.style.height = 'auto';
            e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        const window = document.getElementById('chatbot-window');
        const fab = document.getElementById('chatbot-fab');

        if (this.isOpen) {
            window.classList.add('active');
            fab.classList.add('active');
            document.getElementById('chatbot-input').focus();
        } else {
            window.classList.remove('active');
            fab.classList.remove('active');
        }
    }

    closeChat() {
        this.isOpen = false;
        document.getElementById('chatbot-window').classList.remove('active');
        document.getElementById('chatbot-fab').classList.remove('active');
    }

    showWelcomeMessage() {
        setTimeout(() => {
            this.addBotMessage(
                '¡Hola! Soy tu Asistente Herbal. Puedo ayudarte con información sobre plantas medicinales.',
                true
            );

            // Agregar sugerencias rápidas
            setTimeout(() => {
                this.addQuickReplies([
                    '¿Qué plantas conoces?',
                    'Plantas para dolor de cabeza',
                    'Plantas antiinflamatorias',
                    'Info sobre menta'
                ]);
            }, 500);
        }, 500);
    }

    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();

        if (!message || this.isTyping) return;

        // Agregar mensaje del usuario
        this.addUserMessage(message);
        this.conversationHistory.push({ role: 'user', content: message });

        // Limpiar input
        input.value = '';
        input.style.height = 'auto';

        // Mostrar indicador de escritura
        this.showTypingIndicator();

        try {
            // Enviar consulta al backend
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    history: this.conversationHistory
                })
            });

            const data = await response.json();

            // Ocultar indicador de escritura
            this.hideTypingIndicator();

            if (data.success) {
                this.addBotMessage(data.response, false, data.plant_info);
                this.conversationHistory.push({ role: 'bot', content: data.response });

                // Agregar sugerencias si las hay
                if (data.suggestions && data.suggestions.length > 0) {
                    setTimeout(() => {
                        this.addQuickReplies(data.suggestions);
                    }, 300);
                }
            } else {
                this.addBotMessage('Lo siento, ocurrió un error. Por favor, intenta de nuevo.', false);
            }

        } catch (error) {
            console.error('Error al enviar mensaje:', error);
            this.hideTypingIndicator();
            this.addBotMessage('Lo siento, no pude procesar tu consulta. Verifica tu conexión e intenta de nuevo.', false);
        }
    }

    addUserMessage(text) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const time = this.getCurrentTime();

        const messageHTML = `
            <div class="message user">
                <div class="message-content">
                    <div class="message-bubble">${this.escapeHtml(text)}</div>
                    <div class="message-time">${time}</div>
                </div>
                <div class="message-avatar">
                    <i class="fas fa-user"></i>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
    }

    addBotMessage(text, isWelcome = false, plantInfo = null) {
        const messagesContainer = document.getElementById('chatbot-messages');
        const time = this.getCurrentTime();

        let messageContent = `<div class="message-bubble">${this.formatBotMessage(text)}</div>`;

        // Si hay información de planta, agregar tarjeta
        if (plantInfo) {
            messageContent += this.createPlantCard(plantInfo);
        }

        const messageHTML = `
            <div class="message bot">
                <div class="message-avatar">
                    <i class="fas fa-leaf"></i>
                </div>
                <div class="message-content">
                    ${messageContent}
                    <div class="message-time">${time}</div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', messageHTML);
        this.scrollToBottom();
    }

    createPlantCard(plantInfo) {
        const properties = plantInfo.propiedades ?
            plantInfo.propiedades.slice(0, 3).map(prop =>
                `<span class="property-tag">${prop}</span>`
            ).join('') : '';

        return `
            <div class="plant-card">
                <div class="plant-card-header">
                    <i class="fas fa-seedling"></i>
                    <div>
                        <h4>${plantInfo.nombre_comun}</h4>
                        <p><em>${plantInfo.nombre_cientifico}</em></p>
                    </div>
                </div>
                ${properties ? `<div class="plant-properties">${properties}</div>` : ''}
            </div>
        `;
    }

    addQuickReplies(suggestions) {
        const messagesContainer = document.getElementById('chatbot-messages');

        const quickRepliesHTML = `
            <div class="message bot">
                <div class="message-avatar">
                    <i class="fas fa-leaf"></i>
                </div>
                <div class="message-content">
                    <div class="quick-replies">
                        ${suggestions.map(suggestion =>
                            `<button class="quick-reply-btn" onclick="chatbot.handleQuickReply('${this.escapeHtml(suggestion)}')">${suggestion}</button>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', quickRepliesHTML);
        this.scrollToBottom();
    }

    handleQuickReply(text) {
        const input = document.getElementById('chatbot-input');
        input.value = text;
        this.sendMessage();
    }

    showTypingIndicator() {
        this.isTyping = true;
        const messagesContainer = document.getElementById('chatbot-messages');

        const typingHTML = `
            <div class="message bot" id="typing-indicator">
                <div class="message-avatar">
                    <i class="fas fa-leaf"></i>
                </div>
                <div class="message-content">
                    <div class="message-bubble">
                        <div class="typing-indicator">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        messagesContainer.insertAdjacentHTML('beforeend', typingHTML);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        this.isTyping = false;
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    formatBotMessage(text) {
        // Convertir saltos de línea a <br>
        text = text.replace(/\n/g, '<br>');

        // Convertir **texto** a negrita
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

        // Convertir listas con viñetas
        text = text.replace(/• (.*?)(<br>|$)/g, '<br>• $1$2');

        return text;
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    getCurrentTime() {
        const now = new Date();
        return now.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' });
    }

    scrollToBottom() {
        const messagesContainer = document.getElementById('chatbot-messages');
        setTimeout(() => {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }, 100);
    }
}

// Inicializar chatbot cuando el DOM esté listo
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new MedicinalPlantsChatbot();
});
