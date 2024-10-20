# 导入第三方库
from crewai.flow.flow import Flow, listen, start
from crews.marketAnalystCrew.marketAnalystCrew import marketAnalystCrew
from crews.contentCreatorCrew.contentCreatorCrew import contentCreatorCrew


class testFlow(Flow):

    def __init__(self, model, inputData):
        super().__init__()
        self.model = model
        self.inputData = inputData

    @start()
    def marketAnalystCrew(self):
        result = marketAnalystCrew(self.model).crew().kickoff(inputs=self.inputData)
        print("marketAnalystCrew result:", result)
        return result
    @listen(marketAnalystCrew)
    def contentCreatorCrew(self):
        result = contentCreatorCrew(self.model).crew().kickoff(inputs=self.inputData)
        print("contentCreatorCrew result:", result)
        return result

