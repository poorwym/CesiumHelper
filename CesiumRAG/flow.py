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

def main():
    # 从配置文件加载配置
    config = load_config()
    
    # 初始化各节点
    api_query_node = APIQueryNode(node_id="api_query_node", config=config["llm"])
    embedding_node = EmbeddingNode(node_id="embedding_node", config=config["embedding"])
    vectordb_node = VectorDBNode(node_id="vectordb_node", config=config["vectordb"])
    retriever_node = RetrieverNode(node_id="retriever_node")
    llm_node = LLMNode(node_id="llm_node", config=config["llm"])
    output_node = OutputNode(node_id="output_node")

    # 构造输入
    input_data = {
        "user_query": "帮我寻找直接从构造函数构建CesiumTerrainProvider类实体的方法",
        "original_user_query": "帮我寻找直接从构造函数构建CesiumTerrainProvider类实体的方法"
    }

    # 按顺序执行
    data_after_api_query = api_query_node.process(input_data)
    print("API 描述:", data_after_api_query["api_description"])
    print("\n", "*"*100, "\n")
    data_after_embedding = embedding_node.process(data_after_api_query)
    # print("embedding:", data_after_embedding)
    data_after_vdb = vectordb_node.process(data_after_embedding)
    # print("vdb:", data_after_vdb)
    data_after_retriever = retriever_node.process(data_after_vdb)
    print("retriever:", data_after_retriever)
    print("\n", "*"*100, "\n")
    data_after_llm = llm_node.process(data_after_retriever)
    print("llm:", data_after_llm)
    print("\n", "*"*100, "\n")
    final_result = output_node.process(data_after_llm)

    print("\n最终回答:", final_result["final_output"])

if __name__ == "__main__":
    main()