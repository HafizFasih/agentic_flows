# type: ignore
from crewai.flow.flow import Flow, start, listen
from litellm import completion

class EvaluatorOptimizerFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_response(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Write a draft summary about the benefits of AI in education."}]
        )
        draft = response["choices"][0]["message"]["content"].strip()
        print("Initial Draft Summary:")
        print(draft)
        return draft

    @listen(generate_response)
    def evaluate_and_optimize(self, draft):
        # In a real-world scenario, you might get human feedback.
        # Here, we simulate optimization by asking the model for improvements.
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Critically evaluate and improve this summary: {draft}"}]
        )
        improved = response["choices"][0]["message"]["content"].strip()
        print("Improved Summary:")
        print(improved)
        return improved

def main():
    flow = EvaluatorOptimizerFlow()
    final_summary = flow.kickoff()
    flow.plot("repo")
    print("Final Summary:")
    print(final_summary)
