import os
from dotenv import load_dotenv

# Load environment variables from credentials.env
load_dotenv(".env")


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1", "t")

    # MongoDB Configuration
    MONGO_USER = os.environ.get("MONGO_USER")
    MONGO_PASSWORD = os.environ.get("MONGO_PASSWORD")
    MONGO_DB = os.environ.get("MONGO_DB")
    MONGO_COLLECTION = os.environ.get("MONGO_COLLECTION")
    MONGO_URI = os.environ.get("MONGO_URI")
