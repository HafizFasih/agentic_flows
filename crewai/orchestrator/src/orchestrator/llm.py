# type: ignore
from crewai.flow.flow import Flow, start, listen, and_
from litellm import completion

class OrchestratorFlow(Flow):
    def __init__(self):
        super().__init__()
        self.text = "Analyze the customer feedback: Service was slow but food was delicious. Prices reasonable."
        self.results = {}

    @start()
    def In(self):
        print("Starting sentiment analysis flow...\n")
        return self.text

    @listen(In)
    def Orchestrator(self, text):
        print("Orchestrator breaking down feedback analysis...")
        # Split into different aspects
        return {
            "service": "Service was slow",
            "food": "food was delicious",
            "price": "Prices reasonable"
        }

    @listen("Orchestrator")
    def LLMCall1(self, aspects):
        print("Analyzing service sentiment...")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{
                "role": "user", 
                "content": f"Analyze the sentiment (positive/negative/neutral) and provide a 1-5 rating for: {aspects['service']}"
            }]
        )
        self.results["service_analysis"] = response.choices[0].message.content
        return self.results["service_analysis"]

    @listen("Orchestrator")
    def LLMCall2(self, aspects):
        print("Analyzing food quality sentiment...")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{
                "role": "user", 
                "content": f"Analyze the sentiment (positive/negative/neutral) and provide a 1-5 rating for: {aspects['food']}"
            }]
        )
        self.results["food_analysis"] = response.choices[0].message.content
        return self.results["food_analysis"]
        
    @listen("Orchestrator")
    def LLMCall3(self, aspects):
        print("Analyzing price sentiment...")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{
                "role": "user", 
                "content": f"Analyze the sentiment (positive/negative/neutral) and provide a 1-5 rating for: {aspects['price']}"
            }]
        )
        self.results["price_analysis"] = response.choices[0].message.content
        return self.results["price_analysis"]

    @listen(and_("LLMCall1", "LLMCall2", "LLMCall3"))
    def Synthesizer(self, *args):
        print("\nGenerating comprehensive feedback report...\n")
        response = completion(
            model="gemini/gemini-1.5-flash",
            messages=[{
                "role": "user",
                "content": f"Create a brief summary report based on these analysis points:\nService: {self.results['service_analysis']}\nFood: {self.results['food_analysis']}\nPrice: {self.results['price_analysis']}"
            }]
        )
        return response.choices[0].message.content

    @listen("Synthesizer")
    def Out(self, result):
        with open("sentiment_analysis.txt", "w") as f:
            f.write(result)
        print("\nFinal Analysis Report:", result)
        return result

def main():
    flow = OrchestratorFlow()
    flow.kickoff()
    flow.plot("llm")
