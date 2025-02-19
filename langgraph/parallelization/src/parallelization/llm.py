# type: ignore
import litellm
from langgraph.func import task, entrypoint

# ✅ Task 1: Find the best travel deals based on user preferences
@task
def find_travel_deals(input: dict) -> str:
    destination = input["destination"]
    budget = input["budget"]
    
    # Simulated travel deals based on budget
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
    
    # Simulated weather data (in reality, use an API like OpenWeather)
    weather_data = {
        "Paris": "Sunny, 22°C",
        "Tokyo": "Rainy, 18°C",
        "New York": "Cloudy, 20°C",
        "Dubai": "Hot, 35°C"
    }
    
    forecast = weather_data.get(destination, "Weather data not available")
    return f"Weather in {destination}: {forecast}"

# ✅ Task 3: Generate AI-based personalized travel tips
@task
def generate_travel_tips(input: dict) -> str:
    destination = input["destination"]
    travel_deals = input["travel_deals"]
    weather_forecast = input["weather_forecast"]
    
    prompt = f"""
    A user is planning a trip to {destination}. Here are the travel deals available:
    {travel_deals}

    Also, the weather forecast for the destination is:
    {weather_forecast}

    Based on this information, provide personalized travel tips and recommendations.
    """
    
    response = litellm.completion(
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

# ✅ Parallel Execution Entry Point
@entrypoint()
def travel_planning_workflow(input: dict):
    futures = [
        find_travel_deals(input),
        get_weather_forecast(input),
    ]
    
    # Wait for travel deals and weather forecast before AI advice
    results = [future.result() for future in futures]
    travel_deals_result, weather_forecast_result = results[0], results[1]
    
    # Generate AI travel tips based on results
    advice_future = generate_travel_tips({
        "destination": input["destination"],
        "travel_deals": travel_deals_result,
        "weather_forecast": weather_forecast_result
    })
    advice_result = advice_future.result()
    
    return {
        "best_travel_deals": travel_deals_result,
        "weather_forecast": weather_forecast_result,
        "personalized_travel_tips": advice_result
    }

# ✅ Function to Invoke Workflow
def main():
    result = travel_planning_workflow.invoke({
        "destination": "Paris",
        "budget": 750  # User-defined budget
    })
    print(result)