#  type: ignore
from crewai.flow.flow import Flow, start, listen, router, or_

class AgentFlow(Flow):
    human_city = "karachi"
    llm_clarity = False
    @start()
    def Human(self):
        query = f"Human: How is the weather today...?"
        print(query)

    @router(or_("Human", "Environment"))
    def LLMCall(self, data):
        if not self.llm_clarity:
            print("LLM: Searching....")
            print("LLM: I have all the weather status about every city in the world")
            print("LLM: But... i need the city name to search the weather details of human")
            print("LLM: Let's check the human's environment to find the city name") # <= Action
            return "Search from envoirnment"
        else:
            weather_details = {
               "karachi": "Sunny",
               "lahore": "Cloudy",
               "islamabad": "Rainy",
               "peshawar": "Windy",
               "quetta": "Foggy",
               "multan": "Sunny",
            }
            print("LLM: I got the city name")
            print(f"LLM: It's {data}")
            print("LLM: Searching the weather details....")
            print(weather_details.get(data)) # <= Final Answer
            return "Output"

    @listen("Search from envoirnment")
    def Environment(self):
        print("Environment: Searching for it...")
        print("Environment: I found the city name")
        print(f"Environment: It's {self.human_city}") # <= FeedBack
        self.llm_clarity = True
        return self.human_city
    
    @listen("Output")
    def Out(self):
        print("Stopping the flow....")

    @listen("Out")
    def Stop(self):
        print("Flow is finished!")

def main():
    flow = AgentFlow()
    flow.kickoff()
    flow.plot("own")
