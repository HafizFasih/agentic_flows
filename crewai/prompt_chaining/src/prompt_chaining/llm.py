# type: ignore
from crewai.flow.flow import Flow, start, listen
from litellm import completion

class ParallelFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    
    def __init__(self):
        super().__init__()
        self.story_elements = {}
    
    @start()
    def In(self):
        print("Starting story generation...")
        self.story_elements['theme'] = "A sci-fi adventure"
    
    @listen("In")
    def LLMCall1(self):
        print("Generating main character...")
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Create a main character for {self.story_elements['theme']}. Describe them in 2-3 sentences."
            }]
        )
        self.story_elements['character'] = response.choices[0].message.content
        print(f"Character: {self.story_elements['character']}")
    
    @listen("LLMCall1")
    def LLMCall2(self):
        print("Generating plot setup...")
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Given this character: {self.story_elements['character']}, create an initial plot setup for {self.story_elements['theme']} in 2-3 sentences."
            }]
        )
        self.story_elements['plot'] = response.choices[0].message.content
        print(f"Plot: {self.story_elements['plot']}")

    @listen("LLMCall2")
    def LLMCall3(self):
        print("Generating conflict...")
        response = completion(
            model=self.model,
            messages=[{
                "role": "user",
                "content": f"Based on this plot: {self.story_elements['plot']}, create a major conflict for the character in 2-3 sentences."
            }]
        )
        self.story_elements['conflict'] = response.choices[0].message.content
        print(f"Conflict: {self.story_elements['conflict']}")
    
    @listen("LLMCall3")
    def Out(self):
        print("\nFinal Story Elements:")
        for key, value in self.story_elements.items():
            print(f"\n{key.capitalize()}:")
            print(value)
    
def main():
    flow = ParallelFlow()
    flow.kickoff()
    flow.plot("llm")
