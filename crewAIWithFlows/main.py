# 导入python标准库
import os
import uuid
import time
import json
import asyncio
import uvicorn
# 导入第三方库
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
# 导入本应用程序提供的方法
from flows import testFlow
from utils.myLLM import my_llm



# Agent所使用大模型类型 openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
LLM_TYPE = "openai"

# 设置OpenAI的大模型的参数  Task中设置输出为:output_json时，需要用到默认的大模型
os.environ["OPENAI_API_BASE"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-dvdCgdO3LSWYgqnMiJR5NqG0eLSTM69yjryjD6LuL3lWkvf3"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

# 谷歌搜索引擎
SERPER_API_KEY = "eb8f2749944a5e5fbcfeae072535f07844b5134e"

# 初始化LLM模型
llm = None

# API服务设置相关  根据自己的实际情况进行调整
PORT = 8012  # 服务访问的端口


# 定义Message类
class RequestMessage(BaseModel):
    role: str
    customer_domain: str
    project_description: str
class ResponseMessage(BaseModel):
    role: str
    content: str
# 定义ChatCompletionRequest类
class ChatCompletionRequest(BaseModel):
    messages: List[RequestMessage]
    stream: Optional[bool] = False
# 定义ChatCompletionResponseChoice类
class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ResponseMessage
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
    global LLM_TYPE, llm
    global SERPER_API_KEY
    try:
        print("正在初始化模型")
        # 设置google搜索引擎
        os.environ["SERPER_API_KEY"] = SERPER_API_KEY
        # 根据MODEL_TYPE选择初始化对应的模型,默认使用gpt大模型
        llm = my_llm(LLM_TYPE)
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
    if not llm:
        print("服务未初始化")
        raise HTTPException(status_code=500, detail="服务未初始化")
    try:
        # print(f"收到聊天完成请求: {request}")
        print(f"已经进入到请求中")
        customer_domain = request.messages[-1].customer_domain
        project_description = request.messages[-1].project_description
        print(f"接收到的信息customer_domain: {customer_domain},接收到的信息project_description: {project_description}")
        # 构造数据
        inputData = {"customer_domain": customer_domain, "project_description": project_description}
        # 运行flow
        result = await testFlow(llm, inputData).kickoff()
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
                        message=ResponseMessage(role="assistant", content=formatted_response),
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



