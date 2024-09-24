import os
from typing import Optional  # Add this import

from dotenv import load_dotenv

# Load environment variables from credentials.env
load_dotenv(".env")


class Config:
    DEBUG: bool = os.environ.get("FLASK_DEBUG", "False").lower() in (
        "true",
        "1",
        "t",
    )

    # MongoDB Configuration
    MONGO_USER: Optional[str] = os.environ.get("MONGO_USER")
    MONGO_PASSWORD: Optional[str] = os.environ.get("MONGO_PASSWORD")
    MONGO_DB: Optional[str] = os.environ.get("MONGO_DB")
    MONGO_COLLECTION: Optional[str] = os.environ.get("MONGO_COLLECTION")
    MONGO_URI: Optional[str] = os.environ.get("MONGO_URI")
