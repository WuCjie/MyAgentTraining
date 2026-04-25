# D1 - 基础 API 调用

基于 LangChain 封装的 LLM 对话客户端，支持多轮对话、历史记录管理。

## 📦 功能特性

- 🔧 **API 封装**：支持自定义 API Key、Base URL、模型
- 💬 **多轮对话**：自动保留对话上下文
- 📜 **历史管理**：保存/加载/清空对话记录
- ✂️ **智能裁剪**：自动保留最近 10 轮对话（20条消息）
- 🔐 **环境变量**：使用 `.env` 文件管理敏感信息
- ⚠️ **错误处理**：初始化时检查配置有效性

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
```

### 3. 运行示例

```bash
python main.py
```

## 📁 项目结构

```
D1-基础 API 调用/
├── src/
│   ├── __init__.py          # 包入口
│   └── llm_client.py        # LLMClient 类实现
├── main.py                   # 使用示例入口
├── requirements.txt          # 依赖清单
├── .env.example              # 环境变量模板
└── README.md                 # 本文档
```

## 📖 API 文档

### 初始化

```python
from src.llm_client import LLMClient

# 方式1：使用 .env 配置
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
response = chatbot.historyChat("你好，请叫我彭于晏")
print(response)

# 继续对话，AI 记得上下文
response2 = chatbot.historyChat("还记得我是谁吗？")
print(response2)
```

**注意**：历史自动限制为最多 10 轮（20条消息），超出的会自动删除最早的对话。

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

## ⚠️ 注意事项

1. **API Key 安全**：使用 `.env` 文件管理，不要硬编码到代码中，且 `.env` 文件不要提交到 Git
2. **历史长度**：自动保留最近 10 轮对话，超出的会自动删除
3. **错误处理**：初始化时会检查 API Key 和 Base URL 是否为空

## 📝 学习要点

本项目涵盖以下知识点：

- Python 类封装与面向对象编程
- 类型注解（Type Hints）的使用
- 环境变量管理（python-dotenv）
- LangChain 基础使用
- JSON 文件读写
- Python 包结构（`__init__.py`）

## 🔄 更新日志

### 2025-04-25
- 完善代码结构，添加类型注解
- 分离类定义与使用示例
- 添加项目文档

### 2025-04-23
- 添加历史长度限制（10轮）
- 添加保存/加载对话功能
- 添加清空历史功能
- 添加初始化错误检查

### 2025-04-22
- 封装 LLMClient 类
- 实现基础多轮对话
- 支持环境变量配置

---

_本项目为 AI 应用开发岗培训第一周（D1）作业_ 🐔
