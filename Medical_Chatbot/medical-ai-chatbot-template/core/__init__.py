"""Medical AI Chatbot Core Module"""
__version__ = "1.0.0"

from .config_manager import ConfigManager
from .disease_manager import DiseaseManager
from .base_processor import BaseDiseaseProcessor
from .disease_detector import DiseaseDetector
from .ai_client import AIClient

__all__ = [
    'ConfigManager',
    'DiseaseManager', 
    'BaseDiseaseProcessor',
    'DiseaseDetector',
    'AIClient'
]