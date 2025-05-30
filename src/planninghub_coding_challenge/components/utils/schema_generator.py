import src.planninghub_coding_challenge.components.utils.csv as csv
import json
import src.planninghub_coding_challenge.constants as constants

class SchemaGenerator:
    '''
    Generates a JSON schema from a CSV file.

    Args:
        config_path (str): The path to the CSV file containing the config.
        schema_path (str): The path to save the generated schema.
    '''
    def __init__(self, config_path: str, schema_path: str):
        print(f"[SchemaGenerator] Initialising schema generator")
        self.config = self.load_config(config_path)
        self.schema_path = schema_path
        
        print(f"[SchemaGenerator] Config loaded")


    '''
    Loads the config from a CSV file.

    Args:
        config_path (str): The path to the CSV file containing the config.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    '''
    def load_config(self, config_path: str):
        print(f"[SchemaGenerator] Loading config from {config_path}")
        return csv.read_csv(config_path)

    '''
    Groups the conditions by condition type.

    Returns:
        dict: A dictionary containing the grouped conditions.
    '''
    def group_conditions(self):
        print(f"[SchemaGenerator] Grouping conditions")
        grouped_conditions = self.config.groupby('condition_type')['condition'].unique()
        
        grouped_conditions_dict = grouped_conditions.to_dict()
        print(f"[SchemaGenerator] Grouped conditions")
        
        return grouped_conditions_dict
    
    '''
    Saves the schema to a JSON file.

    Args:
        schema (dict): The schema to save.
    '''
    def save_schema(self, schema: dict):
        print(f"[SchemaGenerator] Saving schema to {self.schema_path}")
        
        with open(self.schema_path, "w") as f:
            json.dump(schema, f)
            
        print(f"[SchemaGenerator] Schema saved to {self.schema_path}")

    '''
    Generates the schema.

    Returns:
        dict: The generated schema.
    '''
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
        

if __name__ == "__main__":
    schema_generator = SchemaGenerator(constants.CONFIG_PATH, constants.SCHEMA_PATH)
    schema_generator.generate_schema()
