# main.py - LLMClient 使用演示
from src.llm_client import LLMClient
import time

# 1. 初始化客户端
chatbot = LLMClient()
print("=" * 50)
print("🤖 LLMClient 使用演示")
print("=" * 50)



# 2. 多轮对话 - historyChat
print("\n📝 databricks")
res1 = chatbot.historyChat("databricks里面，创建视图a后，用户登出两天后，这个视图a还存在吗，select的到吗")
print(f"助手：{res1}")