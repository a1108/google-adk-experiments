import os

from dotenv import load_dotenv


def load_environment():
    """
    Load environment variables from .env file.
    """

    load_dotenv()

    print(".env loaded successfully.")

    print("Vertex AI :", os.getenv("GOOGLE_GENAI_USE_VERTEXAI"))
    print("Project   :", os.getenv("GOOGLE_CLOUD_PROJECT"))
    print("Location  :", os.getenv("GOOGLE_CLOUD_LOCATION"))