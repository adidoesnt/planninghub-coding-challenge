from dotenv import load_dotenv
import os

load_dotenv()

# Server
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", "8080"))

# Classifier
CONFIG_PATH = os.getenv("CONFIG_PATH", "./config/planning-permission-rules-config.csv")
SCHEMA_PATH = os.getenv("SCHEMA_PATH", "./config/schema.json")
SAMPLE_INPUT_PATH = os.getenv("SAMPLE_INPUT_PATH", "./config/sample-input.json")
