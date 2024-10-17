import requests
import json
import logging


# 设置日志模版
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


url = "http://localhost:8012/v1/chat/completions"
headers = {"Content-Type": "application/json"}


# 构造消息体
# 默认非流式输出 True or False
stream_flag = False
# 用户输入
# customer_domain = 'crewai.com'
# project_description = """
# CrewAI 是一家领先的多代理系统供应商，旨在为其企业客户的营销自动化带来革命性的变化。该项目包括制定创新营销战略，展示 CrewAI 先进的人工智能驱动解决方案，强调易用性、可扩展性和集成能力。营销活动将针对大中型企业中精通技术的决策者，突出 CrewAI 平台的成功案例和变革潜力。
# 客户领域： 人工智能和自动化解决方案
# 项目概述： 创建一个全面的营销活动，以提高企业客户对 CrewAI 服务的认识和采用。
# """

customer_domain = 'https://www.emqx.com/zh'
project_description = """
EMQX 是一种开源的分布式消息中间件，专注于处理物联网 (IoT) 场景下的大规模消息通信。它基于MQTT协议，能够实现高并发、低延迟的实时消息推送，支持设备之间、设备与服务器之间的双向通信。
客户领域： 分布式消息中间件解决方案
项目概述： 创建一个全面的营销活动，以提高企业客户对 EMQX 服务的认识和采用。
"""

data = {
    "messages": [{"role": "user", "customer_domain": customer_domain, "project_description": project_description}],
    "stream": stream_flag,
}


# 接收流式输出
if stream_flag:
    try:
        with requests.post(url, stream=True, headers=headers, data=json.dumps(data)) as response:
            for line in response.iter_lines():
                if line:
                    json_str = line.decode('utf-8').strip("data: ")
                    # 检查是否为空或不合法的字符串
                    if not json_str:
                        logger.info(f"收到空字符串，跳过...")
                        continue
                    # 确保字符串是有效的JSON格式
                    if json_str.startswith('{') and json_str.endswith('}'):
                        try:
                            data = json.loads(json_str)
                            if data['choices'][0]['finish_reason'] == "stop":
                                logger.info(f"接收JSON数据结束")
                            else:
                                logger.info(f"流式输出，响应内容是: {data['choices'][0]['delta']['content']}")
                        except json.JSONDecodeError as e:
                            logger.info(f"JSON解析错误: {e}")
                    else:
                        print(f"无效JSON格式: {json_str}")
    except Exception as e:
        print(f"Error occurred: {e}")

# 接收非流式输出处理
else:
    # 发送post请求
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # logger.info(f"接收到返回的响应原始内容: {response.json()}\n")
    content = response.json()['choices'][0]['message']['content']
    logger.info(f"非流式输出，响应内容是: {content}\n")