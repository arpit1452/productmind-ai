from app.chains.agent_executor import create_agent
from app.memory.vector_store import save_memory, get_memory


def run_agent(idea: str) -> dict:
    """
    Runs the AI Product Manager agent on a given product idea.
    Returns a dict with 'output' (final plan) and 'steps' (intermediate tool calls).
    """

    # Create agent executor
    agent = create_agent()

    # Retrieve relevant past memory for context
    memory_context = get_memory(idea)

    # Build a clean, focused input — just the idea + memory
    # The agent prompt template handles all instructions
    if memory_context and memory_context.strip():
        full_input = f"""Product idea: {idea}

Relevant past context from memory:
{memory_context}"""
    else:
        full_input = f"Product idea: {idea}"

    # Run the agent
    try:
        result = agent.invoke({"input": full_input})
    except Exception as e:
        return {
            "output": f"Agent encountered an error: {str(e)}\n\nPlease try again with a more specific product idea.",
            "steps": [],
            "error": str(e)
        }

    # Extract final output
    final_output = result.get("output", "No output generated.")

    # Extract intermediate steps for transparency/debugging
    intermediate_steps = result.get("intermediate_steps", [])
    steps_summary = []
    for action, observation in intermediate_steps:
        steps_summary.append({
            "tool": action.tool,
            "input": action.tool_input,
            "output_preview": str(observation)[:300] + "..." if len(str(observation)) > 300 else str(observation)
        })

    if final_output == "Agent stopped due to iteration limit or time limit.":
        steps_text = "\n\n".join([
            f"### {s['tool']}\n{s['output_preview']}" 
            for s in steps_summary
        ])
        final_output = f"## Partial Results (agent timed out)\n\n{steps_text}"

    # Save final output to memory for future reference
    try:
        save_memory(final_output)
    except Exception:
        pass  # Memory saving is non-critical

    return {
        "output": final_output,
        "steps": steps_summary,
        "tools_used": [s["tool"] for s in steps_summary],
        "num_steps": len(steps_summary)
    }