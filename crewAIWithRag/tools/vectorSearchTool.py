# 引入相关库
from crewai_tools import tool
import logging
from openai import OpenAI
import chromadb
import uuid
import numpy as np


# 设置日志模版
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 模型设置相关  根据自己的实际情况进行调整
API_TYPE = "openai"  # openai:调用gpt模型；oneapi:调用oneapi方案支持的模型(这里调用通义千问)
# openai模型相关配置 根据自己的实际情况进行调整
OPENAI_API_BASE = "https://api.wlai.vip/v1"
OPENAI_EMBEDDING_API_KEY = "sk-YgieAyjrhxwWFmn423FbB8A1C3B94f378d3b67467b32F6E7"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
# oneapi相关配置(通义千问为例) 根据自己的实际情况进行调整
ONEAPI_API_BASE = "http://139.224.72.218:3000/v1"
ONEAPI_EMBEDDING_API_KEY = "sk-DoU00d1PaOMCFrSh68196328E08e443a8886E95761D7F4Bf"
ONEAPI_EMBEDDING_MODEL = "text-embedding-v1"
# 指定向量数据库chromaDB的存储位置和集合 根据自己的实际情况进行调整
CHROMADB_DIRECTORY = "/Users/janetjiang/Desktop/agi_code/CrewAITest/crewAIWithRag/unitTest/vectorSaveTest/chromaDB"  # chromaDB向量数据库的持久化路径
# CHROMADB_DIRECTORY = "../unitTest/vectorSaveTest/chromaDB"  # chromaDB向量数据库的持久化路径
CHROMADB_COLLECTION_NAME = "demo001"  # 待查询的chromaDB向量数据库的集合名称


# get_embeddings方法计算向量
def get_embeddings(texts):
    global API_TYPE, ONEAPI_API_BASE, ONEAPI_EMBEDDING_API_KEY, ONEAPI_EMBEDDING_MODEL, OPENAI_API_BASE, OPENAI_EMBEDDING_API_KEY, ONEAPI_EMBEDDING_MODEL
    if API_TYPE == 'oneapi':
        try:
            # 初始化非OpenAI的Embedding模型,这里使用的是oneapi方案
            client = OpenAI(
                base_url=ONEAPI_API_BASE,
                api_key=ONEAPI_EMBEDDING_API_KEY
            )
            data = client.embeddings.create(input=texts, model=ONEAPI_EMBEDDING_MODEL).data
            return [x.embedding for x in data]
        except Exception as e:
            logger.info(f"生成向量时出错: {e}")
            return []

    elif API_TYPE == 'openai':
        try:
            # 初始化OpenAI的Embedding模型
            client = OpenAI(
                base_url=OPENAI_API_BASE,
                api_key=OPENAI_EMBEDDING_API_KEY
            )
            data = client.embeddings.create(input=texts, model=OPENAI_EMBEDDING_MODEL).data
            return [x.embedding for x in data]
        except Exception as e:
            logger.info(f"生成向量时出错: {e}")
            return []


# 对文本按批次进行向量计算
def generate_vectors(data, max_batch_size=25):
    results = []
    for i in range(0, len(data), max_batch_size):
        batch = data[i:i + max_batch_size]
        # 调用向量生成get_embeddings方法  根据调用的API不同进行选择
        response = get_embeddings(batch)
        results.extend(response)
    return results


# 封装向量数据库chromadb类，提供两种方法
class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        # 申明使用全局变量
        global CHROMADB_DIRECTORY
        # 实例化一个chromadb对象
        # 设置一个文件夹进行向量数据库的持久化存储  路径为当前文件夹下chromaDB文件夹
        chroma_client = chromadb.PersistentClient(path=CHROMADB_DIRECTORY)
        # 创建一个collection数据集合
        # get_or_create_collection()获取一个现有的向量集合，如果该集合不存在，则创建一个新的集合
        self.collection = chroma_client.get_or_create_collection(
            name=collection_name)
        # embedding处理函数
        self.embedding_fn = embedding_fn

    # 检索向量数据库，返回包含查询结果的对象或列表，这些结果包括最相似的向量及其相关信息
    # query：查询文本
    # top_n：返回与查询向量最相似的前 n 个向量
    def search(self, query, top_n):
        try:
            results = self.collection.query(
                # 计算查询文本的向量，然后将查询文本生成的向量在向量数据库中进行相似度检索
                query_embeddings=self.embedding_fn([query]),
                n_results=top_n
            )
            return results
        except Exception as e:
            logger.info(f"检索向量数据库时出错: {e}")
            return []


# 封装从向量数据库中查询内容方法  提供外部调用
@tool("vectorSearch")
def vectorSearch(user_query: str) -> str:
    """
	使用这个工具来完成根据用户的问题，从健康档案库中检索相关的内容。
	:param user_query: 用户的问题
	:return: 保存状态消息
	"""
    global CHROMADB_COLLECTION_NAME
    vector_db = MyVectorDBConnector(CHROMADB_COLLECTION_NAME, generate_vectors)
    # 封装检索接口进行检索测试
    # 将检索出的5个近似的结果
    full_text = ''
    search_results = vector_db.search(user_query, 2)
    # logger.info(f"检索向量数据库的结果: {search_results['documents'][0]}")
    for doc in search_results['documents'][0]:
        full_text = full_text+doc
    # logger.info(f"full_text结果: {full_text}")

    return f"检索到的 {user_query} 的结果是: {full_text}"



