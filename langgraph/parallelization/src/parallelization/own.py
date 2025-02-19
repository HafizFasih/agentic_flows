# type: ignore
from langgraph.func import task, entrypoint

# ✅ Task 1: Find the best travel deals based on user preferences
@task
def find_travel_deals(input: dict) -> str:
    destination = input["destination"]
    budget = input["budget"]
    
    if budget < 500:
        deals = f"Best budget-friendly flights to {destination} starting at $299!"
    elif 500 <= budget < 1000:
        deals = f"Mid-range travel package to {destination} for $799 including hotel!"
    else:
        deals = f"Luxury vacation to {destination} for $1499 with all-inclusive stay!"
    
    return deals

# ✅ Task 2: Get the weather forecast for the destination
@task
def get_weather_forecast(input: dict) -> str:
    destination = input["destination"]
    
    weather_data = {
        "Paris": "Sunny, 22°C",
        "Tokyo": "Rainy, 18°C",
        "New York": "Cloudy, 20°C",
        "Dubai": "Hot, 35°C"
    }
    
    forecast = weather_data.get(destination.title(), "Weather data not available")
    return f"Weather in {destination}: {forecast}"

# ✅ Task 3: Generate AI-based personalized travel tips
@task
def generate_travel_tips(input: dict) -> str:
    destination = input["destination"]
    weather = input["weather_forecast"]
    
    # Simple rule-based tips instead of LLM
    tips = [
        f"Welcome to {destination}!",
        f"Based on the weather ({weather}), remember to pack appropriately.",
        "Check local attractions and book tickets in advance.",
        "Keep important documents and emergency contacts handy.",
        "Learn a few basic phrases in the local language."
    ]
    
    return "\n".join(tips)

# ✅ Parallel Execution Entry Point
@entrypoint()
def travel_planning_workflow(input: dict):
    futures = [
        find_travel_deals(input),
        get_weather_forecast(input),
    ]
    
    results = [future.result() for future in futures]
    travel_deals_result, weather_forecast_result = results[0], results[1]
    
    advice_future = generate_travel_tips({
        "destination": input["destination"],
        "travel_deals": travel_deals_result,
        "weather_forecast": weather_forecast_result
    })
    advice_result = advice_future.result()
    
    return {
        "best_travel_deals": f"\n{travel_deals_result}",
        "weather_forecast": f"{weather_forecast_result}",
        "personalized_travel_tips": f"\n{advice_result}"
    }

# ✅ Function to Invoke Workflow
def main():
    print("Trip Planner")
    destination = input("Enter the destination from the following list: Paris, Tokyo, New York, Dubai: ")
    budget = input("Enter your budget: ")
    result = travel_planning_workflow.invoke({
        "destination": destination,
        "budget": int(budget)
    })
    print(result.get("best_travel_deals"))
    print(result.get("weather_forecast"))
    print(result.get("personalized_travel_tips"))