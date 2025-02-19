# type: ignore
from langgraph.func import task, entrypoint

@task
def generate_city():
    selected_city = "Lahore"
    print(f"Step 1: Generated city name: {selected_city}")
    return selected_city

@task
def create_city_fact(selected_city):
    city_fun_fact = f"{selected_city} is known for its historic architecture and delicious food."
    print(f"Step 2: Generated fun fact about {selected_city}")
    return city_fun_fact

@task
def save_fact_to_file(city_fun_fact):
    with open("own_city_facts.md", "w") as output_file:
        output_file.write(city_fun_fact)
    print("Step 3: Saved fun fact to own.txt")

@entrypoint()
def run_flow(input={}):
    selected_city = generate_city().result()
    city_fun_fact = create_city_fact(selected_city).result()
    save_fact_to_file(city_fun_fact)

def main() -> None:
    run_flow.invoke({})