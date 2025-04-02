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
        default_prompt = """请基于以下上下文回答用户关于Cesium的问题：

                        上下文:
                        {context}

                        问题:
                        {original_user_query}

                        请使用Markdown格式来组织你的回答，包括：
                        1. 使用适当的标题层级(##, ###)
                        2. 使用代码块(```)展示代码示例
                        3. 使用列表和表格来组织信息
                        4. 对重要概念使用粗体或斜体
                        5. 使用适当的分隔符分隔不同部分

                        请确保你的回答清晰、准确且容易理解。如果上下文中没有足够信息，请明确指出。
                        """
        
        self.prompt_template = self.config.get("prompt_template", default_prompt)
        
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
    

