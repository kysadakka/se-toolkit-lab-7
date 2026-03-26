"""Tool definitions for LLM function calling."""
from services.lms_client import client

# Tool schemas for OpenAI function calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_items",
            "description": "Get list of all labs and tasks",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_learners",
            "description": "Get list of enrolled students and groups",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_scores",
            "description": "Get score distribution for a lab (4 buckets: 0-25, 26-50, 51-75, 76-100)",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier, e.g. 'lab-04'"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_pass_rates",
            "description": "Get per-task average scores and attempt counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_timeline",
            "description": "Get submissions per day for a lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_groups",
            "description": "Get per-group average scores and student counts for a lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_learners",
            "description": "Get top N learners by score for a lab",
            "parameters": {
                "type": "object",
                "properties": {
                    "lab": {"type": "string", "description": "Lab identifier"},
                    "limit": {"type": "integer", "description": "Number of top learners to return", "default": 5}
                },
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_completion_rate",
            "description": "Get completion rate percentage for a lab",
            "parameters": {
                "type": "object",
                "properties": {"lab": {"type": "string", "description": "Lab identifier"}},
                "required": ["lab"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "trigger_sync",
            "description": "Trigger ETL pipeline to refresh data from autochecker",
            "parameters": {"type": "object", "properties": {}, "required": []}
        }
    }
]

# Map tool names to actual functions
FUNCTION_MAP = {
    "get_items": client.get_items,
    "get_learners": client.get_learners,
    "get_scores": lambda **kwargs: client.get_scores(kwargs.get("lab")),
    "get_pass_rates": lambda **kwargs: client.get_pass_rates(kwargs.get("lab")),
    "get_timeline": lambda **kwargs: client.get_timeline(kwargs.get("lab")),
    "get_groups": lambda **kwargs: client.get_groups(kwargs.get("lab")),
    "get_top_learners": lambda **kwargs: client.get_top_learners(kwargs.get("lab"), kwargs.get("limit", 5)),
    "get_completion_rate": lambda **kwargs: client.get_completion_rate(kwargs.get("lab")),
    "trigger_sync": client.trigger_sync,
}

def execute_tool(name: str, args: dict):
    """Execute a tool by name with given arguments."""
    func = FUNCTION_MAP.get(name)
    if not func:
        return f"Unknown tool: {name}"
    try:
        result = func(**args)
        return str(result)[:2000]
    except Exception as e:
        return f"Error executing {name}: {str(e)}"
