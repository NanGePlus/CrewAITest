# 1、项目介绍
## 1.1、本次分享介绍
本项目是在“营销战略协作智能体”项目的基础之上进行迭代，为大家分析crewAI的Flows功能            
“营销战略协作智能体”项目相关视频链接如下所示:                                                         
【Agent应用案例5-进阶】让任务以JSON数据格式并最终任务以JSON格式输出，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务                
https://www.bilibili.com/video/BV1i5bAeAEWn/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                 
https://youtu.be/w8uxBuVQVlg                                 

**本次分享内容主要为:**               
(1)截止2024.10.20，crewai最新版本0.74.2，crewai-tools最新版本0.13.2                                               
(2)代码实现crewai的Flows功能                              
(3)将Flows功能集成到main服务中对外提供API接口服务，进行接口联调测试                      

## 1.2、Flows介绍      
为构建复杂的AI自动化工作流提供了一个强大的框架     

**核心特点:**           
**(1)简化工作流程创建:** 轻松串联多个crews和任务(自定义的方法)，创建复杂的工作流              
**(2)状态管理:** Flows可以让您在工作流中的不同任务之间轻松管理和共享状态              
**(3)事件驱动架构:** 基于事件驱动模型构建，可实现动态响应的工作流           
**(4)灵活的控制流:** 在工作流中实现条件逻辑、循环和分支           

**关键参数:**            
**(1)@start()装饰器**
用于将一个方法标记为Flow的起点。在一个Flow中支持对多个方法进行@start()标记，当Flow启动时，所有用@start()装饰的方法都会并行执行           
**(2)@listen装饰器**
用于将一个方法标记为Flow中的监听器。在一个Flow中支持对多个方法进行@listen()装饰，当Flow启动后被监听的方法执行完成后，所有用@listen()监听该方法的方法都会被执行             
**(3)@router装饰器**
在Flow中允许根据方法的输出内容来定义路由的执行逻辑，根据方法的输出指定不同的路由，从而动态控制执行流程              
       
**条件控制:**              
**(1)条件逻辑 or_()**               
Flows中@listen()中可以使用or_()函数允许监听多个方法，在这些被监听方法中任何一个执行完成后，监听该方法的方法就会被执行               
**(2)条件逻辑 and_()**                       
Flows中@listen()中可以使用and_()函数允许监听多个方法，在这些被监听方法中全部执行完成后，监听该方法的方法就会被执行             

**结果输出:**                 
**(1)检索结果的最后输出**              
运行Flow时，最终的输出是由最后完成的方法决定的                                 
**(2)访问和更新状态**                
状态可用于在Flow中的不同方法之间存储和共享数据                       
**(3)状态管理**
有效管理状态对于构建可靠、可维护的AI工作流至关重要。 Flows为非结构化、结构化状态管理提供了强大的机制，允许根据需求自行选择            
非结构化状态管理:所有状态都存储在Flow类的状态属性中。这种方法具有很大的灵活性，开发人员可随时添加或修改状态属性，而无需定义严格的模式            
结构化状态管理:利用预定义的模式来确保整个工作流程的一致性和类型安全性               

## 1.3、回忆下这个项目所定义的Agent和Task               
### (1)定义了3个Agent        
lead_market_analyst:           
  role: >            
    **首席市场分析师**               
  goal: >              
    以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析，并为营销战略的制定提供专业指导。              
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席市场分析师。               
    你的专长是以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析。                     
chief_marketing_strategist:                
  role: >               
    **首席营销战略师**                 
  goal: >               
    基于产品的市场分析内容，以敏锐的洞察力制定出令人惊喜的营销战略。                   
  backstory: >                 
    你任职在一家一流数字营销公司，你的职位是首席营销战略师。                  
    你的专长是能够制定出成功的定制营销战略。               
creative_content_creator:           
  role: >               
    **首席创意内容创作师**               
  goal: >                  
    基于产品的营销战略内容，为社交媒体活动开发有吸引力的创新内容。               
    重点是创建高影响力的广告文案。                 
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席创意内容创作师。             
    你的专长是能够将营销战略转化为引人入胜的故事和视觉内容，吸引注意力并激发行动。              
                                 
### (2)定义了5个Task       
**research_task:**             
  description: >                
    基于客户提供的{customer_domain}对客户提供的产品和竞争对手进行深入的剖析。请确保找到任何有趣的相关信息，日期限定为2024年。                
    我们正在就以下项目与他们合作：            
    {project_description}。            
  expected_output: >              
    关于客户、客户提供的产品和竞争对手的完整报告、包括指标统计、偏好、市场定位和受众参与度。              
  agent: lead_market_analyst                      
**project_understanding_task:**                 
  description: >                    
    了解{project_description}的项目细节和目标受众。查看提供的任何材料，并根据需要收集更多信息。                 
  expected_output: >                  
    项目的详细摘要和目标受众的简介。                 
  agent: chief_marketing_strategist                   
**marketing_strategy_task:**               
  description: >                 
    基于客户提供的{customer_domain}和{project_description}为项目制定全面的营销战略。                   
    充分使用从研究任务和项目理解任务中获得的见解来制定高质量的战略。               
  expected_output: >                  
    一份详细的营销战略文件，概述目标、目标受众、关键信息和建议的策略，确保包含名称、策略、渠道和关键绩效指标。                   
  agent: chief_marketing_strategist                
**campaign_idea_task:**                  
  description: >                  
    为{project_description}开发富有创意的营销活动构思。               
    确保创意新颖、吸引人，并与整体营销战略保持一致。                 
  expected_output: >                  
    列出 5 个活动设想，每个设想都有简要说明和预期影响。                   
  agent: creative_content_creator                      
**copy_creation_task:**                
  description: >                  
    根据已获批准的{project_description}活动创意制作营销文案。                   
    确保文案引人注目、清晰明了，并适合目标受众。                  
  expected_output: >                 
    每个活动创意的营销副本。                  
  agent: creative_content_creator                                                                    


# 2、前期准备工作
## 2.1 开发环境搭建:anaconda、pycharm
anaconda:提供python虚拟环境，官网下载对应系统版本的安装包安装即可                                      
pycharm:提供集成开发环境，官网下载社区版本安装包安装即可                                               
可参考如下视频进行安装，【大模型应用开发基础】集成开发环境搭建Anaconda+PyCharm                                                          
https://www.bilibili.com/video/BV1q9HxeEEtT/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                             
https://youtu.be/myVgyitFzrA          

## 2.2 大模型相关配置
(1)GPT大模型使用方案              
(2)非GPT大模型(国产大模型)使用方案(OneAPI安装、部署、创建渠道和令牌)                 
(3)本地开源大模型使用方案(Ollama安装、启动、下载大模型)                         
可参考如下视频:                         
提供一种LLM集成解决方案，一份代码支持快速同时支持gpt大模型、国产大模型(通义千问、文心一言、百度千帆、讯飞星火等)、本地开源大模型(Ollama)                       
https://www.bilibili.com/video/BV12PCmYZEDt/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                 
https://youtu.be/CgZsdK43tcY                                                                      


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
命令行终端中执行cd crewAIWithFlows 命令进入到该文件夹内，然后执行如下命令安装依赖包                                           
pip install -r requirements.txt            
每个软件包后面都指定了本次视频测试中固定的版本号         
**注意:** 截止2024.10.20，本项目crewai最新版本0.74.2，crewai-tools最新版本0.13.2，建议先使用要求的对应版本进行本项目测试，避免因版本升级造成的代码不兼容。测试通过后，可进行升级测试。          

# 4、项目测试          
## (1)测试官方的用例模版
打开命令行终端执行cd crewAIWithFlows进入该文件夹下，执行crewai create flow flowsTest 创建应用案例模版工程
在工程源码的main.py中添加如下代码段
import os              
os.environ["OPENAI_API_BASE"] = "https://api.wlai.vip/v1"             
os.environ["OPENAI_API_KEY"] = "sk-dvdCgdO3LSWYgqnMiJR5NqG0eLSTM69yjryjD6LuL3lWkvf3"              
os.environ["OPENAI_MODEL_NAME"] = "gpt-4o-mini"           

最后运行python main.py进行测试             
           
## (2)测试Flows功能
在使用python flowsTest.py命令启动脚本前，需根据自己的实际情况调整utils/myLLM.py代码中参数            
## (3)集成Flows功能，运行main脚本启动API服务
运行 python main.py                 
## (4)运行apiTest脚本进行测试            
在运行python apiTest.py命令启动脚本前，需根据自己的实际情况调整代码中的如下参数:                  
**调整1:默认非流式输出 True or False**                  
stream_flag = False                  
**调整2:检查URL地址中的IP和PORT是否和main脚本中相同**                  
url = "http://localhost:8012/v1/chat/completions"        
                    
