# flow.py

import os
import sys
# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nodes.embedding_node import EmbeddingNode
from nodes.vectordb_node import VectorDBNode
from nodes.retriever_node import RetrieverNode
from nodes.llm_node import LLMNode
from nodes.output_node import OutputNode
from nodes.api_query_node import APIQueryNode

from utils.config_loader import ConfigLoader

# 添加用于从GUI调用的函数
def process_query(query, status_callback=None, progress_callback=None):
    """
    处理用户查询并返回结果
    
    参数:
    query: 用户输入的查询
    status_callback: 状态更新回调函数，接收状态文本
    progress_callback: 进度更新回调函数，接收进度百分比
    
    返回:
    final_output: 最终输出结果
    """
    # 更新状态
    if status_callback: status_callback("正在分析问题...")
    if progress_callback: progress_callback(10)
    
    config = ConfigLoader()
    # 获取 LLM 模型名
    llm_model_name = config.get("llm.model")
    embedding_model_name = config.get("embedding.model")
    base_url = config.get("llm.base_url")
    prompt_template = config.get("llm.prompt_template")
    # 获取向量库存储路径（返回绝对路径）
    persist_dir = config.get_path("vectordb.persist_directory")
    # 获取 API key（环境变量自动解析）
    api_key = config.get("llm.openai_api_key")

    # 初始化各节点
    api_query_node = APIQueryNode(node_id="api_query_node", config={"model": llm_model_name, "base_url": base_url, "prompt_template": prompt_template, "api_key": api_key})
    embedding_node = EmbeddingNode(node_id="embedding_node", config={"model": embedding_model_name, "base_url": base_url, "api_key": api_key})
    vectordb_node = VectorDBNode(node_id="vectordb_node", config={"persist_directory": persist_dir, "base_url": base_url, "api_key": api_key})
    retriever_node = RetrieverNode(node_id="retriever_node")
    llm_node = LLMNode(node_id="llm_node", config={"model": llm_model_name, "base_url": base_url, "prompt_template": prompt_template, "api_key": api_key})
    output_node = OutputNode(node_id="output_node")

    # 构造输入
    input_data = {
        "context": "",
        "user_query": query,
    }

    original_user_query = query

    # 按顺序执行
    if status_callback: status_callback("正在查询相关API...")
    if progress_callback: progress_callback(20)
    data_after_api_query = api_query_node.process(input_data)

    if status_callback: status_callback("正在生成嵌入向量...")
    if progress_callback: progress_callback(40)
    api_description = data_after_api_query["api_description"]
    data_after_embedding = embedding_node.process({"api_description": api_description})
    
    if status_callback: status_callback("正在向量数据库中检索相关文档...")
    if progress_callback: progress_callback(60)
    embeddings = data_after_embedding["embeddings"]
    data_after_vdb = vectordb_node.process({"embeddings": embeddings})
    
    if status_callback: status_callback("正在处理检索结果...")
    if progress_callback: progress_callback(70)
    retrieved_docs = data_after_vdb["retrieved_docs"]
    data_after_retriever = retriever_node.process({"retrieved_docs": retrieved_docs})
    
    if status_callback: status_callback("AI正在生成回答...")
    if progress_callback: progress_callback(80)
    context = data_after_retriever["context"]
    data_after_llm = llm_node.process({"context": context, "user_query": original_user_query})
    
    if progress_callback: progress_callback(95)
    final_result = output_node.process({"input": data_after_llm["answer"]})
    
    if progress_callback: progress_callback(100)
    return final_result["final_output"]

def status_callback(status_text):
    """
    处理用户查询并返回结果，同时更新状态和进度
    
    参数:
    status_text: 状态文本
    """
    print(status_text)

def progress_callback(progress):
    """
    处理用户查询并返回结果，同时更新状态和进度
    
    参数:
    progress: 进度百分比
    """
    print(f"进度: {progress}%")


def main():
    query = str(input("请输入你的问题："))
    result = process_query(query, status_callback, progress_callback)
    print(result)

if __name__ == "__main__":
    main()