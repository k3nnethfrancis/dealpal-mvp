import os
import dotenv

# Load API keys
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")