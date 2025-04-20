from fastapi import FastAPI
import uvicorn
import src.planninghub_coding_challenge.constants as constants
from src.planninghub_coding_challenge.components.classifier import Classifier

class Server:
    def __init__(self):
        print(f"[Server] Initialising server")
        
        self.app = FastAPI()
        self.classifier = Classifier(constants.CONFIG_PATH)
        self.init_routes()
        
    def init_routes(self):
        print(f"[Server] Initialising routes")
        
        @self.app.get("/")
        def health_check():
            print(f"[Server] GET /")
            return {"message": "Server is healthy"}
        
        @self.app.post("/classify")
        def classify(data: dict):
            print(f"[Server] POST /classify")
            
            try:
                is_planning_permission_required = self.classifier.classify(data)
                return {
                    "message": "OK",
                    "input_data": data,
                    "result": {
                        "planning_permission_required": is_planning_permission_required
                    }
                }
            except Exception as e:
                print(f"[Server] Error: {e}")
                return {"message": "Error", "error": str(e)}
        
    def run(self):
        print(f"[Server] Running server on {constants.HOST}:{constants.PORT}")
        uvicorn.run(self.app, host=constants.HOST, port=constants.PORT)
