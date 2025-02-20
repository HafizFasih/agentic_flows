# type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_
from litellm import completion

class ContentEvaluatorFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def In(self):
        print("Starting content evaluation flow...")
        return True

    @listen(or_("In", "rejected"))
    def LLMCallGenerator(self):
        print("Generating initial content...")
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a short paragraph about climate change."}]
        )
        content = response["choices"][0]["message"]["content"].strip()
        print("\nGenerated content:")
        print(content, "\n")
        return content

    @router("LLMCallGenerator") 
    def LLMCallEvaluator(self, content):
        print("Evaluating content quality...")
        response = completion(
            model=self.model,
            messages=[{
                "role": "user", 
                "content": f"Evaluate if this content is high quality and factual. Respond with only 'ACCEPT' or 'REJECT': {content}"
            }]
        )
        evaluation = response["choices"][0]["message"]["content"].strip()
        print(f"Evaluation result: {evaluation}\n")
        
        if "ACCEPT" in evaluation.upper():
            return "accepted"
        return "rejected"

    @listen("accepted")
    def Out(self):
        print("Content approved and flow completed!")

def main():
    flow = ContentEvaluatorFlow()
    flow.kickoff()
    flow.plot("llm")
