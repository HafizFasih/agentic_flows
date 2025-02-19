# type: ignore
from langgraph.func import task, entrypoint
from litellm import completion
import json

@task
def math_expert(query: str) -> str:
    system_prompt = "You are a mathematics expert. Provide clear, accurate answers to math questions. Keep responses concise."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    response = completion(model="gemini/gemini-1.5-flash", messages=messages)
    return response.choices[0].message.content

@task
def history_expert(query: str) -> str:
    system_prompt = "You are a history expert. Provide accurate historical information and context. Keep responses concise."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    response = completion(model="gemini/gemini-1.5-flash", messages=messages)
    return response.choices[0].message.content

@task
def science_expert(query: str) -> str:
    system_prompt = "You are a science expert. Explain scientific concepts clearly and accurately. Keep responses concise."
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    response = completion(model="gemini/gemini-1.5-flash", messages=messages)
    return response.choices[0].message.content

def classify_query(query: str) -> str:
    system_prompt = """Classify the given query into one of these categories: 'math', 'history', or 'science'.
    Respond with only the category name in lowercase."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": query}
    ]
    response = completion(model="gemini/gemini-1.5-flash", messages=messages)
    return response.choices[0].message.content.strip().lower()

@entrypoint()
def problem_solver(input={"query": ""}):
    query = input["query"]
    subject = classify_query(query)
    
    if subject == "math":
        return math_expert(query).result()
    elif subject == "history":
        return history_expert(query).result()
    else:
        return science_expert(query).result()

def main():
    # Example usage
    user_query = input("Enter your question: ")
    result = problem_solver.invoke({"query": user_query})
    print("\nExpert Response:", result)

if __name__ == "__main__":
    main()




