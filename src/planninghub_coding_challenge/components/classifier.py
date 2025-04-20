import src.planninghub_coding_challenge.components.utils.csv as csv
import pandas as pd
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

    # TODO: Implement the classification logic
    def classify(self, data: dict):
        print(f"[Classifier] Classifying data: {data}")
        
        flattened_input = self.flatten_input(data)
    