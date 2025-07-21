import re
from typing import List

class DiseaseDetector:
    def __init__(self):
        self.disease_keywords = {
            'lung_cancer': ['lung', 'cancer', 'smoking', 'cough', 'chest', 'breath', 'tobacco'],
            'general_health': ['health', 'medical', 'symptoms', 'disease']
        }
    
    def detect_diseases(self, query: str) -> List[str]:
        query_lower = query.lower()
        detected = []
        
        for disease, keywords in self.disease_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                detected.append(disease)
        
        return detected if detected else ['lung_cancer']  # Default
    
    def is_medical_query(self, query: str) -> bool:
        medical_terms = ['health', 'medical', 'symptom', 'disease', 'cancer', 'pain', 'treatment']
        query_lower = query.lower()
        return any(term in query_lower for term in medical_terms)