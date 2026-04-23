# LLM Client - AI对话客户端

基于LangChain封装的LLM对话客户端，支持多轮对话、历史记录管理。

## 📦 功能特性

- ✅ API封装：支持自定义API Key、Base URL、模型
- ✅ 多轮对话：自动保留对话上下文
- ✅ 历史管理：保存/加载/清空对话记录
- ✅ 智能裁剪：自动保留最近10轮对话
- ✅ 环境变量：使用.env文件管理敏感信息
- ✅ 错误处理：初始化时检查配置有效性

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install langchain-openai python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. 基础使用

```python
from llm_client import LLMClient

# 创建客户端（自动读取.env配置）
chatbot = LLMClient()

# 多轮对话
response1 = chatbot.historyChat("你好，请叫我彭于晏")
print(response1)

response2 = chatbot.historyChat("还记得我是谁吗？")
print(response2)
```

## 📖 API文档

### 初始化

```python
# 方式1：使用.env配置
chatbot = LLMClient()

# 方式2：自定义参数
chatbot = LLMClient(
    api_key="your_key",
    base_url="https://api.xxx.com/v1",
    model="gpt-4o-mini"
)
```

### 多轮对话

```python
# 发送消息，自动保留历史
response = chatbot.historyChat("你的消息")

# 历史自动限制：最多保留10轮（20条消息）
```

### 历史管理

```python
# 清空对话历史
chatbot.clear_history()

# 保存对话到文件（自动生成文件名）
chatbot.save_history()
# 或指定文件名
chatbot.save_history("my_chat.json")

# 从文件加载对话
chatbot.load_history("history_20250424_012345.json")
```

## 📁 文件结构

```
.
├── llm_client.py      # 主程序
├── .env               # 环境变量（不提交到git）
├── history_*.json     # 保存的对话记录
└── README.md          # 本文档
```

## ⚠️ 注意事项

1. **API Key安全**：使用`.env`文件管理，不要硬编码到代码中
2. **历史长度**：自动保留最近10轮，超出的会自动删除
3. **错误处理**：初始化时会检查API Key和Base URL是否为空

## 📝 更新日志

### 2025-04-24 (Day3)
- 添加历史长度限制（10轮）
- 添加保存/加载对话功能
- 添加清空历史功能
- 添加初始化错误检查

### 2025-04-23 (Day2)
- 封装LLMClient类
- 实现基础多轮对话
- 支持环境变量配置
