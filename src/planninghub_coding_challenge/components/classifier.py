import src.planninghub_coding_challenge.components.utils.csv as csv

class Classifier:
    def __init__(self, config_path: str):
        print(f"[Classifier] Initialising classifier")
        self.config = self.load_config(config_path)
        
        print(f"[Classifier] Config loaded")

    def load_config(self, config_path: str):
        print(f"[Classifier] Loading config from {config_path}")
        return csv.read_csv(config_path)

    # TODO: Implement the classification logic
    def classify(self, data: dict):
        print(f"[Classifier] Classifying data: {data}")
        return True
    