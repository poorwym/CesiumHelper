import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredPDFLoader, UnstructuredWordDocumentLoader, UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
import openai

# 加载环境变量
load_dotenv()

# 设置 OpenAI API 密钥和基础 URL
openai.base_url = "https://api.chatanywhere.tech/v1"

# 1. 加载文件夹中的所有文档
def load_documents_from_folder(folder_path):
    print(f"开始扫描目录: {folder_path}")
    loaders = [
        DirectoryLoader(folder_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True),
        DirectoryLoader(folder_path, glob="**/*.pdf", loader_cls=UnstructuredPDFLoader, show_progress=True),
        DirectoryLoader(folder_path, glob="**/*.docx", loader_cls=UnstructuredWordDocumentLoader, show_progress=True),
        DirectoryLoader(folder_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader, show_progress=True),
    ]
    all_docs = []
    for loader in loaders:
        try:
            docs = loader.load()
            print(f"使用 {loader.__class__.__name__} 加载了 {len(docs)} 篇文档")
            all_docs.extend(docs)
        except Exception as e:
            print(f"使用 {loader.__class__.__name__} 加载文档时出错: {str(e)}")
    return all_docs

# 2. 分割文档
def split_documents(docs, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_documents(docs)

# 3. 构建 embedding 并持久化
def build_vectorstore(docs, persist_path="./chroma_db"):
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        base_url="https://api.chatanywhere.tech/v1",
        api_key=os.getenv("OPENAI_API_KEY")
    )
    vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_path)
    vectordb.persist()
    return vectordb

# === 主流程 ===
folder_path = "./curated"  # 替换为你自己的文档文件夹路径
persist_path = "./chroma_openai"

print("加载文件...")
raw_docs = load_documents_from_folder(folder_path)

print(f"共加载 {len(raw_docs)} 篇文档，开始切分...")
split_docs = split_documents(raw_docs)

print(f"共切分为 {len(split_docs)} 段，开始构建向量库并持久化...")
build_vectorstore(split_docs, persist_path)

print("构建完毕，向量数据库已持久化。")