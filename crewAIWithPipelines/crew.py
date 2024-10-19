# 核心功能:在CrewAI中定义Agent和Task，并通过Crew来管理这些Agent和Task的执行流程

# 导入第三方库
from crewai import Agent, Crew, Process, Task, Pipeline
from crewai.project import CrewBase, agent, crew, task, pipeline
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
# 导入本应用程序提供的方法
from utils.models import MarketStrategy, CampaignIdea, Copy



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
