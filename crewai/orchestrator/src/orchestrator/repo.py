# type: ignore
from crewai.flow.flow import Flow, start, listen
from litellm import completion
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())  

class OrchestratorFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def initial_draft(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Draft a short blog post about AI automation."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = draft
        print("Initial Draft:")
        print(draft)
        return draft

    @listen(initial_draft)
    def refine_draft(self, draft):
        # Simulate dynamic task delegation: iterate refinement.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Refine this draft for clarity and style: {draft}"}]
        )
        refined = response["choices"][0]["message"]["content"].strip()
        self.state["draft"] = refined
        print("Refined Draft:")
        print(refined)
        return refined

def main(): 
    flow = OrchestratorFlow()
    final_draft = flow.kickoff()
    flow.plot("repo")   
    print("Final Draft:")
    print(final_draft)
