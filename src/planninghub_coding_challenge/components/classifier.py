import src.planninghub_coding_challenge.components.utils.csv as csv
import src.planninghub_coding_challenge.constants as constants
import numpy as np
import json
import jsonschema

class Classifier:
    '''
    Initializes the classifier.

    Args:
        config_path (str): The path to the CSV file containing the config.
    '''
    def __init__(self, config_path: str):
        print(f"[Classifier] Initialising classifier")
        self.config = self.load_config(config_path)
        
        print(f"[Classifier] Config loaded")

    '''
    Loads the config from a CSV file.

    Args:
        config_path (str): The path to the CSV file containing the config.

    Returns:
        pd.DataFrame: A pandas DataFrame containing the data from the CSV file.
    '''
    def load_config(self, config_path: str):
        print(f"[Classifier] Loading config from {config_path}")
        return csv.read_csv(config_path)
    
    '''
    Flattens the input data.

    Args:
        data (dict): The input data.

    Returns:
        np.array: A numpy array containing the flattened input data.
    '''
    def flatten_input(self, data: dict):
        print(f"[Classifier] Flattening input")
        
        condition_type_pairs = self.config[["condition_type", "condition"]].values
        
        flattened = []
        for condition_type, condition in condition_type_pairs:
            value = data.get(condition_type, {}).get(condition, False)
            flattened.append(int(value))
            
        print(f"[Classifier] Flattened input: {flattened}")
            
        return np.array(flattened)
    
    '''
    Matches the input against the columns.

    Args:
        flattened_input (np.array): The flattened input data.
        columns_to_check (list): The columns to check.
        is_universal (bool): Whether the columns are universal.

    Returns:
        np.array: A numpy array containing the matches.
    '''
    def match_against_columns(self, flattened_input: np.array, columns_to_check, is_universal: bool):
        print(f"[Classifier] Matching against categories: {columns_to_check}")
        
        input_vector = flattened_input.reshape(-1, 1) # Reshape the input vector to a column vector
        matrix = self.config[columns_to_check].values
        
        if is_universal:
            matches = []
            for col in range(matrix.shape[1]):
                category_ones = matrix[:, col] == 1
                input_matches = input_vector[category_ones] == 1
                matches.append(np.any(input_matches))
            matches = np.array(matches)
        else:
            matches = np.all(matrix == input_vector, axis=0)
        
        if not np.any(matches):
            print("[Classifier] No matches found")
        else:
            print(f"[Classifier] Matches found: {matches}")
        
        return matches
    
    '''
    Gets the matches for the input.

    Args:
        flattened_input (np.array): The flattened input data.

    Returns:
        bool: Whether the input matches any categories.
    '''    
    def get_matches(self, flattened_input: np.array):
        print(f"[Classifier] Getting matching columns")
        
        category_columns = [col for col in self.config.columns[2:]]
        
        # Get the row that indicates if categories are universal or not
        universal_row = self.config[self.config['condition_type'] == 'other'][self.config['condition'] == 'universal_category']
        universal_flags = universal_row[category_columns].values[0]
        
        # Use the universal flags to split the columns into universal and other columns
        universal_columns = [col for col, is_universal in zip(category_columns, universal_flags) if is_universal]
        other_columns = [col for col, is_universal in zip(category_columns, universal_flags) if not is_universal]
        
        # Get the planning permission requirements for each category
        permission_row = self.config[self.config['condition_type'] == 'metadata'][self.config['condition'] == 'requires_planning_permission']
        requires_permission = permission_row[category_columns].values[0]
        
        if universal_columns:
            universal_matches = self.match_against_columns(flattened_input, universal_columns, is_universal=True)
            if np.any(universal_matches):
                print(f"[Classifier] Universal category match found")
                return True  # Universal categories always require permission
        
        if other_columns:
            other_matches = self.match_against_columns(flattened_input, other_columns, is_universal=False)
            
            # First check if we have any matches at all
            if len(other_matches) == 0:
                raise ValueError("Input does not match any categories")
            
            # If we have matches, check if any of them require permission
            matching_permissions = requires_permission[len(universal_columns):][other_matches]
            return np.any(matching_permissions)
            
        return False
    '''
    Validates the input data.

    Args:
        data (dict): The input data.
        
    Raises:
        jsonschema.exceptions.ValidationError: If the input data is invalid.
    '''
    def validate_input_data(self, data: dict):
        print(f"[Classifier] Validating input data: {data}")
        
        with open(constants.SCHEMA_PATH) as f:
            schema = json.load(f)
            
        jsonschema.validate(instance=data, schema=schema)
        
        return True
    
    '''
    Classifies the input data.

    Args:
        data (dict): The input data.
        
    Returns:
        bool: Whether planning permission is required.
    '''
    def classify(self, data: dict):
        print(f"[Classifier] Classifying data: {data}")
        
        self.validate_input_data(data)
        flattened_input = self.flatten_input(data)
        matches = self.get_matches(flattened_input)
        
        planning_permission_required = bool(np.any(matches))
        return planning_permission_required
    