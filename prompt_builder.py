def get_system_prompt(TOOL_REGISTRY):
    prompt = "You are an AI assistant that can use tools. You have access to conversation history and MUST use it to answer questions about previous conversations.\n"
    prompt += "You must output in the following format:\n\n"
    prompt += "Thought: ...\n"
    prompt += "Action: {\"name\": \"tool_name\", \"args\": {...}}\n\n"
    prompt += "When you have the final answer, output:\n"
    prompt += "Final Answer: ...\n\n"
    prompt += "Available tools:\n"
    prompt += "\n重要：你的每一次输出都必须严格以 'Thought:' 或 'Final Answer:' 开头，绝对不能直接回复普通对话。\n"
    for name in TOOL_REGISTRY:
        prompt += f"- {name}: {TOOL_REGISTRY[name].__doc__}\n"
    return prompt
    