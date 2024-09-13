# 1、项目介绍
本项目实现一个健康档案助手智能体                            
包含两个Agent，一个Agent负责根据医生询问的健康问题，从私有健康档案库(RAG)中检索相关内容               
另一个Agent负责根据检索的内容和问题进行健康分析并最终调用外部工具把生成的报告以PDF文件保存到本地             
回忆下RAG的功能:                 
离线步骤:文档加载->文档切分->向量化->灌入向量数据库                              
在线步骤:获取用户问题->用户问题向量化->检索向量数据库->将检索结果和用户问题填入prompt模版->用最终的prompt调用LLM->由LLM生成回复     
关于RAG的应用，大家可以观看这期视频:             
【流程实操】RAG+LangChain+FastAPI+OpenAI+通义千问打造私有领域知识库，构建和检索全流程源码分享，一份代码搞定多类型大模型集成                         
https://www.bilibili.com/video/BV1ryHxesEHs/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                       
https://youtu.be/xAEi5CWEIl0                      
### (1)定义了两个Agent        
retrieval_agent:              
  role: >                   
    健康档案检索专家                
  goal: >                 
    根据医生询问的健康问题: {topic}，从健康档案中检索相关记录。              
  backstory: >                    
    你是一位专业的健康档案检索专家，擅长在庞大的健康档案库中快速找到与用户健康问题相关的历史记录。                  
report_agent:              
  role: >                
    健康报告撰写专家                   
  goal: >            
    你的任务是分析从健康档案中检索到的相关数据，再结合医生问的问题 {topic} 并基于这些信息撰写一份简洁明了、富有医学依据的健康建议报告。                         
    你需要综合分析用户的病史、体检数据、生活方式等因素，确保报告内容能够帮助医生做出科学决策，并为患者提供个性化的健康改善建议。              
  backstory: >                                      
    你是一位医学背景的报告撰写专家，擅长分析健康档案并生成专业、易于医生理解的健康建议报告，内容既简洁又具有医学严谨性。                                     
### (2)定义了两个Task       
retrieval_task:             
  description: >                
    根据用户提供的健康问题: {topic} ，使用提供的外部工具tool从健康档案库中检索与其相关的所有健康信息。                  
  expected_output: >                  
    与用户健康问题密切相关的健康档案记录。                  
  agent: retrieval_agent                   
report_task:                  
  description: >                 
    根据健康档案检索专家返回的健康记录内容，再结合医生问的问题 {topic} ，撰写一份清晰、简洁的健康建议报告。报告应包括对用户当前健康状况的详细分析，并根据分析结果提供个性化的健康建议。         
    并使用提供的外部工具tool将报告内容存储到pdf文件               
  expected_output: >               
   一份包含健康状况分析和实际健康建议的报告，使用简洁的医学语言。                  
  agent: report_agent                                                


# 2、前期准备工作
往期相关视频:                 
(1)【Agent应用案例1-基础】使用CrewAI+FastAPI打造多Agent协作应用并对外提供API服务，支持gpt、通义千问、Ollama本地大模型对比测试                      
对应工程文件夹为:crewaitest                   
https://www.bilibili.com/video/BV1N44reDEt3/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                              
https://youtu.be/2TE5DlYlvGw                                            
(2)【Agent应用案例2-进阶】技术研究员智能体案例，Agent支持调用外部工具实现将生成的报告保存至PDF文件并下载至本地，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务                    
对应工程文件夹为:crewAIWithResearcher                    
https://www.bilibili.com/video/BV1Sy4HeiEBn/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                     
https://youtu.be/MGEdzUUKISw                                       
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
本应用案例需要用到的汉字字体包，请下载后将文件放置在对应的工程文件夹内         
https://pan.baidu.com/s/1fhg2ac2UUjdEXbWjJT2kuQ?pwd=1234 提取码: 1234                  

## 3.2 构建项目
使用pycharm构建一个项目，为项目配置虚拟python环境               
项目名称：CrewAITest                  

## 3.3 将相关代码拷贝到项目工程中           
直接将下载的文件夹中的文件拷贝到新建的项目目录中               

## 3.4 安装项目依赖          
命令行终端中执行cd crewAIWithRag 命令进入到该文件夹内，然后执行如下命令安装依赖包                                           
pip install -r requirements.txt            
每个软件包后面都指定了本次视频测试中固定的版本号           
# 4、项目测试          
### （1）测试外部工具
终端执行 cd unitTest 进入该文件夹下，对本次需要使用的两个工具进行测试                 

### （2）运行main脚本启动API服务
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

### （3）运行apiTest脚本进行测试            
在运行python apiTest.py命令启动脚本前，需根据自己的实际情况调整代码中的如下参数:                  
**调整1:默认非流式输出 True or False**                  
stream_flag = False                  
**调整2:检查URL地址中的IP和PORT是否和main脚本中相同**                  
url = "http://localhost:8012/v1/chat/completions"                      
