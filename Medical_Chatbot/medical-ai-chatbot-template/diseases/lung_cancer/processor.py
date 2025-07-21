import csv
import json
from typing import Dict, List, Any
from pathlib import Path
from core.base_processor import BaseDiseaseProcessor

class LungCancerProcessor(BaseDiseaseProcessor):
    def __init__(self):
        super().__init__("lung_cancer")
        self.data_list = self._load_csv_as_list()
    
    def _load_csv_as_list(self) -> List[Dict[str, Any]]:
        """Load CSV data as list of dictionaries (pandas replacement)"""
        data_path = self.disease_path / "data.csv"
        data_list = []
        
        if data_path.exists():
            try:
                with open(data_path, 'r', encoding='utf-8') as file:
                    csv_reader = csv.DictReader(file)
                    for row in csv_reader:
                        # Convert numeric columns
                        processed_row = {}
                        for key, value in row.items():
                            # Clean the key (remove spaces)
                            clean_key = key.strip()
                            clean_value = value.strip() if isinstance(value, str) else value
                            
                            # Try to convert to number if possible
                            if clean_value.isdigit():
                                processed_row[clean_key] = int(clean_value)
                            elif clean_value in ['YES', 'NO', 'M', 'F']:
                                processed_row[clean_key] = clean_value
                            else:
                                try:
                                    processed_row[clean_key] = float(clean_value)
                                except ValueError:
                                    processed_row[clean_key] = clean_value
                        data_list.append(processed_row)
                
                print(f"✅ Loaded {len(data_list)} records for {self.disease_name}")
                return data_list
            except Exception as e:
                print(f"❌ Error loading {self.disease_name} data: {e}")
                return []
        else:
            print(f"⚠️ No data file found at: {data_path}")
            return []
    
    def get_statistics(self) -> Dict[str, Any]:
        """Return comprehensive lung cancer statistics"""
        if not self.data_list:
            return {"error": "No data available"}
        
        # Basic calculations
        total_records = len(self.data_list)
        cancer_cases = len([row for row in self.data_list if row.get('LUNG_CANCER') == 'YES'])
        non_cancer_cases = total_records - cancer_cases
        cancer_rate = (cancer_cases / total_records * 100) if total_records > 0 else 0
        
        stats = {
            "dataset_overview": {
                "total_records": total_records,
                "cancer_cases": cancer_cases,
                "non_cancer_cases": non_cancer_cases,
                "cancer_rate": round(cancer_rate, 2)
            },
            "demographics": self._get_demographics(),
            "symptoms": self._get_symptoms_stats()
        }
        
        return stats
    
    def _get_demographics(self) -> Dict[str, Any]:
        """Get demographic statistics"""
        demographics = {}
        
        # Age statistics
        ages = [row.get('AGE', 0) for row in self.data_list if 'AGE' in row and isinstance(row.get('AGE'), (int, float))]
        if ages:
            demographics['age'] = {
                "mean": round(sum(ages) / len(ages), 1),
                "min": min(ages),
                "max": max(ages)
            }
        
        # Gender statistics
        genders = [row.get('GENDER') for row in self.data_list if 'GENDER' in row and row.get('GENDER')]
        if genders:
            gender_counts = {}
            for gender in genders:
                gender_counts[gender] = gender_counts.get(gender, 0) + 1
            demographics['gender'] = gender_counts
        
        return demographics
    
    def _get_symptoms_stats(self) -> Dict[str, Any]:
        """Get symptom prevalence statistics"""
        symptom_stats = {}
        
        # Define symptom columns (exclude non-symptoms)
        exclude_cols = {'AGE', 'GENDER', 'LUNG_CANCER'}
        
        if self.data_list:
            # Get all column names from first row
            all_columns = set(self.data_list[0].keys())
            symptom_cols = all_columns - exclude_cols
            
            for symptom in symptom_cols:
                # Count cases where symptom = 2 (present)
                total_cases = len([row for row in self.data_list if row.get(symptom) == 2])
                prevalence = (total_cases / len(self.data_list) * 100) if len(self.data_list) > 0 else 0
                
                symptom_stats[symptom] = {
                    "total_cases": total_cases,
                    "prevalence_percent": round(prevalence, 2)
                }
        
        return symptom_stats
    
    def generate_insights(self, query: str) -> str:
        """Generate disease-specific insights"""
        stats = self.get_statistics()
        
        if 'error' in stats:
            return "No lung cancer data available for analysis."
        
        overview = stats['dataset_overview']
        context = f"""
LUNG CANCER DATASET ANALYSIS ({overview['total_records']} patients):

OVERVIEW:
- Total cases: {overview['total_records']}
- Cancer cases: {overview['cancer_cases']} ({overview['cancer_rate']}%)
- Non-cancer cases: {overview['non_cancer_cases']}

DEMOGRAPHICS:
"""
        
        if 'demographics' in stats and 'age' in stats['demographics']:
            age_info = stats['demographics']['age']
            context += f"- Age range: {age_info['min']}-{age_info['max']} years (average: {age_info['mean']})\n"
        
        if 'demographics' in stats and 'gender' in stats['demographics']:
            gender_info = stats['demographics']['gender']
            context += f"- Gender distribution: {gender_info}\n"
        
        context += "\nTOP SYMPTOMS:\n"
        if 'symptoms' in stats:
            # Get top 5 symptoms by prevalence
            sorted_symptoms = sorted(stats['symptoms'].items(), 
                                   key=lambda x: x[1]['prevalence_percent'], 
                                   reverse=True)[:5]
            
            for symptom, data in sorted_symptoms:
                symptom_name = symptom.replace('_', ' ').title()
                context += f"- {symptom_name}: {data['prevalence_percent']}% ({data['total_cases']} cases)\n"
        
        return context
    
    def get_basic_info(self) -> Dict[str, Any]:
        """Override to include actual record count"""
        basic_info = super().get_basic_info()
        basic_info['total_records'] = len(self.data_list)
        return basic_info