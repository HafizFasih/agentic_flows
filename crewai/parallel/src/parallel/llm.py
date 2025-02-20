#  type: ignore
from crewai.flow.flow import Flow, start, listen, and_
from litellm import completion

class WorkFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    output = {}
    @start()
    def In(self):
        return "Generate three different creative ideas"

    @listen("In")
    def LLMIdeaGenerator(self, prompt):
        response = completion(
            model=self.model,
            messages=[{
                "role": "user", 
                "content": f"{prompt} for different domains"
            }]
        )
        ideas = response["choices"][0]["message"]["content"].strip()
        print("Generated Ideas:", ideas)
        return ideas

    @listen("LLMIdeaGenerator")
    def MobileAppAnalyzer(self, ideas):
        # Process and analyze ideas for mobile context
        mobile_analysis = f"Mobile App Analysis:\n{ideas}"
        self.output['mobile_analysis'] = mobile_analysis
        print("Mobile Analysis Complete")

    @listen("LLMIdeaGenerator")
    def WebServicePlanner(self, ideas):
        # Process and plan implementation for web context
        web_plan = f"Web Service Plan:\n{ideas}"
        self.output['web_plan'] = web_plan
        print("Web Planning Complete")

    @listen("LLMIdeaGenerator")
    def AIFeasibilityChecker(self, ideas):
        # Check AI feasibility and requirements
        ai_feasibility = f"AI Feasibility Report:\n{ideas}"
        self.output['ai_feasibility'] = ai_feasibility
        print("AI Feasibility Check Complete")

    @listen(and_("MobileAppAnalyzer", "WebServicePlanner", "AIFeasibilityChecker"))
    def Aggregator(self):
        mobile_analysis, web_plan, ai_feasibility = (
            self.output.get(key) for key in self.output.keys()
        )
        combined = f"""Combined Analysis:
        {mobile_analysis}
        {web_plan}
        {ai_feasibility}"""
        print("\nAggregated Analysis:", combined)
        return combined

    @listen("Aggregator")
    def Out(self, combined_analysis):
        print("\nAnalysis Complete")
        return combined_analysis
    
def main():
    wf = WorkFlow()
    wf.kickoff()
    wf.plot("llm")
