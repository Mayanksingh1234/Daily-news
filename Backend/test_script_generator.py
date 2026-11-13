from app.services.script_generator import ScriptGenerator


generator = ScriptGenerator()

sources = [
    {
        "title": "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks",
        "url": "https://arxiv.org/abs/2005.11401",
        "published_at": "2020-05-22",
        "content": """
        Retrieval-Augmented Generation, or RAG, combines
        a language model with an external non-parametric
        memory. The system first retrieves relevant
        documents from an external knowledge source and
        then uses those retrieved documents as context
        when generating an answer.

        RAG was introduced to improve knowledge-intensive
        natural language processing tasks. Instead of
        relying entirely on information stored in the
        parameters of a language model, RAG allows the
        model to access external information during
        generation.

        The original approach uses a retriever to select
        relevant passages and a generator that produces
        the final output using the retrieved passages.
        """
    }
]

script = generator.generate(
    topic="How does retrieval augmented generation work?",
    sources=sources,
)

print("\n================ SCRIPT ================\n")
print(script)