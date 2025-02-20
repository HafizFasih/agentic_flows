# type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_
import random
from litellm import completion

class ModelRouterFlow(Flow):
    @start()
    def Input(self):
        print("Routing question to appropriate model...")
        # Simulate different types of questions
        questions = [
            "Write a poem about spring",
            "What is 234 * 456?",
            "Explain quantum entanglement"
        ]
        return random.choice(questions)

    @router("Input")
    def QuestionRouter(self, question):
        if "poem" in question.lower() or "write" in question.lower():
            return "Creative"
        elif any(x in question.lower() for x in ["*", "+", "-", "/"]):
            return "Math"
        else:
            return "Science"

    @listen("Creative")
    def CreativeTask(self, question):
        print(f"Routing to Gemini for creative task: {question}")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": question}]
        )
        self.state["output"] = response.choices[0].message.content
        print(f"Response: {response.choices[0].message.content}")

    @listen("Math")
    def MathTask(self, question):
        print(f"Routing to Gemini for mathematical task: {question}")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": question}]
        )
        print(f"Response: {response.choices[0].message.content}")

    @listen("Science")
    def ScienceTask(self, question):
        print(f"Routing to Gemini for science task: {question}")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{"role": "user", "content": question}]
        )
        print(f"Response: {response.choices[0].message.content}")

    @listen(or_("CreativeTask", "MathTask", "ScienceTask"))
    def Output(self):
        print("Response generated successfully!")

def main():
    flow = ModelRouterFlow()
    flow.kickoff()
    flow.plot("llm")
