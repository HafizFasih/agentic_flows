# type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_

class EvaluatorFlow(Flow):
    @start()
    def In(self):
        print("Step 1 from In")
    
    @listen(or_("In", "retry"))
    def LLMCallGenerator(self):
        print("Step 2 from LLMCallGenerator")
        age = int(input("Enter your age: "))
        return age
    
    @router("LLMCallGenerator")
    def LLMCallEvaluator(self, age):
        print("Step 3 from LLMCallEvaluator")
        if age <= 18:
            return "retry"
        return "accepted"

    @listen("accepted")
    def Out(self):
        print("Step 4 from Out")
    
def kickoff():
    flow = EvaluatorFlow()
    flow.kickoff()
    flow.plot("own")

if __name__ == "__main__":
    kickoff()