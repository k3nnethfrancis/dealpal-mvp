function_jsons = {
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
    },
    "email_sender_tool": {
        "name": "send_email",
        "description": "Sends an email using provided sender and receiver details, subject, and text.",
        "parameters": {
            "type": "object",
            "properties": {
                "sender_email": {"type": "string"},
                "receiver_email": {"type": "string"},
                "subject": {"type": "string"},
                "text": {"type": "string"}
            },
            "required": ["sender_email", "receiver_email", "subject", "text"]
        },
        "returns": {
            "description": "Returns the response of the email sending process, including status codes and any messages."
        }
    }
}