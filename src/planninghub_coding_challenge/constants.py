from dotenv import load_dotenv
import os

load_dotenv()

CONFIG_PATH = os.getenv("CONFIG_PATH", "./config/planning-permission-rules-config.csv")
SCHEMA_PATH = os.getenv("SCHEMA_PATH", "./config/schema.json")