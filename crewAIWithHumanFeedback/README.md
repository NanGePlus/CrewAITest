# 1、项目介绍
本期视频演示项目实现一个营销战略协作智能体                                              
上一期视频主要学习如何让任务以格式化数据输出，如自定义JSON数据格式并最终以JSON格式输出              
本期视频主要学习Human Feedback(HF，人类反馈)         
### (1)Human Feedback基础概念
Human Feedback（人类反馈）是指人类在评估和改进人工智能模型行为过程中提供的反馈信息                 
它通常被用于帮助训练、优化和监督机器学习模型，特别是大规模语言模型              
通过人类反馈，AI 模型能够更好地理解人类意图、提供更符合预期的响应，并减少生成错误或有害内容的几率              
### (2)Human Feedback关键作用
**模型训练中的监督：**                
在训练过程中，人类会对模型的输出进行评价，指出哪些答案是正确的，哪些是不正确的。这些反馈被用来调整模型的参数，使其产生更准确和有效的结果                
**强化学习中的人类反馈 (RLHF)：**                   
强化学习中的人类反馈（Reinforcement Learning from Human Feedback, RLHF） 是一种通过人类反馈信号优化模型的技术。具体做法是：             
人类评审员会对模型的多个输出进行排名                    
模型通过这些人类给出的排名，学会哪些输出是优先的                  
最终，模型通过这些反馈不断改进决策能力                
这种方法已经被应用于生成式 AI，如 GPT-3 和 GPT-4，以确保模型的输出与用户期望更加一致。                               
**内容审查和安全性提升：**             
人类反馈被用来审查模型生成的内容，确保输出不包含有害、不准确、或违反政策的内容。这种方式有助于改进 AI 的安全性和合规性。            
**持续优化：**                   
Human Feedback 不仅在模型的初始训练阶段有用，在模型上线后也会持续进行，以确保模型随着时间推移能够适应新的数据和任务。                  
### (3)Human Feedback挑战
主观性：不同的人类评审员可能会对同一输出有不同的判断，因此反馈结果可能存在主观差异              
反馈量的限制：收集足够多的高质量人类反馈可能需要大量时间和资源             
一致性问题：人类评审员在不同情况下提供一致、标准化的反馈是一个挑战                 
### (4)案例简介
**(1)定义了3个Agent**               
lead_market_analyst:           
  role: >            
    首席市场分析师               
  goal: >              
    以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析，并为营销战略的制定提供专业指导。              
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席市场分析师。               
    你的专长是以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析。                     
chief_marketing_strategist:                
  role: >               
    首席营销战略师                 
  goal: >               
    基于产品的市场分析内容，以敏锐的洞察力制定出令人惊喜的营销战略。                   
  backstory: >                 
    你任职在一家一流数字营销公司，你的职位是首席营销战略师。                  
    你的专长是能够制定出成功的定制营销战略。               
creative_content_creator:           
  role: >               
    首席创意内容创作师               
  goal: >                  
    基于产品的营销战略内容，为社交媒体活动开发有吸引力的创新内容。               
    重点是创建高影响力的广告文案。                 
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席创意内容创作师。             
    你的专长是能够将营销战略转化为引人入胜的故事和视觉内容，吸引注意力并激发行动。               
**(2)定义了5个Task**                        
research_task:             
  description: >                
    基于客户提供的{customer_domain}对客户提供的产品和竞争对手进行深入的剖析。请确保找到任何有趣的相关信息，日期限定为2024年。                
    我们正在就以下项目与他们合作：            
    {project_description}。            
  expected_output: >              
    关于客户、客户提供的产品和竞争对手的完整报告、包括指标统计、偏好、市场定位和受众参与度。              
  agent: lead_market_analyst                      
project_understanding_task:                 
  description: >                    
    了解{project_description}的项目细节和目标受众。查看提供的任何材料，并根据需要收集更多信息。                 
  expected_output: >                  
    项目的详细摘要和目标受众的简介。                 
  agent: chief_marketing_strategist                   
marketing_strategy_task:               
  description: >                 
    基于客户提供的{customer_domain}和{project_description}为项目制定全面的营销战略。                   
    充分使用从研究任务和项目理解任务中获得的见解来制定高质量的战略。               
  expected_output: >                  
    一份详细的营销战略文件，概述目标、目标受众、关键信息和建议的策略，确保包含名称、策略、渠道和关键绩效指标。                   
  agent: chief_marketing_strategist                
campaign_idea_task:                  
  description: >                  
    为{project_description}开发富有创意的营销活动构思。               
    确保创意新颖、吸引人，并与整体营销战略保持一致。                 
  expected_output: >                  
    列出 5 个活动设想，每个设想都有简要说明和预期影响。                   
  agent: creative_content_creator                      
copy_creation_task:                
  description: >                  
    根据已获批准的{project_description}活动创意制作营销文案。                   
    确保文案引人注目、清晰明了，并适合目标受众。                  
  expected_output: >                 
    每个活动创意的营销副本。                  
  agent: creative_content_creator                                                                    


# 2、前期准备工作
往期相关视频:                 
(1)【Agent应用案例1-基础】使用CrewAI+FastAPI打造多Agent协作应用并对外提供API服务，支持gpt、通义千问、Ollama本地大模型对比测试                      
对应工程文件夹为:crewaitest                   
https://www.bilibili.com/video/BV1N44reDEt3/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                                 
https://youtu.be/2TE5DlYlvGw                                                
## 2.1 CrewAI介绍
### (1)简介
CrewAI是一个用于构建多Agent系统的工具，它能够让多个具有不同角色和目标的Agent共同协作，完成复杂的Task                
该工具可以将Task分解，分配给不同的Agent，借助它们的特定技能和工具，完成各自的职责，最终实现整体任务目标              
官网:https://www.crewai.com/                                          
GitHub:https://github.com/crewAIInc/crewAI                                          
官方首页的介绍:                          
AI Agents for real use cases                                           
Most AI agent frameworks are hard to use.We provide power with simplicity.                                           
Automate your most important workflows quickly.            
### (2)核心概念
**Agents:**          
是一个自主可控单元，通过编程可以实现执行任务、作出决定、与其他Agent协作交流          
可类比为团队中的一员，拥有特定的技能和任务                    
属性:             
role(角色):定义Agent在团队中的角色功能                              
goal(目标):Agent实现的目标                             
backstory(背景信息):为Agent提供上下文                                    
**Tasks:**               
分配给Agent的具体任务，提供执行任务所需的所有细节                          
属性:                         
description(任务描述):简明扼要说明任务要求                                                 
agent(分配的Agent):分配负责该任务的Agent                                                
expected_output(期望输出):任务完成情况的详细描述                                                         
Tools(工具列表):为Agent提供可用于执行该任务的工具列表                   
output_json(输出json):输出一个json对象，只能输出一种数据格式                    
output_file(工具列表):将任务结果输出到一个文件中，指定输出的文件格式                                                     
context(上下文):指定其输出被用作该任务上下文的任务                                  
**Processes**                      
CrewAI中负责协调Agent执行任务                        
类似于团队中的项目经理                        
确保任务分配和执行效率与预定计划保持一致                       
目前拥有两种实施机制:                             
sequential(顺序流程):反映了crew中动态的工作流程，以深思熟虑的和系统化的方式推进各项任务，按照任务列表中预定义的顺序执行，一个任务的输出作为下一个任务的上下文            
hierarchical(分层流程):允许指定一个自定义的管理Agent，负责监督任务执行，包括计划、授权和验证。任务不是预先分配的，而是根据Agent的能力进行任务分配，审查产出并评估任务完成情况              
**Crews:**          
1个crew代表一组合作完成一系列任务的Agent                        
每个crew定义了任务执行策略、Agent协作和整体工作流程                                          
属性:                               
Tasks(任务列表):分配给crew的任务列表                                                          
Agents(Agent列表):分配给crew的Agent列表                                                         
Process(背景信息):crew遵循的流程                              
manager_llm(大模型):在hierarchical模式下指定大模型                                                                             
language(语言):指定crew使用的语言                                                                                               
language_file(语言文件):指定crew使用的语言文件                        
**Pipleline:**          
在CrewAI中,pipleline代表一种结构化的工作流程，允许多个crew顺序或并行执行           
提供了一种组织涉及多个阶段的复杂流程的方法，其中一个阶段的输出可作为后续阶段的输入                                                        
关键术语:                               
Stage:pipleline中的1个独立部分，可以是1个顺序crews，也可以是一个并行的crews                                                                       
Run:运行pipleling处理的单个实例                                                                    
Branch:Stage内的并行执行                                                      
Trace:单个输入在整个pipleline中的运行轨迹、捕捉它所经历的路径和转换            

## 2.2 anaconda、pycharm 安装   
anaconda:提供python虚拟环境，官网下载对应系统版本的安装包安装即可                                      
pycharm:提供集成开发环境，官网下载社区版本安装包安装即可                                               
可参考如下视频进行安装，【大模型应用开发基础】集成开发环境搭建Anaconda+PyCharm                                                          
https://www.bilibili.com/video/BV1q9HxeEEtT/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                             
https://youtu.be/myVgyitFzrA                                           

## 2.3 GPT大模型使用方案            
可以使用代理的方式，具体代理方案自己选择                                   
可以参考视频《GraphRAG最新版本0.3.0对比实战评测-使用gpt-4o-mini和qwen-plus分别构建近2万字文本知识索引+本地/全局检索对比测试》中推荐的方式:                                    
https://www.bilibili.com/video/BV1maHxeYEB1/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                                    
https://youtu.be/iXfsJrXCEwA                     

## 2.4 非GPT大模型(国产大模型)使用方案,OneAPI安装、部署、创建渠道和令牌 
### （1）OneAPI是什么
官方介绍：是OpenAI接口的管理、分发系统             
支持 Azure、Anthropic Claude、Google PaLM 2 & Gemini、智谱 ChatGLM、百度文心一言、讯飞星火认知、阿里通义千问、360 智脑以及腾讯混元             
### (2)安装、部署、创建渠道和令牌   
创建渠道：大模型类型(通义千问)、APIKey(通义千问申请的真实有效的APIKey)                 
创建令牌：创建OneAPI的APIKey，后续代码中直接调用此APIKey                
### (3)详细介绍可以观看这期视频 
【GraphRAG+阿里通义千问大模型】构建+检索全流程实操，打造基于知识图谱的本地知识库，本地搜索、全局搜索二合一          
https://www.bilibili.com/video/BV1yzHxeZEG5/?vd_source=30acb5331e4f5739ebbad50f7cc6b949            
https://youtu.be/w9CRDbafhPI              
     
## 2.5 本地开源大模型使用方案,Ollama          
### （1）Ollama是什么
Ollama是一个轻量级、跨平台的工具和库，专门为本地大语言模型(LLM)的部署和运行提供支持          
它旨在简化在本地环境中运行大模型的过程，不需要依赖云服务或外部API，使用户能够更好地掌控和使用大型模型                
### （2）Ollama安装、启动、下载大模型
安装Ollama，进入官网https://ollama.com下载对应系统版本直接安装即可                                      
启动Ollama，安装所需要使用的本地模型，执行指令进行安装即可，参考如下:                                              
ollama pull qwen2:latest                                                
ollama pull llama3.1:latest                                             
ollama pull gemma2:latest                                                  
ollama pull nomic-embed-text:latest                                                   
其中:                            
qwen2:latest(7b),对应版本有0.5b、1.5b、7b、72b;                 
llama3.1:latest(8b)，对应版本有8b、70b、405b;                 
gemma2:latest(9b)，对应版本有2b、9b、27b等                      
embedding模型:nomic-embed-text:latest(也就是1.5版本)                  
### (3)详细介绍可以观看这期视频                                                 
【GraphRAG+Ollama】本地开源大模型llama3.1与qwen2构建+检索全流程实操对比评测，打造基于知识图谱的本地知识库，本地搜索、全局搜索二合一               
https://www.bilibili.com/video/BV1mpH9eVES1/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                                                
https://youtu.be/thNMan45lWA                           
                       

# 3、项目初始化
## 3.1 下载源码
GitHub或Gitee中下载工程文件到本地，下载地址如下：                
https://github.com/NanGePlus/CrewAITest          
https://gitee.com/NanGePlus/CrewAITest                 

## 3.2 构建项目
使用pycharm构建一个项目，为项目配置虚拟python环境               
项目名称：CrewAITest                  

## 3.3 将相关代码拷贝到项目工程中           
直接将下载的文件夹中的文件拷贝到新建的项目目录中               

## 3.4 安装项目依赖          
命令行终端中执行cd crewAIWithMarketingStrategy 命令进入到该文件夹内，然后执行如下命令安装依赖包                                           
pip install -r requirements.txt            
每个软件包后面都指定了本次视频测试中固定的版本号           
# 4、项目测试          
### （1）运行main脚本启动API服务
在使用python main.py命令启动脚本前，需根据自己的实际情况调整代码中的如下参数:               
**openai模型相关配置 根据自己的实际情况进行调整**              
OPENAI_API_BASE = "https://api.wlai.vip/v1"            
OPENAI_CHAT_API_KEY = "sk-XmrIEFplNArLlYa0E8C5A7C5F82041FdBd923e9d115746D0"          
OPENAI_CHAT_MODEL = "gpt-4o-mini"           
**非gpt大模型相关配置(oneapi方案 通义千问为例) 根据自己的实际情况进行调整**              
ONEAPI_API_BASE = "http://139.224.72.218:3000/v1"            
ONEAPI_CHAT_API_KEY = "sk-0FxX9ncd0yXjTQF877Cc9dB6B2F44aD08d62805715821b85"               
ONEAPI_CHAT_MODEL = "qwen-max"               
**本地大模型相关配置(Ollama方案 llama3.1:latest为例) 根据自己的实际情况进行调整**             
OLLAMA_API_BASE = "http://localhost:11434/v1"                
OLLAMA_CHAT_API_KEY = "ollama"          
OLLAMA_CHAT_MODEL = "llama3.1:latest"             
**openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型**              
MODEL_TYPE = "openai"           
**API服务设置相关  根据自己的实际情况进行调整**              
PORT = 8012  # 服务访问的端口                

### （2）运行apiTest脚本进行测试            
在运行python apiTest.py命令启动脚本前，需根据自己的实际情况调整代码中的如下参数:                  
**调整1:默认非流式输出 True or False**                  
stream_flag = False                  
**调整2:检查URL地址中的IP和PORT是否和main脚本中相同**                  
url = "http://localhost:8012/v1/chat/completions"                      
