from src.router import Router

print("Vitalis Core Initialized. Type your input to imprint the synthetic mind.")
router = Router()

while True:
    user_input = input(">> ")
    if user_input.lower() == "exit":
        break
    router.process(user_input)
    print("Signal imprinted.")
