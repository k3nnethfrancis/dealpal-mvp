import json
# utils
def show_json(obj):
    print(json.loads(obj.model_dump_json()))
