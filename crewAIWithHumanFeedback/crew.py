# 核心功能:在CrewAI中定义Agent和Task，并通过Crew来管理这些Agent和Task的执行流程

# 导入相关的依赖包
from typing import List
from crewai import Agent, Crew, Process, Task
# CrewBase是一个装饰器，标记一个类为CrewAI项目。agent、task和crew装饰器用于定义agent、task和crew
from crewai.project import CrewBase, agent, crew, task
# 使用CrewAI官方提供的工具
# https://github.com/crewAIInc/crewAI-tools/tree/main/crewai_tools/tools
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from pydantic import BaseModel, Field



class MarketStrategy(BaseModel):
	"""Market strategy model"""
	name: str = Field(..., description="市场战略名称")
	tatics: List[str] = Field(..., description="市场战略中使用的战术清单")
	channels: List[str] = Field(..., description="市场战略中使用的渠道清单")
	KPIs: List[str] = Field(..., description="市场战略中使用的关键绩效指标清单")

class CampaignIdea(BaseModel):
	"""Campaign idea model"""
	name: str = Field(..., description="活动创意名称")
	description: str = Field(..., description="Description of the campaign idea")
	audience: str = Field(..., description="活动创意说明")
	channel: str = Field(..., description="活动创意渠道")

class Copy(BaseModel):
	"""Copy model"""
	title: str = Field(..., description="副本标题")
	body: str = Field(..., description="正文")



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
			human_input=True
		)

	@task
	def project_understanding_task(self) -> Task:
		return Task(
			config=self.tasks_config['project_understanding_task'],
			human_input=True

		)

	@task
	def marketing_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['marketing_strategy_task'],
			output_json=MarketStrategy,
			human_input=True
		)

	@task
	def campaign_idea_task(self) -> Task:
		return Task(
			config=self.tasks_config['campaign_idea_task'],
			output_json=CampaignIdea,
			human_input=True

		)

	@task
	def copy_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['copy_creation_task'],
			context=[self.marketing_strategy_task(), self.campaign_idea_task()],
			output_json=Copy,
			human_input=True
		)


	# Crew类将agent和task组合成一个执行队列，并根据指定的执行流程进行任务调度
	# 通过@crew装饰器定义crew，创建一个Crew实例
	# agents=self.agents和tasks=self.tasks分别自动获取@agent和@task装饰器生成的agent和task
	# process=Process.sequential指定agent执行顺序为顺序执行模式
	# process=Process.hierarchical指定agent执行顺序为层次化执行
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)



