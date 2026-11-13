from app.agents.research_agent import ResearchAgent


agent = ResearchAgent()

results = agent.research(
    "Startup funding announced in the last 24 hours"
)

for result in results:
    print("\n-----------------------------")
    print("TITLE:", result["title"])
    print("URL:", result["url"])
    print("PUBLISHED:", result["published_at"])
    print("CONTENT:", result["content"][:500])