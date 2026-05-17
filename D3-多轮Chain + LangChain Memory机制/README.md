# D3 - 多轮 Chain + LangChain Memory 机制学习总结

## 📚 学习目标
掌握 LangChain Expression Language (LCEL) 的使用，理解 Chain 的构建方式，以及如何实现多轮对话的 Memory 机制。

## 🛠️ 核心内容

### 1. LCEL（LangChain Expression Language）基础

LCEL 是一种声明式方法，通过 Python 原生操作符（如管道符 `|`）将组件连接成可执行流程。

**基本构成**：
```
Prompt + Model + OutputParser = Chain
```

**简单 Chain 示例**：
```python
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

prompt = PromptTemplate.from_template("给我讲一个关于{topic}的笑话")
parser = StrOutputParser()

chain = prompt | llm | parser
response = chain.invoke({"topic": "飞机"})
```

### 2. 顺序链（Sequential Chain）

将多个 Chain 顺序连接，形成 Pipeline：
- Chain A 的输出作为 Chain B 的输入
- 适用于需要多步骤处理的复杂任务

**实现方式**：
```python
full_chain = (
    {"dynasty": lambda x: x}
    | promptA
    | llm
    | parser
    | {"description": lambda x: x}  # 将 chainA 输出映射为 description
    | promptB
    | llm
    | parser
)
```

**实际应用**：
- Chain A：历史学家角色，详细介绍某个朝代
- Chain B：总结专家角色，提炼长文本的核心内容

### 3. Memory 机制实现

#### 方法：使用 RunnableWithMessageHistory

**核心组件**：
- `InMemoryChatMessageHistory`：内存中的对话历史存储
- `MessagesPlaceholder`：在 Prompt 中预留历史消息的位置
- `RunnableWithMessageHistory`：包装 Chain，自动管理历史

**实现步骤**：

1. **创建历史存储管理函数**：
```python
store = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]
```

2. **定义带历史占位符的 Prompt**：
```python
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名资深的中国历史学家..."),
    MessagesPlaceholder(variable_name="history"),  # 历史消息插入位置
    ("human", "{input}"),
])
```

3. **包装 Chain**：
```python
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)
```

4. **调用时指定 session_id**：
```python
response = chain_with_history.invoke(
    {"input": "讲讲明朝的历史"},
    config={"configurable": {"session_id": "user_123"}}
)
```

### 4. 版本变化说明

⚠️ **LangChain 0.3+ 版本变化**：
- 移除了旧的 `memory` 模块
- 推荐使用 `RunnableWithMessageHistory` 或自定义实现
- 可通过继承 `BaseChatMessageHistory` 实现更灵活的 Memory 需求

## 💡 关键收获

1. **LCEL 的优势**：
   - 代码简洁直观，使用管道符连接组件
   - 支持流式输出、并行执行、重试等高级特性
   - 易于调试和扩展

2. **Chain 的设计模式**：
   - 单一职责：每个 Chain 只做一件事
   - 数据流清晰：明确每个步骤的输入输出
   - 可组合性：小 Chain 可以组合成大 Chain

3. **Memory 的核心思想**：
   - 对话历史需要与业务逻辑分离
   - 通过 session_id 区分不同用户的对话
   - 历史存储可替换（内存、Redis、数据库等）

4. **实际应用场景**：
   - 客服机器人：需要记住用户之前的问题
   - 角色扮演：保持角色设定和对话连贯性
   - 多轮任务：如分步骤收集用户信息

## 📁 文件结构
```
D3-多轮Chain + LangChain Memory机制/
├── Chain&Memory.ipynb    # 主要学习笔记和代码
├── .env                  # 环境变量配置
└── README.md             # 本文件
```

## 🔧 使用的技术栈
- LangChain
- LangChain-OpenAI
- Python 3.x

## 📝 核心代码示例

### 完整 Memory Chain 实现
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

# 历史存储
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# Prompt 定义
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名资深的中国历史学家..."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# 基础 Chain
chain = prompt | llm

# 带历史的 Chain
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 使用
response = chain_with_history.invoke(
    {"input": "用户输入"},
    config={"configurable": {"session_id": "唯一标识"}}
)
```

## 🚀 进阶方向

1. **持久化存储**：将 `InMemoryChatMessageHistory` 替换为 Redis、数据库等
2. **历史摘要**：当历史过长时，使用 LLM 对历史进行摘要
3. **多模态 Memory**：支持图片、文件等的多轮对话

---

*学习日期：2026年5月*
