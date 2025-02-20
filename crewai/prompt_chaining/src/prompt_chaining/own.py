# type: ignore
from crewai.flow.flow import Flow, start, listen

class ParallelFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    @start()
    def In(self):
        print("This is In...")
    
    @listen("In")
    def LLMCall1(self):
        print("This is LLMCall1...")
    
    @listen("LLMCall1")
    def LLMCall2(self):
        print("This is LLMCall2...")

    @listen("LLMCall2")
    def LLMCall3(self):
        print("This is LLMCall3...")
    
    @listen("LLMCall3")
    def Out(self):
        print("This is Out...")
    
def main():
    flow = ParallelFlow()
    flow.kickoff()
    flow.plot("own")
