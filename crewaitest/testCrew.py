# 这段代码是用于执行、训练、回放、和测试CrewAI项目的主文件。它的功能是提供一种接口来启动项目的各个task和agent
# 该脚本通过提供4个主要功能 (run, train, replay, test)，让用户能够在不同的模式下运行和测试CrewAI项目


import sys
from crew import CrewtestprojectCrew


# run函数是启动Crew执行的入口
# kickoff是Crew执行的核心方法，它会启动所有代理并运行指定任务
def run():
    inputs = {
        'topic': 'AI LLMs'
    }
    CrewtestprojectCrew().crew().kickoff(inputs=inputs)


# train函数用于训练Crew，运行指定次数的迭代
# 从命令行获取n_iterations（训练迭代次数）和filename（训练保存的文件名）
# 使用 try-except 块捕获并处理潜在的异常，以防训练过程中发生错误
def train():
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewtestprojectCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")


# replay函数允许从一个特定的任务ID回放Crew的执行
# 从命令行获取task_id作为回放的起始点。
# replay方法用于重现之前的执行流程
def replay():
    try:
        CrewtestprojectCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")


# test函数是测试Crew项目的运行
# n_iterations和openai_model_name是命令行传入的参数，用来指定测试的迭代次数和使用的模型名称
# 测试执行任务并返回结果，同样使用try-except捕获潜在的错误
def test():
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        CrewtestprojectCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")



if __name__ == "__main__":
    result = run()
    print(f"最终得到的回复是：{result} ")
