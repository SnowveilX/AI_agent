def get_system_prompt(TOOL_REGISTRY):
    prompt = "You are an AI assistant that can use tools.\n"
    prompt += "You must output in the following format:\n\n"
    prompt += "Thought: ...\n"
    prompt += "Action: {\"name\": \"tool_name\", \"args\": {...}}\n\n"
    prompt += "When you have the final answer, output:\n"
    prompt += "Final Answer: ...\n\n"
    prompt += "Available tools:\n"
    for name in TOOL_REGISTRY:
        prompt += f"- {name}: {TOOL_REGISTRY[name].__doc__}\n"
    return prompt