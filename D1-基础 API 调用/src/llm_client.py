import dotenv
from langchain_openai import ChatOpenAI
from datetime import datetime
import os
import json

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")

class LLMClient:
    def __init__(self, api_key: str | None = None, base_url: str | None = None, model: str | None = None) -> None:
        dotenv.load_dotenv()    #加载环境变量

        self.api_key = api_key or os.getenv("OPENAI_API_KEY")   #优先使用传进来的参数作为key和url
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")

        if not self.api_key:
            raise ValueError("API Key 不能为空！请检查：1) .env文件 2) 环境变量")
        if not self.base_url:
            raise ValueError("Base URL 不能为空！请检查 .env 文件")

        self.model = model or "gpt-4o-mini"

        try:
            self.llm = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                base_url=self.base_url
            )
        except Exception as e:
            raise RuntimeError(f"初始化 LLM 失败：{e}")

        self.history: list[dict[str, str]] = [] #存储对话历史记录

    def historyChat(self, prompt: str) -> str:
        self.history.append({"role": "user", "content": prompt})
        max_history = 20
        while len(self.history) > max_history:
            self.history.pop(0) #弹出用户的
            self.history.pop(0) #弹出ai的，如果加了系统提示词，得从1开始弹出
        respose = self.llm.invoke(self.history).content
        self.history.append({"role": "assistant", "content": respose})
        return respose

    def clear_history(self) -> None:
        self.history = []
        return

    def save_history(self, filepath: str | None = None) -> None:
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"history_{timestamp}.json"

        data = {
            "save_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": self.model,
            "message_count": len(self.history),
            "messages": self.history
        }

        # 写入文件
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"对话已保存到：{filepath}")
        return

    def load_history(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            print(f"文件不存在：{filepath}")
            return False

        # 读取JSON文件
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        # 恢复历史记录
        self.history = data.get("messages", [])
        return