import dotenv
from langchain_openai import ChatOpenAI
import os

dotenv.load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_BASE_URL"] = os.getenv("OPENAI_BASE_URL")
llm = ChatOpenAI(model="gpt-4o-mini")


class LLMClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        dotenv.load_dotenv()    #加载环境变量
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")   #优先使用传进来的参数作为key和url
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL")
        self.model = model or "gpt-4o-mini"
        self.llm = ChatOpenAI(
            model=self.model,
            api_key=self.api_key,        # 直接传参
            base_url=self.base_url       # 直接传参
        )
        self.history=[] #存储对话历史记录
    def chat(self,prompt,temperature=0.5):
        return self.llm.invoke(prompt,temperature).content

    def historyChat(self,prompt):
        self.history.append({"role": "user", "content": prompt})
        respose = self.llm.invoke(self.history).content
        self.history.append({"role": "assistant", "content": respose})
        return respose

chatbot = LLMClient()

res = chatbot.historyChat("后面的对话中称呼我为彭于晏")

res1 = chatbot.historyChat("我是谁")

print(res1)