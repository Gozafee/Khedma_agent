"""
Khedma Agent - Week 5
Rebuild of Week 4 agent using CrewAI framework.
Uses Ollama via LiteLLM OpenAI-compatible endpoint.
"""
import os
import time

# Configure environment for Ollama (must be before importing crewai)
os.environ["OPENAI_API_KEY"] = "ollama"
os.environ["OPENAI_BASE_URL"] = "http://localhost:11434/v1"
os.environ["OPENAI_API_BASE"] = "http://localhost:11434/v1"

from crewai import Agent, Task, Crew, Process, LLM


def create_khedma_crew():
    """Build the CrewAI agent, task, and crew."""

    # Use CrewAI's LLM class (v1.x compatible)
    llm = LLM(
        model="openai/yousif-khedma",  # Treat as OpenAI-compatible
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        temperature=0.0,
    )

    # Define the agent
    agent = Agent(
        role="Sudanese Passport Renewal Assistant",
        goal=(
            "Extract user data accurately: name, national_id, "
            "reason, location. Never invent data."
        ),
        backstory=(
            "Expert in Sudanese government procedures. "
            "Always use ONLY values from the user input."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=5,
    )

    # Define the task
    task = Task(
        description="""
        Extract the following fields from the user input:
        - name: Full name
        - national_id: National ID number
        - reason: Renewal reason
        - location: Inside Sudan or abroad

        STRICT RULES:
        1. Use ONLY values from the user input below.
        2. Do NOT invent data.
        3. If a field is missing, write "not specified".

        USER INPUT:
        {user_input}
        """,
        expected_output="JSON object with: name, national_id, reason, location",
        agent=agent,
    )

    # Create the crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True,
    )

    return crew


def run_crewai_agent(user_query: str):
    """Run the CrewAI agent and return result + timing."""
    crew = create_khedma_crew()

    start = time.time()
    result = crew.kickoff(inputs={"user_input": user_query})
    latency = time.time() - start

    return {
        "result": str(result),
        "latency": latency,
    }


if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Khedma Agent - CrewAI (Week 5)")
    print("=" * 60)

    test_query = (
        "اسمي يوسف عبدالمنعم، رقم هويتي 123456، "
        "عايز أجدد الجواز عشان مسافر"
    )
    print(f"\n📥 User Input: {test_query}\n")

    output = run_crewai_agent(test_query)

    print("\n" + "=" * 60)
    print("📤 RESULT:")
    print("=" * 60)
    print(output["result"])
    print(f"\n⏱️  Latency: {output['latency']:.2f} seconds")
    print("=" * 60)