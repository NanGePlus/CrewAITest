# 导入依赖包
import os
import sys
import re
import uuid
import time
import json
import asyncio
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
import uvicorn
from langchain_openai import ChatOpenAI
from crew import CrewtestprojectCrew



# 模型全局参数配置  根据自己的实际情况进行调整
# openai模型相关配置 根据自己的实际情况进行调整
OPENAI_API_BASE = "https://api.wlai.vip/v1"
OPENAI_CHAT_API_KEY = "sk-CU5Dncdg7OebzZm4Fa532b1cBf134447A93fE109Bd2d1b19"
OPENAI_CHAT_MODEL = "gpt-4o-mini"
# 非gpt大模型相关配置(oneapi方案 通义千问为例) 根据自己的实际情况进行调整
ONEAPI_API_BASE = "http://139.224.72.218:3000/v1"
ONEAPI_CHAT_API_KEY = "sk-0FxX9ncd0yXjTQF877Cc9dB6B2F44aD08d62805715821b85"
ONEAPI_CHAT_MODEL = "qwen-max"
# 本地大模型相关配置(Ollama方案 llama3.1:latest为例) 根据自己的实际情况进行调整
OLLAMA_API_BASE = "http://localhost:11434/v1"
OLLAMA_CHAT_API_KEY = "ollama"
OLLAMA_CHAT_MODEL = "llama3.1:latest"


# 初始化LLM模型
model = None
# API服务设置相关  根据自己的实际情况进行调整
PORT = 8012  # 服务访问的端口
# openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
MODEL_TYPE = "openai"



# 定义Message类
class Message(BaseModel):
    role: str
    content: str
# 定义ChatCompletionRequest类
class ChatCompletionRequest(BaseModel):
    messages: List[Message]
    stream: Optional[bool] = False
# 定义ChatCompletionResponseChoice类
class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: Message
    finish_reason: Optional[str] = None
# 定义ChatCompletionResponse类
class ChatCompletionResponse(BaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{uuid.uuid4().hex}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    choices: List[ChatCompletionResponseChoice]
    system_fingerprint: Optional[str] = None


# 定义了一个异步函数lifespan，它接收一个FastAPI应用实例app作为参数。这个函数将管理应用的生命周期，包括启动和关闭时的操作
# 函数在应用启动时执行一些初始化操作
# 函数在应用关闭时执行一些清理操作
# @asynccontextmanager 装饰器用于创建一个异步上下文管理器，它允许在yield之前和之后执行特定的代码块，分别表示启动和关闭时的操作
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    # 申明引用全局变量，在函数中被初始化，并在整个应用中使用
    global MODEL_TYPE, model
    global ONEAPI_API_BASE, ONEAPI_CHAT_API_KEY, ONEAPI_CHAT_MODEL
    global OPENAI_API_BASE, OPENAI_CHAT_API_KEY, OPENAI_CHAT_MODEL
    global OLLAMA_API_BASE, OLLAMA_CHAT_API_KEY, OLLAMA_CHAT_MODEL
    # 根据自己实际情况选择调用model和embedding模型类型
    try:
        print("正在初始化模型")
        # 根据MODEL_TYPE选择初始化对应的模型,默认使用gpt大模型
        if MODEL_TYPE == "oneapi":
            # 实例化一个oneapi客户端对象
            model = ChatOpenAI(
                base_url=ONEAPI_API_BASE,
                api_key=ONEAPI_CHAT_API_KEY,
                model=ONEAPI_CHAT_MODEL,  # 本次使用的模型
                # temperature=0,# 发散的程度，一般为0
                # timeout=None,# 服务请求超时
                # max_retries=2,# 失败重试最大次数
            )
        elif MODEL_TYPE == "ollama":
            # 实例化一个ChatOpenAI客户端对象
            model = ChatOpenAI(
                base_url=OLLAMA_API_BASE,# 请求的API服务地址
                api_key=OLLAMA_CHAT_API_KEY,# API Key
                model=OLLAMA_CHAT_MODEL,# 本次使用的模型
                # temperature=0,# 发散的程度，一般为0
                # timeout=None,# 服务请求超时
                # max_retries=2,# 失败重试最大次数
            )
        else:
            # 实例化一个ChatOpenAI客户端对象
            model = ChatOpenAI(
                base_url=OPENAI_API_BASE,# 请求的API服务地址
                api_key=OPENAI_CHAT_API_KEY,# API Key
                model=OPENAI_CHAT_MODEL,# 本次使用的模型
                # temperature=0,# 发散的程度，一般为0
                # timeout=None,# 服务请求超时
                # max_retries=2,# 失败重试最大次数
            )

        print("LLM初始化完成")

    except Exception as e:
        print(f"初始化过程中出错: {str(e)}")
        # raise 关键字重新抛出异常，以确保程序不会在错误状态下继续运行
        raise

    # yield 关键字将控制权交还给FastAPI框架，使应用开始运行
    # 分隔了启动和关闭的逻辑。在yield 之前的代码在应用启动时运行，yield 之后的代码在应用关闭时运行
    yield
    # 关闭时执行
    print("正在关闭...")


# lifespan 参数用于在应用程序生命周期的开始和结束时执行一些初始化或清理工作
app = FastAPI(lifespan=lifespan)


# POST请求接口，与大模型进行知识问答
@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    if not model:
        print("服务未初始化")
        raise HTTPException(status_code=500, detail="服务未初始化")
    try:
        # print(f"收到聊天完成请求: {request}")
        query_prompt = request.messages[-1].content
        print(f"用户问题是: {query_prompt}")
        # 执行crew
        inputs = {
            "topic": query_prompt
        }
        # 传入model，指定crew中的Agent使用什么大模型
        result = CrewtestprojectCrew(model).crew().kickoff(inputs=inputs)
        # 将返回的数据转成string类型
        formatted_response = str(result)
        print(f"LLM最终回复结果: {formatted_response}")

        # 处理流式响应
        if request.stream:
            # 定义一个异步生成器函数，用于生成流式数据
            async def generate_stream():
                # 为每个流式数据片段生成一个唯一的chunk_id
                chunk_id = f"chatcmpl-{uuid.uuid4().hex}"
                # 将格式化后的响应按行分割
                lines = formatted_response.split('\n')
                # 历每一行，并构建响应片段
                for i, line in enumerate(lines):
                    # 创建一个字典，表示流式数据的一个片段
                    chunk = {
                        "id": chunk_id,
                        "object": "chat.completion.chunk",
                        "created": int(time.time()),
                        # "model": request.model,
                        "choices": [
                            {
                                "index": 0,
                                "delta": {"content": line + '\n'}, # if i > 0 else {"role": "assistant", "content": ""},
                                "finish_reason": None
                            }
                        ]
                    }
                    # 将片段转换为JSON格式并生成
                    yield f"{json.dumps(chunk)}\n"
                    # 每次生成数据后，异步等待0.5秒
                    await asyncio.sleep(0.5)
                # 生成最后一个片段，表示流式响应的结束
                final_chunk = {
                    "id": chunk_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "choices": [
                        {
                            "index": 0,
                            "delta": {},
                            "finish_reason": "stop"
                        }
                    ]
                }
                yield f"{json.dumps(final_chunk)}\n"

            # 返回fastapi.responses中StreamingResponse对象，流式传输数据
            # media_type设置为text/event-stream以符合SSE(Server-SentEvents) 格式
            return StreamingResponse(generate_stream(), media_type="text/event-stream")
        # 处理非流式响应处理
        else:
            response = ChatCompletionResponse(
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=Message(role="assistant", content=formatted_response),
                        finish_reason="stop"
                    )
                ]
            )
            # print(f"发送响应内容: \n{response}")
            # 返回fastapi.responses中JSONResponse对象
            # model_dump()方法通常用于将Pydantic模型实例的内容转换为一个标准的Python字典，以便进行序列化
            return JSONResponse(content=response.model_dump())

    except Exception as e:
        print(f"处理聊天完成时出错:\n\n {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    print(f"在端口 {PORT} 上启动服务器")
    # uvicorn是一个用于运行ASGI应用的轻量级、超快速的ASGI服务器实现
    # 用于部署基于FastAPI框架的异步PythonWeb应用程序
    uvicorn.run(app, host="0.0.0.0", port=PORT)



