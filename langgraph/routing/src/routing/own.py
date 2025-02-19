# type: ignore
from langgraph.func import task, entrypoint
import random

@task
def math_expert(query: str) -> str:
    print("User query: ", query)
    return "I am a math expert.\nThe answer to your question is 4"

@task
def history_expert(query: str) -> str:
    print("User query: ", query)
    return "I am a history expert.\nThe capital of France is Paris"

@task
def science_expert(query: str) -> str:
    print("User query: ", query)
    return "I am a science expert.\nThe speed of light is 299,792,458 m/s"

@entrypoint()
def problem_solver(input={}):
    data = [
        {"query": "What is the capital of France?", "subject": "history"},
        {"query": "What is 2 + 2?", "subject": "math"},
        {"query": "What is the speed of light?", "subject": "science"},
    ]
    random_data = random.choice(data)
    if random_data["subject"] == "math":
        return math_expert(random_data["query"]).result()
    elif random_data["subject"] == "history":
        return history_expert(random_data["query"]).result()
    else:
        return science_expert(random_data["query"]).result()

def main():
    result = problem_solver.invoke({})
    print(result)




