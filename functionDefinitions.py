import uuid

# TOOL definitions as specified in https://platform.openai.com/docs/guides/function-calling

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "start_over",
            "description": "Starts a new process to create a release for the user",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "ask_clarification",
            "description": "Prompts the customer for clarification on their request.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The prompt to ask the customer."
                    }
                },
                "required": ["prompt"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_change_context",
            "description": "Creates a change context",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "Change context title with high-level description of the change."
                    },
                    "module_org": {
                        "type": "string",
                        "description": "The Modul Org (department) responsible for the car component affected by the change."
                    },
                    "derivative": {
                        "type": "string",
                        "description": "The derivative (car component) affected by the change."
                    }
                },
                "required": ["title", "module_org", "derivative"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_kitz",
            "description": "Creates a Change Object (KITZ) associated to a previously created Change Context",
            "parameters": {
                "type": "object",
                "properties": {
                    "problem": {
                        "type": "string",
                        "description": "Description of the problem that this KITZ object is trying to solve."
                    },
                    "benefit": {
                        "type": "string",
                        "description": "Description of the benefits of solving."
                    },
                    "solution": {
                        "type": "string",
                        "description": "Description of the change itself."
                    },
                    "delivery_date": {
                        "type": "string",
                        "description": "Target delivery date for the change in DD/MM/YY format."
                    },
                },
                "required": ["solution", "delivery_date"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_previous_kmnrs",
            "description": "Searches for previously completed Changes (KMNRs) to use as reference for new Change Contexts / Change Objects (KITZ)",
            "parameters": {
                "type": "object",
                "properties": {
                    "search_query": {
                        "type": "string",
                        "description": "Search query."
                    }
                },
                "required": ["search_query"],
                "additionalProperties": False
            }
        }
    }
]


# HANDLERS for the tools with mocked calls to external systems
# `start_over` and `ask_clarification` are special tools not requiring
# any interaction with an external system and are handled directly
# in the orchestrator

def handle_create_change_context(arguments):
    return {
        "id": str(uuid.uuid4()),
        "title": arguments["title"],
        "module_org": arguments["module_org"],
        "derivative": arguments["derivative"]
    }


def handle_create_kitz(arguments):
    return {
        "id": str(uuid.uuid4()),
        "problem": arguments.get("problem", ""),
        "benefit": arguments.get("benefit", ""),
        "solution": arguments["solution"],
        "delivery_date": arguments["delivery_date"]
    }


def handle_search_previous_kmnrs(arguments):
    return [
        {
            "id": str(uuid.uuid4()),
            "module_org": "KE02",
            "derivative": "X12",
            "title": "New mirror cap variant for the X12"
        },
        {
            "id": str(uuid.uuid4()),
            "module_org": "FE04",
            "derivative": "R44",
            "title": "Door hinge issues on R44"
        },
        {
            "id": str(uuid.uuid4()),
            "module_org": "KU12",
            "derivative": "F44",
            "title": "Steering wheel position"
        }
    ]


TOOL_HANDLERS = {
    "create_change_context": handle_create_change_context,
    "create_kitz": handle_create_kitz,
    "search_previous_kmnrs": handle_search_previous_kmnrs
}
