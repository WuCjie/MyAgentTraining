# RAG（检索增强生成）学习笔记

## 概述

RAG = **R**etrieval + **A**ugmented + **G**eneration。核心思路：让 LLM 回答问题前先去资料库检索相关内容，再基于检索结果生成答案，从而减少幻觉、提高准确性。

## 六步流程

### 1. 文档加载（Document Loading）

把原始文档读入程序。LangChain 提供了多种 Loader（TextLoader、PDFLoader、WebBaseLoader 等），按文档格式选用。

- **要点**：关注编码格式（如 UTF-8），否则可能有乱码

### 2. 文本分割（Text Splitting）

把长文档切成小块（chunk），原因：
- Embedding 模型有 token 上限，超长文本无法编码
- 块太大会稀释语义，太小会丢失上下文

两个核心参数：
- **chunk_size**：每块大小。一般 256~1024，取决于模型和文档类型
- **chunk_overlap**：相邻块之间的重叠量，避免关键信息被切断

常用分割器：`RecursiveCharacterTextSplitter`，按句号/换行等分隔符逐级切分，尽量保持语义完整。

### 3. 向量化（Embedding）

把文本块转成固定维度的向量。语义相近的文本，向量距离也相近。

- 模型选择：中文场景可用 `Qwen3-Embedding`、`BGE` 等开源模型
- 使用 `SentenceTransformer` 一行加载，自动完成 tokenize → pooling → normalize
- 向量维度通常在 768~4096 之间，越高表达能力越强但存储和检索越慢

### 4. 向量存储（Vector Store）

将所有文本块的向量存入向量数据库，实现高效相似度搜索和持久化。

常用的轻量向量库：
| 工具 | 适用场景 |
|------|---------|
| Chroma | 学习/中小项目，API 简单 |
| FAISS | 大规模数据集，检索速度极快 |
| Milvus | 生产环境，分布式架构 |

**核心概念**：Collection（类似表），每条记录包含 id + document + embedding。

### 5. 检索（Retrieval）

用户提问时，把问题向量化后在库中搜索最相关的 Top-K 个文本块。

关键考虑：
- **Top-K**：通常 3~5，太小缺信息，太大引入噪声
- **检索策略**：
  - 语义检索：向量相似度，能理解同义词
  - 关键词检索（BM25）：精确匹配，适合专有名词
  - 混合检索：两者加权结合，生产环境推荐

### 6. 增强生成（Generation）

将检索到的文本块作为参考资料拼入 Prompt，交给 LLM 生成答案。

**Prompt 模板四要素**：
1. 角色设定 — 告诉 LLM 它是谁
2. 参考资料 — 检索结果（RAG 的核心价值）
3. 用户问题 — 原始提问
4. 约束条件 — "严格基于资料回答，不知道就说不知道"

这个约束是防幻觉的关键：不写这句话，LLM 可能忽略资料直接编造。

## 技术栈

- 文档处理：LangChain (`langchain_community`, `langchain_text_splitters`)
- Embedding：SentenceTransformer + Qwen3-Embedding-0.6B
- 向量数据库：Chroma
- LLM：OpenAI 兼容接口（ChatOpenAI）

## 文件结构

```
D4-RAG Q&A/
├── .env                              # 环境变量配置
├── .claude/
│   └── settings.local.json           # Claude 编辑器配置
├── chroma_db/                        # Chroma 向量数据库
│   ├── chroma.sqlite3                # SQLite 数据库文件
│   └── 66a7526b-2656-4a3b-b9c3-249c7ebb504e/  # Collection 数据
│       ├── data_level0.bin           # 向量数据
│       ├── header.bin                # 文件头
│       ├── length.bin                # 长度信息
│       └── link_lists.bin            # 链接列表
├── crossover_epic_saga.txt           # 示例文档：次元裂缝小说
├── D4-RAG Q&A.ipynb                  # 主要学习笔记和代码
├── README.md                         # 本文件
└── 使用本地嵌入模型和文本分割器.md   # 补充说明文档
```

## 运行

```bash
pip install langchain langchain-community langchain-text-splitters chromadb sentence-transformers langchain-openai
```

然后按 notebook 单元格顺序运行，确保 `.env` 中配好 `OPENAI_API_KEY` 和 `OPENAI_BASE_URL`。
