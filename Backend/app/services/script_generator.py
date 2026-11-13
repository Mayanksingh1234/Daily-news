from google import genai

from app.config import GEMINI_API_KEY


class ScriptGenerator:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    def generate(
        self,
        topic: str,
        sources: list[dict],
    ) -> str:

        research_text = ""

        for index, source in enumerate(
            sources,
            start=1
        ):
            research_text += f"""
SOURCE {index}

Title:
{source.get("title")}

URL:
{source.get("url")}

Published:
{source.get("published_at")}

Content:
{source.get("content")}

--------------------------------
"""

        prompt = f"""
You are an expert research summarizer
and podcast script writer.

Topic:
{topic}

Below are research results collected
from multiple web sources.

Your task is to summarize the most
important and reliable information and
turn it into a SHORT spoken podcast script.

Research:
{research_text}

STRICT REQUIREMENTS:

1. The final script must be between
   800 and 1000 words.

2. Focus only on the most important
   information from the research.

3. Remove repetitive information
   between sources.

4. Prioritize recent and relevant facts.

5. Mention important people, companies,
   numbers, dates, and events when
   relevant.

6. Only use information supported by
   the provided research.

7. Do not invent facts.

8. If sources disagree, briefly mention
   the uncertainty.

9. Write naturally for spoken audio.

10. Start with a short engaging
    introduction.

11. End with a concise summary.

12. Do not include headings.

13. Do not include stage directions.

14. Do not include URLs.

15. Do not include citations.

16. Do not write unnecessary background
    information.

17. The output will be sent directly
    to a text-to-speech API, so keep
    the language natural and concise.

Return ONLY the final podcast script.
"""

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        script = response.text.strip()

        print(
            f"Generated script: "
            f"{len(script)} characters"
        )

        print(
            f"Generated script: "
            f"{len(script.split())} words"
        )

        return script