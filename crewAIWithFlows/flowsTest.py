# 导入python标准库
import os
import asyncio
# 导入第三方库
from crewai.flow.flow import Flow, listen, start
from crews.marketAnalystCrew.marketAnalystCrew import marketAnalystCrew
from crews.contentCreatorCrew.contentCreatorCrew import contentCreatorCrew
from utils.myLLM import my_llm


# Agent所使用大模型类型 openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
LLM_TYPE = "openai"

# 设置OpenAI的大模型的参数  Task中设置输出为:output_json时，需要用到默认的大模型
os.environ["OPENAI_API_BASE"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-dvdCgdO3LSWYgqnMiJR5NqG0eLSTM69yjryjD6LuL3lWkvf3"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

# 谷歌搜索引擎
SERPER_API_KEY = "eb8f2749944a5e5fbcfeae072535f07844b5134e"


class testFlow(Flow):

    def __init__(self, model, inputData):
        super().__init__()
        self.model = model
        self.inputData = inputData

    @start()
    def marketAnalystCrew(self):
        result = marketAnalystCrew(self.model).crew().kickoff(inputs=self.inputData)
        print("marketAnalystCrew result:", result)
        return result
    @listen(marketAnalystCrew)
    def contentCreatorCrew(self):
        result = contentCreatorCrew(self.model).crew().kickoff(inputs=self.inputData)
        print("contentCreatorCrew result:", result)
        return result



if __name__ == "__main__":
    customer_domain = 'https://www.emqx.com/zh'
    project_description = """
    EMQX 是一种开源的分布式消息中间件，专注于处理物联网 (IoT) 场景下的大规模消息通信。它基于MQTT协议，能够实现高并发、低延迟的实时消息推送，支持设备之间、设备与服务器之间的双向通信。
    客户领域： 分布式消息中间件解决方案
    项目概述： 创建一个全面的营销活动，以提高企业客户对 EMQX 服务的认识和采用。
    """
    inputData = {"customer_domain": customer_domain,"project_description": project_description}

    async def runFlow(inputData):
        result = await testFlow(my_llm(LLM_TYPE),inputData).kickoff()
        print("fianl result:", result)

    # 在异步环境中运行
    asyncio.run(runFlow(inputData))
