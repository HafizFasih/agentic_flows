#  type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_
from litellm import completion

class StoryGeneratorFlow(Flow):
    model = "gemini/gemini-1.5-flash"
    story_theme = None
    story_outline = None
    
    @start()
    def GetTheme(self):
        query = "Human: Can you help me write a story?"
        print(query)
        return "Get theme from LLM"

    @router(or_("GetTheme", "RefineTheme"))
    def ThemeGenerator(self, data=None):
        if not self.story_theme:
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": "Generate a creative theme for a short story"}]
            )
            theme = response["choices"][0]["message"]["content"].strip()
            print(f"LLM: I suggest writing about: {theme}")
            print("LLM: Let me check if this theme needs refinement...")
            self.story_theme = theme
            return "Check theme"
        else:
            print(f"LLM: Great! Let's develop an outline for: {self.story_theme}")
            response = completion(
                model=self.model,
                messages=[{"role": "user", "content": f"Create a brief outline for a story about: {self.story_theme}"}]
            )
            outline = response["choices"][0]["message"]["content"].strip()
            self.story_outline = outline
            print(f"LLM: Here's your story outline:\n{outline}")
            return "Generate story"

    @listen("Check theme")
    def RefineTheme(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Should this story theme be refined or improved: {self.story_theme}? ***IMPORTANT*** Answer only with 'yes' or 'no'"}]
        )
        needs_refinement = "yes" in response["choices"][0]["message"]["content"].strip().lower()
        print(needs_refinement)
        if needs_refinement:
            print("LLM: I think we can do better. Let me try again...")
            self.story_theme = None
            return None
        else:
            print("LLM: This theme looks good!")
            return self.story_theme

    @listen("Generate story")
    def FinalStory(self):
        response = completion(
            model=self.model,
            messages=[{"role": "user", "content": f"Write a short story based on this outline: {self.story_outline}"}]
        )
        final_story = response["choices"][0]["message"]["content"].strip()
        print("\nFinal Story:")
        print(final_story)

    @listen("FinalStory")
    def Complete(self):
        print("\nStory generation complete!")

def main():
    flow = StoryGeneratorFlow()
    flow.kickoff()
    flow.plot("llm")
