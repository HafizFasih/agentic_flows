# type: ignore
from crewai.flow.flow import Flow, start, listen, and_

class OrchestratorFlow(Flow):
    def __init__(self):
        super().__init__()
        self.text = "The quick brown fox jumps over the lazy dog"
        self.results = {}

    @start()
    def In(self):
        print("Starting the flow...")
        return self.text

    @listen(In)
    def Orchestrator(self, text):
        print("Orchestrator dividing the text into parts...")
        # Split text into 3 parts
        words = text.split()
        part1 = " ".join(words[:3])  # "The quick brown"
        part2 = " ".join(words[3:6])  # "fox jumps over"
        part3 = " ".join(words[6:])   # "the lazy dog"
        return {"part1": part1, "part2": part2, "part3": part3}

    @listen("Orchestrator")
    def LLMCall1(self, parts):
        print("LLMCall1 processing first part...")
        # Convert first part to uppercase
        self.results["part1"] = parts["part1"].upper()
        return self.results["part1"]

    @listen("Orchestrator")
    def LLMCall2(self, parts):
        print("LLMCall2 processing second part...")
        # Reverse the second part
        self.results["part2"] = " ".join(reversed(parts["part2"].split()))
        return self.results["part2"]
        
    @listen("Orchestrator")
    def LLMCall3(self, parts):
        print("LLMCall3 processing third part...")
        # Add exclamation marks to third part
        self.results["part3"] = parts["part3"] + "!!!"
        return self.results["part3"]

    @listen(and_("LLMCall1", "LLMCall2", "LLMCall3"))
    def Synthesizer(self, *args):
        print("Synthesizer combining results...")
        # Combine all processed parts
        combined = f"{self.results['part1']} | {self.results['part2']} | {self.results['part3']}"
        return combined

    @listen("Synthesizer")
    def Out(self, result):
        print("Final output:", result)
        return result

def main():
    flow = OrchestratorFlow()
    flow.kickoff()
    flow.plot("own")
