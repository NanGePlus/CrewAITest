# 核心功能:在CrewAI中定义Agent和Task，并通过Crew来管理这些Agent和Task的执行流程

# 导入相关的依赖包
from crewai import Agent, Crew, Process, Task
# CrewBase是一个装饰器，标记一个类为CrewAI项目。agent、task和crew装饰器用于定义agent、task和crew
from crewai.project import CrewBase, agent, crew, task
# 使用自定义工具
from tools.savePdfTool import saveText2Pdf
from tools.vectorSearchTool import vectorSearch



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
	# tools=[MyCustomTool()] 表示代理可以加载自定义工具，但此处为注释，需根据需求自行加载。
	@agent
	def retrieval_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['retrieval_agent'],
			verbose=True,
			llm=self.model,
			tools=[vectorSearch]
		)

	@agent
	def report_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['report_agent'],
			verbose=True,
			llm=self.model,
			tools=[saveText2Pdf]
		)

	# 通过@task装饰器定义research_task，返回一个Task实例
	# 配置文件为tasks.yaml中的research_task部分
	@task
	def retrieval_task(self) -> Task:
		return Task(
			config=self.tasks_config['retrieval_task'],
		)

	@task
	def report_task(self) -> Task:
		return Task(
			config=self.tasks_config['report_task'],

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



