import os
import yaml
import dotenv
import json

# Load API keys
dotenv.load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

AGENT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "agents")
ARI_CONFIG_PATH = os.path.join(AGENT_CONFIG_PATH, "ari.yaml")

# pull in Ari assistant ID from yaml config
with open(ARI_CONFIG_PATH, "r") as f:
    ari_config = yaml.safe_load(f)

ASSISTANT_ID = ari_config.get("ID")


# utils
def show_json(obj):
    print(json.loads(obj.model_dump_json()))