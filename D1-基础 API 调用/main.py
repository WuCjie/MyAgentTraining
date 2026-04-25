# main.py - LLMClient 使用演示
from src.llm_client import LLMClient
import time

# 1. 初始化客户端
chatbot = LLMClient()
print("=" * 50)
print("🤖 LLMClient 使用演示")
print("=" * 50)

# 2. 多轮对话 - historyChat
print("\n📝 多轮对话")
res1 = chatbot.historyChat("以后叫我彭于晏")
print(f"用户：以后叫我彭于晏")
print(f"助手：{res1}")

res2 = chatbot.historyChat("我是谁？")
print(f"\n用户：我是谁？")
print(f"助手：{res2}")

res3 = chatbot.historyChat("今天天气怎么样？帮我简单说两句")
print(f"\n用户：今天天气怎么样？")
print(f"助手：{res3}")

print(f"\n📊 当前历史记录数：{len(chatbot.history)}")

# 3. 保存对话历史 - save_history
print("\n💾 保存对话历史")
filename = f"chat_history_{time.strftime('%Y%m%d_%H%M%S')}.json"
chatbot.save_history(filename)

# 4. 清空历史 - clear_history
print("\n🗑️ 清空对话历史")
chatbot.clear_history()
print(f"清空后历史记录数：{len(chatbot.history)}")

# 5. 加载历史 - load_history
print("\n📂 加载之前保存的对话")
chatbot.load_history(filename)
print(f"加载后历史记录数：{len(chatbot.history)}")
print(f"第一条消息：{chatbot.history[0]}")