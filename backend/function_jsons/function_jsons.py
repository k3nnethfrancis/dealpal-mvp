function_json = {
    'search_tool': {
        "name": "run_search",
        "description": "Executes a web search procedure for answers to any query.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
            },
            "required": ["query"],
        },
    },
    'scraper_tool': {
        "name": "run_selenium",
        "description": "Executes an automated process in a web browser using Selenium, based on the provided category. It does not return any value.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "The category on which to execute the Selenium process."
                }
            },
            "required": ["category"]
        },
        "returns": {
            "description": "Does not return any value (None)."
            }
    }
}