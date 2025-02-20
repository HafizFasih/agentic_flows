# type: ignore
from crewai.flow.flow import Flow, start, listen, and_
from litellm import completion

class AndAggregationFlow(Flow):
    model = "gemini/gemini-1.5-flash"

    @start()
    def generate_slogan(self):
        # This task generates a creative slogan.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Generate a creative slogan for a futuristic brand."
            }]
        )
        slogan = response["choices"][0]["message"]["content"].strip()
        print("Slogan generated:", slogan)
        return slogan

    @start()
    def generate_tagline(self):
        # This task generates a creative tagline.
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": "Generate a creative tagline for a futuristic brand."
            }]
        )
        tagline = response["choices"][0]["message"]["content"].strip()
        print("Tagline generated:", tagline)
        return tagline

    @listen(and_(generate_slogan, generate_tagline))
    def combine_outputs(self, outputs):
        # The `and_` decorator ensures this method is called only when both tasks complete.
        # 'outputs' is a tuple containing the outputs of generate_slogan and generate_tagline.
        slogan, tagline = outputs
        combined = f"Combined Output: Slogan - '{slogan}' | Tagline - '{tagline}'"
        print("Aggregated Combined Output:", combined)
        return combined

def main():
    flow = AndAggregationFlow()
    final_output = flow.kickoff()
    flow.plot("repo_two")
    print("Final Output of the Flow:")
    print(final_output)
