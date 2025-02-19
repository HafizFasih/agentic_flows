# type: ignore
from crewai.flow.flow import Flow, start, listen, and_
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class OrchestratorFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def In(self):
        print("Starting the flow...")

    @listen(In)
    def Orchestrator(self):
        print("Orchestrator...")

    @listen("Orchestrator")
    def LLMCall1(self):
        print("LLMCall1...")

    @listen("Orchestrator")
    def LLMCall2(self):
        print("LLMCall2...")
        
    @listen("Orchestrator")
    def LLMCall3(self):
        print("LLMCall3...")

    @listen(and_("LLMCall1", "LLMCall2", "LLMCall3"))
    def Synthesizer(self):
        print("Synthesizer...")

    @listen("Synthesizer")
    def Out(self):
        print("Out...")

def kickoff():
    flow = OrchestratorFlow()
    flow.kickoff()
    flow.plot("own")

if __name__ == "__main__":
    kickoff()
