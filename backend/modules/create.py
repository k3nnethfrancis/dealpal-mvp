import os
import yaml
from backend.base import BaseConfig

config = BaseConfig(__name__)

def fetch_and_print_all_assistants(client):
    print("Fetching all existing assistants for verification...")
    existing_assistants = client.beta.assistants.list(limit=100)
    for assistant in existing_assistants:
        print(f"Assistant Name: {assistant.name}, ID: {assistant.id}")

def main():
    agents_path = r'/Users/eb/PycharmProjects/dealpal-mvp/backend/agents'
    client = config.get_openai_client()

    # Check and log the existence of the agents directory
    if not os.path.exists(agents_path) or not os.path.isdir(agents_path):
        raise ValueError('The "agents" folder is missing or not a directory.')
    else:
        print(f"The 'agents' directory exists at {agents_path}")

    # Iterate through each file in the agents directory
    for file_name in os.listdir(agents_path):
        # Check if the file is a YAML file
        if file_name.endswith('.yaml'):
            print(f"\nProcessing YAML file: {file_name}")
            yaml_file_path = os.path.join(agents_path, file_name)

            with open(yaml_file_path, 'r') as file:
                agent_config = yaml.safe_load(file)

                # Log all data pulled from YAML
                print("Agent configuration from YAML:")
                for key, value in agent_config.items():
                    print(f"  {key}: {value}")

                # Extract and log configuration details
                assistant_id = agent_config.get('ID')
                assistant_name = agent_config.get('name')
                instructions = agent_config.get('instructions')
                model = agent_config.get('model')
                tools = [{"type": agent_config.get('tools')}]

                print(f"\nAttempting to process assistant: {assistant_name}")
                if assistant_id is None or assistant_id == "":
                    print(f"Assistant ID is empty or None. Creating a new assistant.")
                    # Create a new assistant
                    assistant = client.beta.assistants.create(
                        name=assistant_name,
                        instructions=instructions,
                        model=model,
                        tools=tools
                    )
                    print(f"Created new assistant: {assistant_name}, ID: {assistant.id}")
                else:
                    try:
                        print(f"Existing assistant ID found: {assistant_id}. Updating assistant.")
                        # Attempt to update an existing assistant
                        assistant = client.beta.assistants.update(
                            assistant_id=assistant_id,
                            name=assistant_name,
                            instructions=instructions,
                            model=model,
                            tools=tools
                        )
                        print(f"Updated assistant: {assistant_name}, ID: {assistant.id}")
                    except KeyError as e:
                        # Log the error if the assistant ID does not exist
                        print(f"Error updating assistant: {assistant_name}. KeyError: {e}")
        else:
            print(f"Skipping non-YAML file: {file_name}")

    print("\nProcess completed.")

if __name__ == "__main__":
    client = config.get_openai_client()
    main()
    fetch_and_print_all_assistants(client)
