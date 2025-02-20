#  type: ignore
from crewai.flow.flow import Flow, start, listen, and_

class WorkFlow(Flow):
    @start()
    def In(self):
        print("Hello, World!")
    @listen("In")
    def LLMCall1(self):
        print("Hello, World! from LLMCall1")
    @listen("In")
    def LLMCall2(self):
        print("Hello, World! from LLMCall2")
    @listen("In")
    def LLMCall3(self):
        print("Hello, World! from LLMCall3")

    @listen(and_("LLMCall1", "LLMCall2", "LLMCall3"))
    def Aggregator(self):
        print("This is Aggregator")

    @listen("Aggregator")
    def Out(self):
        print("This is Output")
    
def main():
    wf = WorkFlow()
    wf.kickoff()
    wf.plot("own")
