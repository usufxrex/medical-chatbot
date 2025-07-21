import google.generativeai as genai
import os
import time

class AIClient:
    def __init__(self, config_manager):
        self.config = config_manager
        self.api_key = self._get_api_key()
        self.model = None
        self.model_name = None
        self._setup_client()
    
    def _get_api_key(self) -> str:
        api_key = self.config.get('ai.api_key') or os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("Gemini API key not found")
        return api_key
    
    def _setup_client(self):
        try:
            genai.configure(api_key=self.api_key)
            
            models_to_try = [
                'models/gemini-2.0-flash',
                'models/gemini-1.5-flash',
                'gemini-1.5-flash'
            ]
            
            for model_name in models_to_try:
                if self._test_model(model_name):
                    self.model = genai.GenerativeModel(model_name)
                    self.model_name = model_name
                    print(f"✅ AI configured with: {model_name}")
                    return
            
            raise Exception("No working model found")
        except Exception as e:
            print(f"❌ AI setup failed: {e}")
            self.model = None
    
    def _test_model(self, model_name: str) -> bool:
        try:
            test_model = genai.GenerativeModel(model_name)
            response = test_model.generate_content("Hello")
            return bool(response.text)
        except:
            return False
    
    def generate_response(self, prompt: str) -> str:
        if not self.model:
            return "❌ AI service not available"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text if response.text else "No response generated"
        except Exception as e:
            return f"❌ Error: {str(e)[:100]}"
    
    def is_available(self) -> bool:
        return self.model is not None