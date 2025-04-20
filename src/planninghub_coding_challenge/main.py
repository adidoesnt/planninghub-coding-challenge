from src.planninghub_coding_challenge.components.server import Server
from src.planninghub_coding_challenge.components.utils.schema_generator import SchemaGenerator
import src.planninghub_coding_challenge.constants as constants

if __name__ == "__main__":
    try:
        # TODO: Make schema generation part of the build process
        schema_generator = SchemaGenerator(config_path=constants.CONFIG_PATH, schema_path=constants.SCHEMA_PATH)
        schema = schema_generator.generate_schema()
        
        server = Server()
        server.run()
        
    except Exception as e:
        print(f"[Main] Error: {e}")
        exit(1)
