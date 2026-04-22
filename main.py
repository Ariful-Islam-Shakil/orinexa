import sys
from google import genai
from components.config import Config
from components.tools import ALL_TOOLS
from components.agents import Agent

def main():
    """Main entry point for the Orinexa AI Assistant."""
    
    if not Config.GEMINI_API_KEY:
        print("❌ Error: GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)

    client = genai.Client(api_key=Config.GEMINI_API_KEY)
    
    agent = Agent(
        name="SmartAssistant",
        goal="Help users solve problems using tools and reasoning",
        backstory="An AI trained in computation, automation, and problem solving.",
        tools=ALL_TOOLS,
        client=client
    )

    print("\n" + "="*50)
    print("🚀 Orinexa AI Assistant is Ready!")
    print("Type 'exit' or 'quit' to end the session.")
    print("="*50 + "\n")

    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("\nGoodbye! 👋")
                break

            response = agent.run(user_input)
            
            print("\n" + "#"*80)
            print(f"Agent: {response.text}")
            print("#"*80 + "\n")

        except KeyboardInterrupt:
            print("\n\nSession ended by user.")
            break
        except Exception as e:
            print(f"\n❌ An error occurred: {e}\n")

if __name__ == "__main__":
    main()