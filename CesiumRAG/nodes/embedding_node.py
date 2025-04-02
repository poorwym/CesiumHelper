# nodes/embedding_node.py

from .base_node import Node
from langchain_openai import OpenAIEmbeddings
# 这里的 embedding 相关引入，例如 from langchain_openai import OpenAIEmbeddings
# 或者你自己封装的embedding类

class EmbeddingNode(Node):
    def __init__(self, node_id: str, config: dict = None):
        """
        继承自BaseNode,初始化embedding相关。
        """
        super().__init__(node_id, config)
        # 在config中可能有 'model'、'openai_api_key' 等
        self.model_name = self.config.get("model_name", "text-embedding-ada-002")
        self.api_key = self.config.get("openai_api_key", "")
        self.base_url = self.config.get("base_url", "https://api.chatanywhere.tech/v1")
        
        # 初始化embedding模型
        self.embedding_model = OpenAIEmbeddings(
            model=self.model_name,
            openai_api_key=self.api_key,
            base_url=self.base_url
            # 其它可配置参数
        )

    def process(self, data: dict) -> dict:
        """
        1. 从data中读取文本
        2. 调用 embedding_model 获取向量
        3. 返回新的dict
        """
        api_description = data.get("api_description", "")
        original_user_query = data.get("original_user_query", "")
        user_query = data.get("user_query", "")
        
        # 处理AIMessage对象
        if hasattr(api_description, 'content'):
            api_description = api_description.content
        
        apis = api_description.split(",")
        embeddings = []
        for api in apis:
            embeddings.append(self.embedding_model.embed_query(api))
        
        return {
            "embeddings": embeddings,
            "original_user_query": original_user_query,
            "user_query": user_query
        }