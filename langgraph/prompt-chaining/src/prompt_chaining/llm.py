# type: ignore
from langgraph.func import task, entrypoint
from litellm import completion
from dotenv import load_dotenv, find_dotenv
import random

load_dotenv(find_dotenv())

@task
def generate_city():
    cities = ["Lahore", "Tokyo", "Paris", "New York", "Istanbul"]
    selected_city = random.choice(cities)
    print(f"Step 1: Generated city name: {selected_city}")
    return selected_city

@task
def create_city_fact(selected_city):
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=[
            {
                "role": "user",
                "content": f"Generate an interesting and unique historical fact about {selected_city} in one sentence."
            }
        ]
    )
    city_fun_fact = response["choices"][0]["message"]["content"]
    print(f"Step 2: Generated AI fact about {selected_city}")
    return city_fun_fact

@task
def enhance_fact(city_fun_fact):
    response = completion(
        model="gemini/gemini-1.5-pro",
        messages=[
            {
                "role": "user",
                "content": f"Make this fact more engaging by adding cultural context: {city_fun_fact}"
            }
        ]
    )
    enhanced_fact = response["choices"][0]["message"]["content"]
    print("Step 3: Enhanced the fact with cultural context")
    return enhanced_fact

@task
def save_fact_to_file(enhanced_fact):
    with open("llm_city_facts.txt", "w", encoding="utf-8") as output_file:
        output_file.write(enhanced_fact)
    print("Step 4: Saved enhanced fact to city_facts.txt")
    return enhanced_fact

@entrypoint()
def run_flow(input={}):
    selected_city = generate_city().result()
    city_fun_fact = create_city_fact(selected_city).result()
    enhanced_fact = enhance_fact(city_fun_fact).result()
    final_result = save_fact_to_file(enhanced_fact).result()
    return {"result": final_result}

def main() -> None:
    result = run_flow.invoke({})
    print("\nFinal Enhanced Fact:", result["result"])