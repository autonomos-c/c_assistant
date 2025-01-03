from .base_agent import BaseLegalAgent
from typing import Dict
from .groq_integration import GroqIntegration
from dotenv import load_dotenv
from pathlib import Path

# Cargar variables de entorno
load_dotenv(Path(__file__).parent.parent / '.env')

class AnalystAgent(BaseLegalAgent):
    def __init__(self):
        super().__init__("analyst")
        self.groq = GroqIntegration()
        
    def handle(self, request: Dict) -> Dict:
        if not self.validate_request(request):
            return self.prepare_response("Invalid request format", {"error": True})
            
        context = request.get("context", "")
        question = request.get("question", "")
        
        messages = [
            {"role": "system", "content": "Eres un Analista y Asesor Legal AI especializado en análisis de riesgos legales y asesoría estratégica. Proporcionas evaluaciones detalladas de riesgos y recomendaciones para mitigarlos."},
            {"role": "user", "content": context},
            {"role": "user", "content": question}
        ]
        
        try:
            response = self.groq.get_chat_completion(messages)
            return self.prepare_response(response, {"source": "groq"})
        except Exception as e:
            return self.prepare_response(f"Error processing request: {str(e)}", {"error": True})