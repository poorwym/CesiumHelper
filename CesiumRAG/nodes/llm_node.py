# nodes/llm_node.py

from .base_node import Node
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
# 例如 from langchain_openai import ChatOpenAI

class LLMNode(Node):
    def __init__(self, node_id: str, config: dict = None):
        super().__init__(node_id, config)
        
        # 从config读取GPT模型、API key等
        self.model_name = self.config.get("model_name", "gpt-4")
        self.api_key = self.config.get("openai_api_key", "")
        self.temperature = self.config.get("temperature", 0)
        self.base_url = self.config.get("base_url", "https://api.chatanywhere.tech/v1")
        
        # 从config读取prompt模板，如果没有则使用默认模板
        self.prompt_template = self.config.get("prompt_template", 
            """基于以下上下文回答用户问题：
            上下文:
            {context}

            问题:
            {original_user_query}
            """)
        
        # 初始化prompt模板
        self.prompt = PromptTemplate(
            template=self.prompt_template,
            input_variables=["context", "original_user_query"]
        )

        # 初始化ChatOpenAI
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.api_key,
            base_url=self.base_url
        )

    def process(self, data: dict) -> dict:
        """
        用context和original_user_query组合prompt，调用LLM生成回答
        """
        context = data.get("context", "")
        original_user_query = data.get("original_user_query", "")

        # 使用prompt模板生成完整prompt
        formatted_prompt = self.prompt.format(
            context=context,
            original_user_query=original_user_query
        )

        response = self.llm.invoke(formatted_prompt)
        
        # 确保response是字符串
        answer = response.content if hasattr(response, 'content') else str(response)

        return {
            "answer": answer
        }
    

