# Nodes 文档

本文档详细介绍了系统中各个节点的功能、输入和输出。

## 基础节点 (BaseNode)

所有节点的基类，定义了基本的节点接口。

### 输入
- `node_id`: 节点的唯一标识符
- `config`: 节点的配置字典（可选）

## LLM节点 (LLMNode)

用于调用大语言模型生成回答的节点。

### 配置参数
- `model_name`: 模型名称（默认：gpt-4）
- `openai_api_key`: OpenAI API密钥
- `temperature`: 温度参数（默认：0）
- `base_url`: API基础URL
- `prompt_template`: 自定义提示词模板（可选）

### Prompt模板
LLM节点支持自定义提示词模板，可以通过配置参数`prompt_template`来设置。模板中可以使用以下变量：
- `{context}`: 上下文信息
- `{user_query}`: 用户问题

默认模板如下：
```
基于以下上下文回答用户问题：
上下文:
{context}

问题:
{user_query}
```

### 输入
```python
{
    "context": "上下文信息",
    "user_query": "用户问题"
}
```

### 输出
```python
{
    "answer": "LLM生成的回答"
}
```

## API查询节点 (APIQueryNode)

用于分析用户查询中可能涉及的Cesium API的节点，继承自LLMNode。

### 配置参数
- 继承LLMNode的所有配置参数
- `prompt_template`: 专门用于API查询的提示词模板（有默认值）

### Prompt模板
默认模板如下：
```
请分析以下用户查询中可能涉及到的 Cesium API，并用简短的陈述句表达出来，不同api间用逗号间隔。
只关注 API 相关的部分，不需要其他解释。
如果查询中没有明确的 API 相关描述，请返回"无明确的 API 相关描述"。

用户查询:
{user_query}

请用陈述句表达:
```

### 输入
```python
{
    "user_query": "用户的原始查询"
}
```

### 输出
```python
{
    "api_description": "分析出的API描述",
    "original_user_query": "原始用户查询"
}
```

## Embedding节点 (EmbeddingNode)

用于将文本转换为向量表示的节点。

### 配置参数
- `model_name`: 模型名称（默认：text-embedding-ada-002）
- `openai_api_key`: OpenAI API密钥
- `base_url`: API基础URL

### 输入
```python
{
    "api_description": "需要转换为向量的API描述",
    "original_user_query": "原始用户查询"
}
```

### 输出
```python
{
    "embeddings": "API描述的向量表示列表",
    "original_user_query": "原始用户查询"
}
```

## 向量数据库节点 (VectorDBNode)

用于在向量数据库中检索相似文档的节点。

### 配置参数
- `persist_directory`: 向量数据库持久化目录（默认：./chroma_data）

### 输入
```python
{
    "embeddings": "查询向量列表",
    "original_user_query": "原始用户查询"
}
```

### 输出
```python
{
    "retrieved_docs": "检索到的文档列表",
    "original_user_query": "原始用户查询"
}
```

## 检索器节点 (RetrieverNode)

用于处理和格式化检索到的文档的节点。

### 输入
```python
{
    "retrieved_docs": "检索到的文档列表",
    "original_user_query": "原始用户查询"
}
```

### 输出
```python
{
    "context": "处理后的文档内容",
    "original_user_query": "原始用户查询"
}
```

## 输出节点 (OutputNode)

用于最终输出处理的节点。

### 输入
```python
{
    "answer": "LLM生成的回答"
}
```

### 输出
```python
{
    "final_output": "格式化后的最终输出"
}
```

## 节点流程示例

一个典型的查询流程如下：

1. 用户输入查询
2. APIQueryNode分析查询中涉及的Cesium API
3. EmbeddingNode将API描述转换为向量
4. VectorDBNode使用向量检索相关文档
5. RetrieverNode处理和格式化检索到的文档
6. LLMNode基于文档生成回答
7. OutputNode格式化并输出最终结果 