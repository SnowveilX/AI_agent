import tiktoken
import os
import logging

# 延迟加载 encoding，避免启动时失败
_ENCODING = None

def get_encoding():
    global _ENCODING
    if _ENCODING is None:
        encoding_name = os.getenv("ENCODING_NAME", "cl100k_base")
        try:
            _ENCODING = tiktoken.get_encoding(encoding_name)
        except Exception as e:
            raise RuntimeError(f"无法加载编码器 {encoding_name}: {e}")
    return _ENCODING

def num_tokens_from_messages(messages):
    encoding = get_encoding()
    tokens_per_message = 4
    tokens_per_name = 2

    num_tokens = 0
    for msg in messages:
        num_tokens += tokens_per_message
        for key, value in msg.items():
            if key == "role":
                continue
            if key == "content":
                # 确保 content 是字符串
                text = value if isinstance(value, str) else str(value)
                num_tokens += len(encoding.encode(text))
            elif key == "name":
                num_tokens += tokens_per_name
                if isinstance(value, str):
                    num_tokens += len(encoding.encode(value))
    num_tokens += 2
    return num_tokens

def trim_messages(messages, max_tokens):
    # 先检查是否已经满足
    if num_tokens_from_messages(messages) <= max_tokens:
        return messages.copy()
    
    # 分离系统消息和非系统消息
    system_msgs = [m for m in messages if m.get("role") == "system"]
    other_msgs = [m for m in messages if m.get("role") != "system"]
    
    # 从最早的非系统消息开始删除，直到 token 数达标
    while other_msgs and num_tokens_from_messages(system_msgs + other_msgs) > max_tokens:
        other_msgs.pop(0)   # 删除最旧的一条
    
    
    return system_msgs + other_msgs

def setup_logger():
    logger = logging.getLogger("AgentLogger")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger