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
# game = "What is the game you would like to build? What will be the mechanics?"

# game = '''
# 1、游戏名称：经典贪吃蛇
# 2、游戏描述：玩家控制一条不断移动的蛇，目标是吃掉屏幕上出现的食物，让蛇变得越来越长。游戏结束的条件是蛇撞到自己或墙壁。
# 3、游戏机制：
# 基本操作：玩家使用方向键（上下左右）控制蛇的移动方向。蛇只能向当前方向前进，不能倒退。
# 游戏目标：吃掉屏幕上随机出现的食物，每吃一个，蛇的长度会增加。游戏难度随着蛇的长度增加而提升。
# 得分系统：每吃一个食物得1分，游戏结束时，玩家的分数是最终蛇吃到食物的总数。
# 游戏结束条件：撞到自己的身体或撞到屏幕边界时，游戏结束。
# '''

game = '''
1、游戏名称：经典俄罗斯方块
2、游戏描述：玩家通过移动和旋转下落的方块，使它们在底部排成完整的行。每当一行被填满，行就会消失，玩家获得积分。方块下落速度控制在一个合理的速度上，不要快。要求四种不同形状的方块，分别为I、T、L、Z，每个方块由四个小方格组成。
3、游戏机制：
(1)基本操作：
方向键左/右：移动方块左右。
方向键下：加速方块下落。
方向键上：旋转方块。
(2)游戏目标：
排列下落的方块，使它们在底部形成完整的行。
当一行被完全填满，没有空隙时，该行会消除并获得积分。
(3)得分系统：
每消除一行得分1分，一次消除多行可获得额外得分。
随着时间推移，方块下落速度逐渐加快，难度逐步提升。
(4)游戏结束条件：当方块堆积到顶部，无法继续放置新的方块时，游戏结束。
'''



data = {
    "messages": [{"role": "user", "content": game}],
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