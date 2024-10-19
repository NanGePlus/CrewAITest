# 核心功能:在CrewAI中定义Agent和Task，并通过Crew来管理这些Agent和Task的执行流程

# 导入python标准库
import asyncio
import os
# 导入第三方库
from crewai import Agent, Crew, Process, Task, Pipeline
from crewai.project import CrewBase, agent, crew, task, pipeline
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field
# 导入本应用程序提供的方法
from utils.myLLM import my_llm
from utils.models import MarketStrategy, CampaignIdea, Copy

# 设置OpenAI的大模型的参数  Task中设置输出为:output_json时，需要用到默认的大模型
os.environ["OPENAI_API_BASE"] = "https://api.wlai.vip/v1"
os.environ["OPENAI_API_KEY"] = "sk-Fk4R8G56aHVTjlvhf0KeRJrVaBRweTSGVne00mcvwp9jM3fP"
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"

# 设置SERPER_API_KEY环境变量，用于Google搜索引擎的API
os.environ["SERPER_API_KEY"] = "88dc7e3ad5a6547d8b1e753a7e4095e7d47ef345"

# Agent所使用大模型类型 openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
LLM_TYPE = "openai"



# 定义了一个CrewtestprojectCrew类并应用了@CrewBase装饰器初始化项目
# 这个类代表一个完整的CrewAI项目
@CrewBase
class CrewtestprojectCrew():
	# agents_config和tasks_config分别指向agent和task的配置文件，存放在config目录下
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	def __init__(self, model):
		# Agent使用的大模型
		self.model = model

	# 通过@agent装饰器定义一个函数researcher，返回一个Agent实例
	# 该代理读取agents_config中的researcher配置
	# 参数verbose=True用于输出调试信息
	# 参数tools=[MyCustomTool()] 可以加载自定义工具
	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			verbose=True,
			llm=self.model,
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
		)

	@agent
	def chief_marketing_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['chief_marketing_strategist'],
			verbose=True,
			llm=self.model,
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
		)

	@agent
	def creative_content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['creative_content_creator'],
			verbose=True,
			llm=self.model
		)


	# 通过@task装饰器定义research_task，返回一个Task实例
	# 配置文件为tasks.yaml中的research_task部分
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def project_understanding_task(self) -> Task:
		return Task(
			config=self.tasks_config['project_understanding_task'],

		)

	@task
	def marketing_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['marketing_strategy_task'],
			output_json=MarketStrategy
		)

	@task
	def campaign_idea_task(self) -> Task:
		return Task(
			config=self.tasks_config['campaign_idea_task'],
			output_json=CampaignIdea

		)

	@task
	def copy_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['copy_creation_task'],
			context=[self.marketing_strategy_task(), self.campaign_idea_task()],
			output_json=Copy
		)


	# Crew类将agent和task组合成一个执行队列，并根据指定的执行流程进行任务调度
	# 通过@crew装饰器定义crew，创建一个Crew实例
	# agents=self.agents和tasks=self.tasks分别自动获取@agent和@task装饰器生成的agent和task
	# process=Process.sequential指定agent执行顺序为顺序执行模式
	# process=Process.hierarchical指定agent执行顺序为层次化执行
	# @crew
	# def crew(self) -> Crew:
	# 	return Crew(
	# 		agents=self.agents,
	# 		tasks=self.tasks,
	# 		process=Process.sequential,
	# 		verbose=True
	# 	)

	@crew
	def crewA(self) -> Crew:
		return Crew(
			agents=[self.lead_market_analyst()],
			tasks=[self.research_task()],
			process=Process.sequential,
			verbose=True
		)

	@crew
	def crewB(self) -> Crew:
		return Crew(
			agents=[self.chief_marketing_strategist(), self.creative_content_creator()],
			tasks=[self.project_understanding_task(), self.marketing_strategy_task(), self.campaign_idea_task(), self.copy_creation_task()],
			process=Process.sequential,
			verbose=True
		)


	# Pipeline类将crew组合成一个可执行的流水线
	# 通过@pipeline装饰器定义pipeline，创建一个Pipeline实例
	# stages:编排crew的一个独立部分，可以是连续的crew编排，也可以是并行的crew编排
	@pipeline
	def my_pipeline(self) -> Pipeline:
		return Pipeline(
			stages = [self.crewA(), self.crewB()]
		)



# 测试
if __name__ == "__main__":
	customer_domain = 'https://www.emqx.com/zh'
	project_description = """
	EMQX 是一种开源的分布式消息中间件，专注于处理物联网 (IoT) 场景下的大规模消息通信。它基于MQTT协议，能够实现高并发、低延迟的实时消息推送，支持设备之间、设备与服务器之间的双向通信。
	客户领域： 分布式消息中间件解决方案
	项目概述： 创建一个全面的营销活动，以提高企业客户对 EMQX 服务的认识和采用。
	"""

	# # 1、测试运行crew
	# input_data = {"customer_domain": customer_domain, "project_description": project_description}
	# result = CrewtestprojectCrew(my_llm(LLM_TYPE)).crew().kickoff(inputs=input_data)
	# print('输出结果为:',result)


	# # 2、方式1-测试运行pipeline(官方文档方式)
	# input_data = [{"customer_domain": customer_domain,"project_description": project_description}]
	# async def testPiple(input_data):
	# 	my_pipeline = Pipeline(
	# 		stages=[CrewtestprojectCrew(my_llm(LLM_TYPE)).crew()]
	# 	)
	# 	results = await my_pipeline.kickoff(inputs=input_data)
	# 	for result in results:
	# 		print(f"Final Output_json",result)
	# 		print(f"Token Usage: {result.token_usage}")
	#
	# # 在异步环境中运行
	# asyncio.run(testPiple(input_data))


	# 3、方式2-测试运行pipeline
	input_data = [{"customer_domain": customer_domain,"project_description": project_description}]
	async def testPiple(input_data):
		results = await CrewtestprojectCrew(my_llm(LLM_TYPE)).my_pipeline().kickoff(inputs=input_data)
		for result in results:
			print(f"Final Output_json",result)
			print(f"Token Usage: {result.token_usage}")

	# 在异步环境中运行
	asyncio.run(testPiple(input_data))