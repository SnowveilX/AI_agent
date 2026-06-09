import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
DEFAULT_TIMEOUT = int(os.getenv("TIMEOUT", 30))
DEFAULT_MAX_TOKENS = int(os.getenv("MAX_TURN_TOKENS", 2048))

def call_llm(messages, timeout=None, max_tokens=None, stream = True):
    """调用 LLM API，返回响应字符串"""
    timeout = timeout or DEFAULT_TIMEOUT
    max_tokens = max_tokens or DEFAULT_MAX_TOKENS

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": max_tokens,   # 或 max_completion_tokens，请根据 API 调整
        "stream": stream,
    }

    try:
        if stream:
            full_response = ""
            with requests.post(
                BASE_URL,
                headers=headers,
                json=payload,
                timeout=timeout,
                stream=True
            ) as response:
                response.raise_for_status()
                print("\n助手：", end="", flush=True)
                for line in response.iter_lines():
                    if not line:
                        continue
                    line = line.decode("utf-8")
                    if line.startswith("data:"):
                        data_str = line[5:].strip()
                        if data_str == "[DONE]":
                            break
                        try:
                            import json
                            data = json.loads(data_str)
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                print(content, end="", flush=True)
                                full_response += content
                        except Exception:
                            continue
                print()
            return full_response
        
        else:
            response = requests.post(
                BASE_URL,
                headers=headers,
                json=payload,
                timeout=timeout
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        raise Exception("LLM 请求超时")
    except requests.exceptions.RequestException as e:
        raise Exception(f"LLM 请求失败: {e}")
    except (KeyError, IndexError, ValueError) as e:
        raise Exception(f"LLM 响应解析失败: {e}")