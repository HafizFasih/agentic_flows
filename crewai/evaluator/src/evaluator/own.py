# type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_

class EvaluatorFlow(Flow):
    @start()
    def In(self):
        print("Step 1 from In")
    
    @listen(or_("In", "rejected"))
    def LLMCallGenerator(self):
        print("Step 2 from LLMCallGenerator")
        age = int(input("Enter your age: "))
        print("\n")
        return age
    
    @router("LLMCallGenerator")
    def LLMCallEvaluator(self, age):
        print("Step 3 from LLMCallEvaluator")
        if age >= 18:
            return "accepted"
        return "rejected"

    @listen("accepted")
    def Out(self):
        print("Step 4 from Out")
    
def main():
    flow = EvaluatorFlow()
    flow.kickoff()
    flow.plot("own")

