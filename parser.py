def parse_action(response):

    import re, json
    
    final_answer_pattern = r"Final Answer:\s*(.*)"
    final_answer_match = re.search(final_answer_pattern, response, re.DOTALL)
    if final_answer_match:
        final_answer = final_answer_match.group(1).strip()    
        return "final_answer", {"answer": final_answer}
    action_pattern = r"Action:\s*(\{.*?\})(?=\n|$)"
    match = re.search(action_pattern, response, re.DOTALL)
    if not match:
        return None, None

    try:
        raw = match.group(1).strip()
        while raw.endswith("}}"):
            try:
                json.loads(raw)
                break
            except json.JSONDecodeError:
                raw = raw[:-1]
        action_data = json.loads(raw)
    except json.JSONDecodeError:
        return None, None
        
    action_name = action_data.get("name")
    args_args = action_data.get("args", {})

    return action_name, args_args
    