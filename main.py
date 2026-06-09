from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")
MODEL = os.getenv("MODEL")
MAX_STEPS = int(os.getenv("MAX_STEPS", 10))
MAX_CONTEXT_TOKENS = int(os.getenv("MAX_CONTEXT_TOKENS", 64000))
MAX_TURN_TOKENS = int(os.getenv("MAX_TURN_TOKENS", 2048))
TIMEOUT = int(os.getenv("TIMEOUT", 30))

from llm_client import call_llm
from prompt_builder import get_system_prompt
from parser import parse_action
from tools import TOOL_REGISTRY
from utils import num_tokens_from_messages,setup_logger, trim_messages

logger = setup_logger()



def main():
    system_prompt = get_system_prompt(TOOL_REGISTRY)
    messages = [{"role": "system", "content": system_prompt}]
    num_tokens = num_tokens_from_messages(messages) 
    while True:
        messages_in_one_turn = messages.copy() 
        input_text = input("\n请输入您的问题（或输入 'exit' 退出）：")
        if input_text.lower() == "exit":
            print("退出程序。")
            break
        messages_in_one_turn.append({"role": "user", "content": input_text})
        for step in range(MAX_STEPS):
            logger.info(f"Step {step+1}/{MAX_STEPS}")
        
            # 调用LLM
            response = call_llm(messages_in_one_turn, timeout=TIMEOUT, max_tokens=MAX_TURN_TOKENS)
            messages_in_one_turn.append({"role": "assistant", "content": response})
        
            logger.info(f"LLM Response: {response}")
        
            # 解析LLM输出
            action_name, action_args = parse_action(response)
         
            if action_name is None:
                logger.warning("LLM 输出格式错误，要求重新输出")
                messages_in_one_turn.append({"role": "user", "content": "请严格按照格式输出 Action 或 Final Answer。"})
                continue   # 重新调用 LLM

            if action_name == "final_answer":
                final_answer = action_args["answer"]
                logger.info(f"Final Answer: {final_answer}")
                print(f"\n助手最终答案：{final_answer}")
                messages = messages_in_one_turn.copy()   # 保存完整对话历史
                break

            if action_name in TOOL_REGISTRY:
                tool_func = TOOL_REGISTRY[action_name]
                tool_result = tool_func(**action_args)
                messages_in_one_turn.append({"role": "tool", "content": f"{action_name} result: {tool_result}"})
                logger.info(f"Executed {action_name} with args {action_args}, got result: {tool_result}")
            else:
                logger.warning(f"Unknown action: {action_name}")        
            # 修剪消息以适应上下文限制
            messages = trim_messages(messages_in_one_turn, MAX_CONTEXT_TOKENS)

        

if __name__ == "__main__":
  main()    
