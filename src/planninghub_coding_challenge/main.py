from src.planninghub_coding_challenge.components.server import Server
from src.planninghub_coding_challenge.components.utils.schema_generator import SchemaGenerator

if __name__ == "__main__":
    try:
        server = Server()
        server.run()
        
    except Exception as e:
        print(f"[Main] Error: {e}")
        exit(1)
