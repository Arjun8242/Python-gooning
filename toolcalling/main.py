from agent import run_agent

def main():
    print("## Welcome to the Appointment Booking Assistant ##")
    print("How can I help you with your appointments?")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("## Thank you for using the Appointment Booking Assistant ##")
            break

        if not user_input:
            continue
            
        try:
            response = run_agent(user_input)
            print("Agent:", response)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()