class ChatManager {
    constructor() {
        this.isProcessing = false;
        this.init();
    }
    
    init() {
        this.chatMessages = document.getElementById('chat-messages');
        this.userInput = document.getElementById('user-input');
        this.sendBtn = document.getElementById('send-btn');
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        this.sendBtn.addEventListener('click', () => this.sendMessage());
        
        this.userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }
    
    async sendMessage() {
        const message = this.userInput.value.trim();
        if (!message || this.isProcessing) return;
        
        // Add user message
        this.addMessage(message, 'user');
        this.userInput.value = '';
        this.setProcessing(true);
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            const data = await response.json();
            this.addMessage(data.ai_response, 'bot');
            
        } catch (error) {
            console.error('Chat error:', error);
            this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
        } finally {
            this.setProcessing(false);
        }
    }
    
    addMessage(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        // Convert line breaks and basic formatting
        const formattedContent = content
            .replace(/\n/g, '<br>')
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        contentDiv.innerHTML = formattedContent;
        messageDiv.appendChild(contentDiv);
        this.chatMessages.appendChild(messageDiv);
        
        this.scrollToBottom();
    }
    
    scrollToBottom() {
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }
    
    setProcessing(processing) {
        this.isProcessing = processing;
        this.sendBtn.disabled = processing;
        this.userInput.disabled = processing;
        
        if (processing) {
            this.sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            if (window.app) window.app.showLoading(true);
        } else {
            this.sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
            if (window.app) window.app.showLoading(false);
            this.userInput.focus();
        }
    }
}

// Initialize chat when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat-messages')) {
        window.chatManager = new ChatManager();
    }
});