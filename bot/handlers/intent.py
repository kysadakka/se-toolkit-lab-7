"""Intent router using LLM with tools."""
import sys
import json
from pathlib import Path

bot_dir = Path(__file__).parent.parent
if str(bot_dir) not in sys.path:
    sys.path.insert(0, str(bot_dir))

from services.llm_client import llm_client
from tools import TOOLS, execute_tool

SYSTEM_PROMPT = """You are a helpful assistant for an LMS system. You have access to tools to query the backend.

Available tools:
- get_items: List all labs and tasks
- get_learners: List enrolled students
- get_scores: Score distribution for a lab
- get_pass_rates: Per-task scores and attempts
- get_timeline: Submissions per day
- get_groups: Per-group performance
- get_top_learners: Top students in a lab
- get_completion_rate: Completion percentage
- trigger_sync: Refresh data

When a user asks a question:
1. Decide which tool(s) to call
2. Call them one by one
3. Summarize the results in a helpful way

Be concise but informative. Use the data to answer questions about labs, scores, and student performance."""

def handle_intent(user_input: str) -> str:
    """Process natural language input using LLM with tools."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    tool_calls_log = []
    max_iter = 10

    for _ in range(max_iter):
        print(f"[debug] Calling LLM...", file=sys.stderr)
        msg = llm_client.chat(messages, tools=TOOLS)

        if not msg.tool_calls:
            # Final answer
            return msg.content or "I couldn't understand that."

        # Process tool calls
        for tool_call in msg.tool_calls:
            name = tool_call.function.name
            try:
                args = json.loads(tool_call.function.arguments)
                print(f"[tool] {name}({args})", file=sys.stderr)
                result = execute_tool(name, args)
                print(f"[tool] Result: {str(result)[:200]}...", file=sys.stderr)
            except Exception as e:
                result = f"Error: {str(e)}"
                print(f"[tool] Error: {result}", file=sys.stderr)

            tool_calls_log.append({
                "tool": name,
                "args": args,
                "result": result[:500]
            })

            # Add tool result to conversation
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

    return "I couldn't process that request. Please try again."
