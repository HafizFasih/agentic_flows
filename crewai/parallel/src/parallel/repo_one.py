# type: ignore
from crewai.flow.flow import Flow, start, listen, or_
from litellm import completion

class ParallelFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_variant_1(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #1."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 1: {variant}")
        return variant

    @start()
    def generate_variant_2(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": "Generate a creative blog topic variant #2."}]
        )
        variant = response["choices"][0]["message"]["content"].strip()
        print(f"Variant 2: {variant}")
        return variant

    @listen(or_(generate_variant_1, generate_variant_2))
    def aggregate_variants(self, variant):
        # For simplicity, print the first variant received.
        print("Aggregated Variant:")
        print(variant)
        return variant

if __name__ == "__main__":
    flow = ParallelFlow()
    final = flow.kickoff()
    flow.plot("repo_one")
    print("Final Aggregated Output:")
    print(final)
