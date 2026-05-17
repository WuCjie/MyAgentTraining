# D2 - 提示词工程学习总结

## 📚 学习目标
掌握 Prompt Engineering 的核心技巧，学会通过优化提示词来引导 LLM 产生更准确、更有用的输出。

## 🛠️ 核心内容

### 1. LLMClient 类封装
- 基于 LangChain 的 `ChatOpenAI` 封装了一个通用的 LLM 客户端
- 支持对话历史管理（`historyChat`）
- 支持历史记录的保存与加载（`save_history` / `load_history`）
- 自动限制历史记录长度（最多保留 20 条消息）

### 2. NLU（自然语言理解）实现
**任务**：识别用户对手机流量套餐的选择条件

**关键属性**：
- `name`：套餐名称（经济套餐、畅游套餐、无限套餐、校园套餐）
- `price`：月费价格（支持运算符：<=, >=, ==）
- `data`：月流量（支持数值或"无上限"）
- `sort`：排序方式（升序/降序）

### 3. 提示词技巧实践

#### ✅ Few-Shot 学习
- 通过提供示例让模型理解任务格式
- 使用 `FewShotChatMessagePromptTemplate` 构建示例模板
- 显著提升输出格式的一致性和准确性

#### ✅ 思维链（Chain of Thought, CoT）
- 在提示词中加入"请一步一步思考"
- 将复杂推理任务分解为多个中间步骤
- 适用于逻辑推理、数学问题等需要多步思考的场景

#### ✅ 输出格式限定
- 通过提示词明确要求 JSON 格式输出
- 定义详细的字段类型和取值范围
- 确保输出可被程序解析使用

## 💡 关键收获

1. **提示词设计原则**：
   - 任务描述要清晰具体
   - 提供足够的上下文和示例
   - 明确输出格式要求

2. **Few-Shot vs Zero-Shot**：
   - Few-Shot 在格式一致性上表现更好
   - 对于复杂任务，示例能显著降低模型的"猜测"成本

3. **CoT 的适用场景**：
   - 逻辑推理题
   - 多步骤数学计算
   - 需要解释思考过程的任务

## 📁 文件结构
```
D2-提示词工程/
├── promptEngineering.ipynb    # 主要学习笔记和代码
├── .env                       # 环境变量配置
└── README.md                  # 本文件
```

## 🔧 使用的技术栈
- LangChain
- LangChain-OpenAI
- Python 3.x

## 📝 示例代码片段

### Few-Shot Prompt 模板
```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples_list = [
    {"input": "便宜的套餐", "output": '{"sort":{"ordering":"ascend","value":"price"}}'},
    {"input": "有没有不限流量的", "output": '{"data":{"operator":"==","value":"无上限"}}'},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai", "{output}"),
])

few_shot_template = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples_list,
)
```

---

*学习日期：2026年4月-5月*
