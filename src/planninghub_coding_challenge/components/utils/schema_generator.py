import src.planninghub_coding_challenge.components.utils.csv as csv
import json

class SchemaGenerator:
    def __init__(self, config_path: str, schema_path: str):
        print(f"[SchemaGenerator] Initialising schema generator")
        self.config = self.load_config(config_path)
        self.schema_path = schema_path
        
        print(f"[SchemaGenerator] Config loaded")

    def load_config(self, config_path: str):
        print(f"[SchemaGenerator] Loading config from {config_path}")
        return csv.read_csv(config_path)
    
    def group_conditions(self):
        print(f"[SchemaGenerator] Grouping conditions")
        grouped_conditions = self.config.groupby('condition_type')['condition'].unique()
        
        grouped_conditions_dict = grouped_conditions.to_dict()
        print(f"[SchemaGenerator] Grouped conditions")
        
        return grouped_conditions_dict
    
    def save_schema(self, schema: dict):
        print(f"[SchemaGenerator] Saving schema to {self.schema_path}")
        
        with open(self.schema_path, "w") as f:
            json.dump(schema, f)
            
        print(f"[SchemaGenerator] Schema saved to {self.schema_path}")
            
    def generate_schema(self):
        print(f"[SchemaGenerator] Generating schema")
        
        grouped_conditions = self.group_conditions()
        
        schema = {
            "type": "object",
            "properties": {}
        }
        
        for condition_type, conditions in grouped_conditions.items():
            schema["properties"][condition_type] = {
                "type": "object",
                "properties": {
                    condition: {"type": "boolean"} for condition in conditions
                }
            }
            
        print(f"[SchemaGenerator] Generated schema")
        
        self.save_schema(schema)
