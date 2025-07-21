// Global app functionality
class App {
    constructor() {
        this.init();
    }
    
    init() {
        console.log('🏥 Medical AI Chatbot initialized');
        this.checkSystemHealth();
    }
    
    async checkSystemHealth() {
        try {
            const response = await fetch('/api/health');
            const data = await response.json();
            console.log('✅ System health:', data);
        } catch (error) {
            console.error('❌ Health check failed:', error);
        }
    }
    
    showLoading(show = true) {
        const loading = document.getElementById('loading');
        if (loading) {
            loading.style.display = show ? 'block' : 'none';
        }
    }
}

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    window.app = new App();
});