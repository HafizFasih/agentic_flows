# type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_
import random

class RouterFlow(Flow):
    @start()
    def In(self):
        print("This is In...")
        subject = random.choice(["English", "Mathematics", "Physics"])
        return subject

    @router("In")
    def LLMCallRouter(self, subject):
        if(subject == "English"):
            return "English"
        elif(subject == "Mathematics"):
            return "Mathematics"
        else:
            return "Physics"        

    @listen("English")
    def LLMCall1(self):
        print("I am an English expert.")

    @listen("Mathematics")
    def LLMCall2(self):
        print("I am a Mathematics expert.")

    @listen("Physics")
    def LLMCall3(self):
        print("I am a Physics expert.")

    @listen(or_("LLMCall1", "LLMCall2", "LLMCall3"))
    def Out(self):
        print("This is out...")

def main():
    flow = RouterFlow()
    flow.kickoff()
    flow.plot("own")
