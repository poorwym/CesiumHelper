# flow.py

import json
from nodes.embedding_node import EmbeddingNode
from nodes.vectordb_node import VectorDBNode
from nodes.retriever_node import RetrieverNode
from nodes.llm_node import LLMNode
from nodes.output_node import OutputNode
from nodes.api_query_node import APIQueryNode

def load_config():
    with open('config.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# 添加用于从GUI调用的函数
def process_query(query, config, status_callback=None, progress_callback=None):
    """
    处理用户查询并返回结果
    
    参数:
    query: 用户输入的查询
    config: 配置信息
    status_callback: 状态更新回调函数，接收状态文本
    progress_callback: 进度更新回调函数，接收进度百分比
    
    返回:
    final_output: 最终输出结果
    """
    # 更新状态
    if status_callback: status_callback("正在分析问题...")
    if progress_callback: progress_callback(10)
    
    # 初始化各节点
    api_query_node = APIQueryNode(node_id="api_query_node", config=config["llm"])
    embedding_node = EmbeddingNode(node_id="embedding_node", config=config["embedding"])
    vectordb_node = VectorDBNode(node_id="vectordb_node", config=config["vectordb"])
    retriever_node = RetrieverNode(node_id="retriever_node")
    llm_node = LLMNode(node_id="llm_node", config=config["llm"])
    output_node = OutputNode(node_id="output_node")

    # 构造输入
    input_data = {
        "context": "",
        "user_query": query,
        "original_user_query": query
    }

    # 按顺序执行
    if status_callback: status_callback("正在查询相关API...")
    if progress_callback: progress_callback(20)
    data_after_api_query = api_query_node.process(input_data)

    if status_callback: status_callback("正在生成嵌入向量...")
    if progress_callback: progress_callback(40)
    data_after_embedding = embedding_node.process(data_after_api_query)
    
    if status_callback: status_callback("正在向量数据库中检索相关文档...")
    if progress_callback: progress_callback(60)
    data_after_vdb = vectordb_node.process(data_after_embedding)
    
    if status_callback: status_callback("正在处理检索结果...")
    if progress_callback: progress_callback(70)
    data_after_retriever = retriever_node.process(data_after_vdb)
    
    if status_callback: status_callback("AI正在生成回答...")
    if progress_callback: progress_callback(80)
    data_after_llm = llm_node.process(data_after_retriever)
    
    if progress_callback: progress_callback(95)
    final_result = output_node.process(data_after_llm)
    
    if progress_callback: progress_callback(100)
    return final_result["final_output"]

def main():
    # 从配置文件加载配置
    config = load_config()
    
    query = str(input("请输入你的问题："))
    result = process_query(query, config)
    print(result)

if __name__ == "__main__":
    main()