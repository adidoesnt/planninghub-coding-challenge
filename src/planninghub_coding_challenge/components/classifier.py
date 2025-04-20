import src.planninghub_coding_challenge.components.utils.csv as csv
import numpy as np

class Classifier:
    def __init__(self, config_path: str):
        print(f"[Classifier] Initialising classifier")
        self.config = self.load_config(config_path)
        
        print(f"[Classifier] Config loaded")

    def load_config(self, config_path: str):
        print(f"[Classifier] Loading config from {config_path}")
        return csv.read_csv(config_path)
    
    def flatten_input(self, data: dict):
        print(f"[Classifier] Flattening input")
        
        condition_type_pairs = self.config[["condition_type", "condition"]].values
        
        flattened = []
        for condition_type, condition in condition_type_pairs:
            value = data.get(condition_type, {}).get(condition, False)
            flattened.append(int(value))
            
        print(f"[Classifier] Flattened input: {flattened}")
            
        return np.array(flattened)
    
    def match_against_columns(self, flattened_input: np.array, columns_to_check):
        print(f"[Classifier] Matching against categories: {columns_to_check}")
        
        input_vector = flattened_input.reshape(-1, 1)
        matrix = self.config[columns_to_check].values
        matches = np.all(matrix == input_vector, axis=0)
        
        print(f"[Classifier] Matches found")
        return matches
    
    def get_matches(self, flattened_input: np.array):
        print(f"[Classifier] Getting matching columns")
        
        category_columns = [col for col in self.config.columns[2:]]
        matches = self.match_against_columns(flattened_input, category_columns)
        
        return matches
    
    def classify(self, data: dict):
        print(f"[Classifier] Classifying data: {data}")
        
        flattened_input = self.flatten_input(data)
        matches = self.get_matches(flattened_input)
        
        if not np.any(matches):
            raise ValueError("Input does not match any categories")
        
        planning_permission_required = np.any(matches)
        return planning_permission_required
    