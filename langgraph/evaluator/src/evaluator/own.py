# type: ignore
from langgraph.func import task, entrypoint


@task
def generate_response(state):
    state['password'] = input("\nEnter a password: ")
    return state


@task
def evaluate_response(state):
    password = state['password']
    state['score'] = 0

    if len(password) >= 8:
        state['score'] += 1
        print("✓ Password length is good")
    else:
        print("✗ Password should be at least 8 characters")
        
    if any(c.isdigit() for c in password):
        state['score'] += 1
        print("✓ Password contains numbers")
    else:
        print("✗ Password should contain numbers")
        
    if any(c in "!@#$%^&*" for c in password):
        state['score'] += 1
        print("✓ Password contains special characters")
    else:
        print("✗ Password should contain special characters")

    print(f"\nPassword strength score: {state['score']}/3")
    return state


@task
def check_quality(state):
    meets_threshold = True if state['score'] >= 2 else False
    if meets_threshold:
        print("\n✅ Password is strong enough!\n")
    else:
        print("\n❌ Password needs improvement")
    return meets_threshold


@entrypoint()
def evaluator_optimizer_flow(state):
    state = generate_response(state).result()
    state = evaluate_response(state).result()
    condition = check_quality(state)    
    
    while condition:
        state = generate_response(state).result()
        state = evaluate_response(state).result()
        condition = check_quality(state)

        if condition:
            break
    
    return state


def main():
    state = {}
    final_state = evaluator_optimizer_flow.invoke(state)
    print(final_state)
