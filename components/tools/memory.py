from components.vector_db import vector_memory

def get_long_term_context(query: str, k: int = 2) -> str:
    """Get long-term context for a given query from the vector database."""
    print(f"\n[Tool Call] get_long_term_context: {query}")
    memories = vector_memory.search(query, k)
    
    if not memories:
        return "No relevant past memories found."

    context = []
    for m in memories:
        context.append(
            f"User: {m['query']}\n"
            f"Answer: {m['final_answer']}\n"
            f"Tools: {m.get('meta', {}).get('tools_used', [])}"
        )
    return "\n---\n".join(context)
